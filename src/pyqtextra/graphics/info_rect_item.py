from PySide6 import QtGui, QtWidgets
from .resizable_rect_item import ResizableRectItem


class InfoRectItem(ResizableRectItem):
    def __init__(self, *args, infoString="", **kwargs):
        super().__init__(*args, **kwargs)
        self.infoString = infoString
        self.infoTextItem = QtWidgets.QGraphicsSimpleTextItem(infoString, parent=self)
        self.infoTextFont = QtGui.QFont("", 12)
        self.infoTextItem.setPos(self.rect().x(), self.rect().y() - 20)

    def setupInfoTextItem(self, fontSize=12, color=None):
        self.infoTextFont = QtGui.QFont("", fontSize)
        self.infoTextItem.setFont(self.infoTextFont)

        if not color:
            color = QtGui.QColor(0, 0, 0)
        elif not isinstance(color, QtGui.QColor):
            color = QtGui.QColor(color)
        self.setTextColor(color)

    def setRectColor(self, color):
        self.setPen(QtGui.QPen(color))

    def setTextColor(self, color):
        self.infoTextItem.setBrush(QtGui.QBrush(color))

    def setColor(self, color):
        self.setRectColor(color)
        self.setTextColor(color)

    def setInfoString(self, s):
        self.infoString = s
        if self.infoString and self.infoTextItem:
            self.infoTextItem.setText(self.infoString)

    def hoverEnterEvent(self, event):
        if not self.activated:
            return
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if not self.activated:
            return
        super().hoverLeaveEvent(event)

    def mouseMoveEvent(self, event):
        if not self.activated:
            return
        super().mouseMoveEvent(event)
        self.infoTextItem.setPos(self.rect().x(), self.rect().y() - 20)

    def setRect(self, *args, **kwargs):
        super().setRect(*args, **kwargs)
        if self.infoTextItem:
            font_height = QtGui.QFontMetrics(self.infoTextFont).height()
            self.infoTextItem.setPos(self.rect().x(), self.rect().y() - font_height)
