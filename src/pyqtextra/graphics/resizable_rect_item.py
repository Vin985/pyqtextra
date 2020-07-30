import copy

from PySide2 import QtCore, QtGui, QtWidgets


class ResizableRectItem(QtWidgets.QGraphicsRectItem):

    DETECTION_RANGE_PROP = 0.2
    RESIZE_LIMIT_PROP = 0.2

    def __init__(self, *args, callback=None, rectChangedCallback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.callback = callback
        self.rectChangedCallback = rectChangedCallback
        self.resize_activated = False
        self.resize_side = False
        self.moving = False
        self.activated = False
        self.resizeBox = None
        self.resizeFunction = None
        self.resizeBoxColor = QtGui.QColor(0, 0, 0, 50)
        self.setupResizeBox()

    def setupResizeBox(self):
        self.resizeBox = QtWidgets.QGraphicsRectItem(self)
        self.resizeBox.setRect(self.rect().x(), self.rect().y(), 0, 0)
        self.resizeBoxPenWidth = 0
        penColor = copy.copy(self.resizeBoxColor)
        penColor.setAlpha(255)
        pen = QtGui.QPen(penColor)
        pen.setWidthF(self.resizeBoxPenWidth)
        self.resizeBox.setPen(pen)
        self.resizeBox.setBrush(QtGui.QBrush(self.resizeBoxColor))
        self.resizeBox.setFlag(QtWidgets.QGraphicsItem.ItemStacksBehindParent, True)

    def setResizeBoxColor(self, color):
        if isinstance(color, str):
            color = QtGui.QColor(color)
        self.resizeBoxColor = color
        self.setupResizeBox()

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange and self.callback:
            self.callback(value)

        return super().itemChange(change, value)

    def activate(self):
        self.activated = True
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def deactivate(self):
        self.deactivateResize()
        self.activated = False
        self.setFlags(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setCursor(QtCore.Qt.ArrowCursor)

    # def contextMenuEvent(self, event):
    #     wa = QtWidgets.QWidgetAction(self.parent)
    #     self.cle = ContextLineEdit(self.parent)
    #     wa.setDefaultWidget(self.cle)
    #
    #     menu = QtWidgets.QMenu(self.parent)
    #     menu.addAction("test")
    #     menu.addAction(wa)
    #     menu.exec_(event.screenPos())

    def drawResizeBox(self, x, y, width, height):
        self.resizeBox.setVisible(True)
        self.resize_activated = True
        # self.deactivate()
        self.resizeBox.setRect(self.rect().x() + x, self.rect().y() + y, width, height)

    def activate_move(self):
        self.drawResizeBox(
            self.rect().width() * self.RESIZE_LIMIT_PROP,
            self.rect().height() * self.RESIZE_LIMIT_PROP,
            self.rect().width() - 2 * self.rect().width() * self.RESIZE_LIMIT_PROP,
            self.rect().height() - 2 * self.rect().height() * self.RESIZE_LIMIT_PROP,
        )
        self.setCursor(QtCore.Qt.SizeAllCursor)
        self.activate()
        self.resize_activated = False

    def deactivateResize(self):
        self.activate()
        self.resize_activated = False
        self.resizeBox.setVisible(False)

    def mouse_close_to(self, x, y):
        horizontal = 0
        vertical = 0

        if x < self.rect().width() * self.DETECTION_RANGE_PROP:
            horizontal = -1
        elif x > self.rect().width() - self.rect().width() * self.DETECTION_RANGE_PROP:
            horizontal = 1

        if y < self.rect().height() * self.DETECTION_RANGE_PROP:
            vertical = -1
        elif (
            y > self.rect().height() - self.rect().height() * self.DETECTION_RANGE_PROP
        ):
            vertical = 1

        return horizontal, vertical

    def activate_resize_box(self, close_to):
        horizontal, vertical = close_to
        x = 0
        y = 0
        width = self.rect().width()
        height = self.rect().height()
        cursor = 0
        if vertical:
            height *= self.RESIZE_LIMIT_PROP
            cursor = QtCore.Qt.SizeVerCursor
            if vertical > 0:
                y = self.rect().height() - height

        if horizontal:
            width *= self.RESIZE_LIMIT_PROP
            if cursor:
                # already have a vertical resize. Use diagonals
                if vertical + horizontal:
                    # |vertical + horizontal| = 2 for top-left and bottom-right
                    cursor = QtCore.Qt.SizeFDiagCursor
                else:
                    # vertical + horizontal = 0 for top-right and bottom-left
                    cursor = QtCore.Qt.SizeBDiagCursor
            else:
                # use horizontal cursor
                cursor = QtCore.Qt.SizeHorCursor
            if horizontal > 0:
                x = self.rect().width() - width

        self.drawResizeBox(x, y, width, height)
        self.setCursor(cursor)

    def hoverMoveEvent(self, event):
        if not self.activated:
            return

        itemPos = event.pos()
        x = itemPos.x() - self.rect().x()
        y = itemPos.y() - self.rect().y()

        is_close = self.mouse_close_to(x, y)
        if any(is_close):
            self.activate_resize_box(is_close)
        else:
            self.activate_move()

    def hoverLeaveEvent(self, event):
        self.deactivateResize()

    def resize_box(self, dx, dy):
        horizontal, vertical = self.resize_side
        rect = self.rect()
        coords = [0, 0, 0, 0]  # list(self.rect().getCoords())
        if horizontal:
            if horizontal < 0:
                coords[0] += dx
            else:
                coords[2] += dx
        if vertical:
            if vertical < 0:
                coords[1] += dy
            else:
                coords[3] += dy
        rect.adjust(*coords)
        self.setRect(rect)
        self.activate_resize_box(self.resize_side)

    def mousePressEvent(self, event):
        if not self.activated:
            return

        itemPos = event.pos()
        x = itemPos.x() - self.rect().x()
        y = itemPos.y() - self.rect().y()

        if self.resize_activated:
            self.resize_side = self.mouse_close_to(x, y)

    def mouseMoveEvent(self, event):
        if not self.activated:
            return

        if not self.resize_activated:
            return super().mouseMoveEvent(event)

        itemPos = event.pos()
        lastPos = event.lastPos()
        dx = itemPos.x() - lastPos.x()
        dy = itemPos.y() - lastPos.y()

        self.resize_box(dx, dy)

    def setRect(self, *args, **kwargs):
        super().setRect(*args, **kwargs)
        if self.rectChangedCallback:
            self.rectChangedCallback()
