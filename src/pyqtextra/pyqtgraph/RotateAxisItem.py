import math

from pyqtgraph.graphicsItems.AxisItem import AxisItem


class RotateAxisItem(AxisItem):
    def __init__(self, *args, angle=90, **kwargs):
        print("init rotate")
        super().__init__(*args, **kwargs)
        self._angle = angle
        self._height_updated = False

    def drawPicture(self, p, axisSpec, tickSpecs, textSpecs):

        p.setRenderHint(p.Antialiasing, False)
        p.setRenderHint(p.TextAntialiasing, True)

        ## draw long line along axis
        pen, p1, p2 = axisSpec
        p.setPen(pen)
        p.drawLine(p1, p2)
        p.translate(0.5, 0)  ## resolves some damn pixel ambiguity

        ## draw ticks
        for pen, p1, p2 in tickSpecs:
            p.setPen(pen)
            p.drawLine(p1, p2)

        # Draw all text
        if self.style["tickFont"] is not None:
            p.setFont(self.style["tickFont"])
        p.setPen(self.textPen())

        max_width = 0
        for rect, flags, text in textSpecs:
            p.save()  # save the painter state

            p.translate(rect.center())  # move coordinate system to center of text rect
            p.rotate(self._angle)  # rotate text
            p.translate(-rect.center())  # revert coordinate system

            x_offset = math.ceil(
                math.fabs(math.sin(math.radians(self._angle)) * rect.width())
            )
            if self._angle < 0:
                x_offset = -x_offset
            p.translate(
                x_offset / 2, 0
            )  # Move the coordinate system (relatively) downwards

            p.drawText(rect, flags, text)
            p.restore()  # restore the painter state
            offset = math.fabs(x_offset)
            max_width = offset if max_width < offset else max_width

        #  Adjust the height
        if not self._height_updated:
            self.setHeight(self.height() + max_width + 40)
            self._height_updated = True
