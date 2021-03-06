import logging
import sys
from multiprocessing import freeze_support

from PySide2 import QtWidgets

from hyo2.sis.app.mainwin import MainWin


class DebugFilter(logging.Filter):

    def filter(self, record):

        if record.name[:3] != "hyo":
            return False

        # if (record.name == 'hyo2.soundspeed.listener.sis.sis') and \
        #         (record.funcName == "parse") and (record.levelname == "INFO"):
        #     return False

        return True


# logging settings
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # change to WARNING to reduce verbosity, DEBUG for high verbosity
ch_formatter = logging.Formatter('%(levelname)-9s %(name)s.%(funcName)s:%(lineno)d > %(message)s')
ch.setFormatter(ch_formatter)
ch.addFilter(DebugFilter())
logger.addHandler(ch)


def sis_gui():
    """create the main windows and the event loop"""

    app = QtWidgets.QApplication(sys.argv)

    main = MainWin()
    main.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    freeze_support()
    sis_gui()
