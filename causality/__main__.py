from gui import gui
from configurator import configurator


def main():

    # The configuration file is fix
    data = configurator.get_config()
    applied_input_files = []
    # applied_input_file = data['input_files']
    applied_input_files = data['input_file_test']

    g = gui()
    g.build_gui(applied_input_files)
    g.start_gui()


if __name__ == "__main__":
    main()
