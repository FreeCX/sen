from sen import render


def setE(state, element, inp):
    element.input = inp
    element.execute()
    print(f'[{state}]: {element.input} -> {element.output}')


if __name__ == '__main__':
    render.to_python('./schema/flip_flop.seb')

    from schema.flip_flop import flip_flop

    element = flip_flop()

    one, hold, reset = ('  one', [1, 0, 1]), (' hold', [0, 0, 1]), ('reset', [0, 1, 1])
    for name, data in [one, hold, reset, hold, one, hold, hold, reset, hold, hold]:
        setE(name, element, data)