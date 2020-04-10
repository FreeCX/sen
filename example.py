from itertools import product
from sen import render


if __name__ == '__main__':
    render.to_python('./schema/full_adder_block.seb', recursive=True)

    from schema.full_adder_block import full_adder_block

    element = full_adder_block()
    element.state()
    element.run_tests()