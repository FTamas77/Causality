class logger:

    class __logger:

        def __init__(self, top, text_widget):
            self.top = top
            self.text_widget = text_widget

    instance = None

    def __init__(self, top, text_widget):
        if not logger.instance:
            logger.instance = logger.__logger(top, text_widget)
        else:
            logger.instance.top = top
            logger.instance.text_widget = text_widget

    @staticmethod
    def print_log(inputStr):
        # TODO: This should not be static.
        if not logger.instance:
            raise Exception("logger instance is not created")
        else:
            logger.instance.text_widget.insert('1.0', inputStr)
            logger.instance.text_widget.insert('1.0', "\n")
            logger.instance.top.update()
