from sen.basis import Node


default_impl = ['NAND', 'NOR', 'NOT', 'AND', 'OR', 'XOR']


def NAND():
    def op_nand(input, output):
        output[0] = (not (input[0] and input[1])) % 2

    node = Node(name='nand', inputs=2, outputs=1, func=op_nand)
    node.set_tests([(0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0)])

    return node


def NOR():
    def op_nor(input, output):
        output[0] = ((not input[0]) and (not input[1])) % 2

    node = Node(name='nor', inputs=2, outputs=1, func=op_nor)
    node.set_tests([(0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 0)])

    return node


def NOT():
    def op_not(input, output):
        output[0] = (not input[0]) % 2

    node = Node(name='not', inputs=1, outputs=1, func=op_not)
    node.set_tests([(0, 1), (1, 0)])

    return 


def AND():
    def op_and(input, output):
        output[0] = (input[0] and input[1]) % 2

    node = Node(name='and', inputs=2, outputs=1, func=op_and)
    node.set_tests([(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 1)])

    return node


def OR():
    def op_or(input, output):
        output[0] = (input[0] or input[1]) % 2

    node = Node(name='or', inputs=2, outputs=1, func=op_or)
    node.set_tests([(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1)])

    return node


def XOR():
    def op_xor(input, output):
        output[0] = (input[0] ^ input[1]) % 2

    node = Node(name='xor', inputs=2, outputs=1, func=op_xor)
    node.set_tests([(0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 1, 0)])

    return node