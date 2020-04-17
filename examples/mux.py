from sen import render

if __name__ == '__main__':
    render.to_python('./schema/mux.seb')

    from schema.mux import mux

    element = mux()
    element.run_tests()