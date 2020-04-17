from sen import render


def set_one(obj):
    print('set RS trigger')
    obj.input = [0, 1]
    obj.execute()


def set_zero(obj):
    print('reset RS trigger')
    obj.input = [1, 0]
    obj.execute()

def read_state(obj):
    obj.input = [0, 0]
    obj.execute()
    return obj.output[0]


if __name__ == '__main__':
    render.to_python('./schema/rs_trigger.seb')

    from schema.rs_trigger import rs_trigger

    element = rs_trigger()

    read_state_count = 5
    for func in [set_zero, set_zero, set_one, set_zero, set_one, set_one]:
        func(element)
        state = [read_state(element) for _ in range(read_state_count)]
        print(f'read state {read_state_count} times: {state}')