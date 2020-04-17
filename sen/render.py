from datetime import datetime as dt
from pathlib import Path
import json
import re

from sen.node import default_impl
from sen import parser


FIND_NODE = re.compile(r'^\w+')
FIND_PORT = re.compile(r'\[\d+\]$')


def extract(text):
    node = FIND_NODE.search(text).group(0)
    port = FIND_PORT.search(text).group(0)[1:-1]
    return node, port


def to_python(filename, *, recursive=False):
    filename = Path(filename)

    if not filename.exists():
        raise FileExistsError(filename)

    data = parser.load(filename.open())

    # update connections
    module_name = data['configuration']['name']
    inputs, outputs, wires = [], [], []
    for a, _, b in data['connection']:
        if a in data['configuration']['input']:
            node, node_port = extract(b)
            inputs.append((node, a, node_port))
        elif b in data['configuration']['output']:
            node, node_port = extract(a)
            outputs.append((node, b, node_port))
        else:
            a_node, a_port = extract(a)
            b_node, b_port = extract(b)
            wires.append((a_node, b_node, a_port, b_port))
    data['connection'] = {'input': inputs, 'output': outputs, 'wire': wires}

    # build all modules
    if recursive:
        for module in data['import']:
            if module not in default_impl:
                file = filename.parent / f'{module}.seb'
                to_python(file, recursive=True)

    # info
    render_data = '"""\nTHIS FILE IS AUTOGENERATED\n'\
    			  'DATE: ' + dt.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'\
    			  f'MODULE: {module_name}\n"""\n'\

    # imports
    render_data += 'from sen.basis import Node\n'
    for module in data['import']:
        if module in default_impl:
            render_data += f'from sen.node import {module}\n'
        else:
            render_data += f'from .{module} import {module}\n'

    # function
    render_data += f'\n\ndef {module_name}():\n'
    inputs = len(data['configuration']['input'])
    outputs = len(data['configuration']['output'])
    render_data += f"    node = Node(name='{module_name}', inputs={inputs}, outputs={outputs})\n"
    
    # blocks
    for k, v in data['element'].items():
        render_data += f'    {k} = node.add({v}())\n'
    for i, v in enumerate(data['configuration']['input']):
        render_data += f'    {v} = {i}\n'
    for i, v in enumerate(data['configuration']['output']):
        render_data += f'    {v} = {i}\n'

    # connection
    for idn, block, node in data['connection']['input']:
        render_data += f'    node.connect_input(node={idn}, out_input={block}, node_input={node})\n'
    for idn, block, node in data['connection']['output']:
        render_data += f'    node.connect_output(node={idn}, out_output={block}, node_output={node})\n'
    for a, b, v1, v2 in data['connection']['wire']:
        render_data += f'    node.connect_wires(a={a}, b={b}, a_output={v1}, b_input={v2})\n'

    # tests
    tests = []
    for test in data['test']:
        block = list(map(int, filter(lambda x: x != '->', test)))
        tests.append(block)
    render_data += f'    tests = {tests}\n'
    render_data += '    node.set_tests(tests)\n'

    # last statement
    render_data += '    return node\n'

    # write file
    output = filename.parent / f'{module_name}.py'
    with output.open('w') as f:
        f.write(render_data)
