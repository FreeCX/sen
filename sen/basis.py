from copy import deepcopy
from math import log10


class Node:
    def __init__(self, *, name=None, inputs=0, outputs=0, func=None):
        self.name = name
        self.func = func
        self.nodes = []
        self.wires = {}
        self.wire_input = []
        self.wire_output = []
        self.tests = []
        self.set_io(inputs=inputs, outputs=outputs)

    def count_nodes(self):
        if hasattr(self.func, '__call__'):
            return 1
        return sum([node.count_nodes() for node in self.nodes])

    def last(self):
        return len(self.nodes) - 1

    def add(self, node):
        self.nodes.append(deepcopy(node))
        return self.last()

    def connect_input(self, *, node, out_input, node_input):
        self.wire_input.append((node, node_input, out_input))

    def connect_output(self, *, node, out_output, node_output):
        self.wire_output.append((node, node_output, out_output))

    def connect_wires(self, *, a, b, a_output, b_input):
        if a not in self.wires:
            self.wires[a] = [{'node': b, 'from': a_output, 'to': b_input}]
        else:
            self.wires[a].append({'node': b, 'from': a_output, 'to': b_input})

    def set_io(self, *, inputs=None, outputs):
        self.input = [None for _ in range(inputs)]
        self.output = [None for _ in range(outputs)]
        self.input_count = inputs
        self.output_count = outputs

    def set_tests(self, tests):
        self.tests = tests

    def run_tests(self):
        test_count = len(self.tests)
        len_count = round(log10(test_count)) if test_count > 0 else 0

        print(f'--- {self.name} ---')
        if test_count == 0:
            print('TEST NOT PRESENTED')

        for index, data in enumerate(self.tests):
            inp_data = data[0:self.input_count]
            out_data = data[self.input_count:]
            self.input = inp_data
            self.execute()
            status = 'PASSED' if self.output == out_data else 'FAIL'
            print('test {1:0{0}}: {2}'.format(len_count, index, status))
            if not status:
                print(f'  input: {inp_data}, output: {out_data}, expected: {out_data}')

    def execute(self):
        if hasattr(self.func, '__call__'):
            self.func(input=self.input, output=self.output) 
        else:
            # передаём сигналы на все подключенные входы
            for nid, nwire, bwire in self.wire_input:
                # print(nid, nwire, bwire)
                self.nodes[nid].input[nwire] = self.input[bwire]

            # TODO:
            # - тут будет логика расчёта распространения сигнала
            # - и скорее обход графа
            # - а пока простой обход
            for idn, node in enumerate(self.nodes):
                node.execute()
                # если выход ноды подключен дальше
                if idn in self.wires:
                    for connect in self.wires[idn]:
                        # то распространяем сигнал с её выхода, на входы других элементов
                        b_id, out_id, in_id = connect['node'], connect['from'], connect['to']
                        self.nodes[b_id].input[in_id] = self.nodes[idn].output[out_id]

            # получаем значения выходов
            for nid, nwire, bwire in self.wire_output:
                self.output[bwire] = self.nodes[nid].output[nwire]

    def state(self):
        print(f'--- {self.name} ---')
        print(f' nodes: {self.count_nodes()}')
        print(f' input: {self.input}')
        print(f'output: {self.output}')
