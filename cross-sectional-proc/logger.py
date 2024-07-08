def init(top, text_widget):
    global logger
    logger = __logger(top, text_widget)


class __logger:

    def __init__(self, top, text_widget):
        self.text_widget = text_widget
        self.top = top

    def print_log(self, inputStr):
        logger.text_widget.insert('1.0', inputStr)
        logger.text_widget.insert('1.0', "\n")
        logger.top.update()
