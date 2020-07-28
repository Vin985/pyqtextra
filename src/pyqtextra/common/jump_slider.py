from PySide2 import QtWidgets, QtCore


class JumpSlider(QtWidgets.QSlider):

    seek_position = QtCore.Signal(int)

    def get_position(self, event):
        pos = QtWidgets.QStyle.sliderValueFromPosition(
            self.minimum(), self.maximum(), event.x(), self.width()
        )
        self.seek_position.emit(pos)
        return pos

    def mousePressEvent(self, ev):
        """ Jump to click position """
        self.setValue(self.get_position(ev))

    def mouseMoveEvent(self, ev):
        """ Jump to pointer position while moving """
        self.setValue(self.get_position(ev))
