from PySide6 import QtCore, QtWidgets

from .ui.selection_list_ui import Ui_SelectionList


class SelectionList(QtWidgets.QWidget, Ui_SelectionList):

    items_added = QtCore.Signal(list)
    items_removed = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.link_signals()

    def init_lists(self, src, dest):
        # Check if source and destination intersect
        intersect = list(set(src) & set(dest))
        if intersect:
            # remove elements from src that are present in dest
            src = list(set(src) - set(dest))

        self.list_src.addItems(src)
        self.list_dest.addItems(dest)

    def disable_items(self, to_disable, src=True):
        # if they intersect, disable selected choices
        widget = self.list_src if src else self.list_dest
        for tag in to_disable:
            res = widget.findItems(tag, QtCore.Qt.MatchExactly)
            if res:
                item = res[0]
                item.setFlags(QtCore.Qt.NoItemFlags)

    def enable_items(self, to_enable, src=True):
        # if they intersect, disable selected choices
        widget = self.list_src if src else self.list_dest
        for tag in to_enable:
            item = widget.findItems(tag, QtCore.Qt.MatchExactly)[0]
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def link_signals(self):
        self.btn_add.clicked.connect(self.add)
        self.btn_remove.clicked.connect(self.remove)

    def add(self):
        moved = self.move_items(self.list_src, self.list_dest)
        self.items_added.emit(moved)

    def remove(self):
        moved = self.move_items(self.list_dest, self.list_src)
        self.items_removed.emit(moved)

    def move_items(self, src, dest, items=None):
        if not items:
            items = src.selectedItems()
        moved = [self.move_item(src, dest, item) for item in items]
        return moved

    @staticmethod
    def move_item(src, dest, item):
        row = src.row(item)
        src.takeItem(row)
        dest.addItem(item)
        return str(item.text())

    def get_src_text(self):
        return self.get_text(self.list_src)

    def get_dest_text(self):
        return self.get_text(self.list_dest)

    @staticmethod
    def get_text(list_widget):
        return [str(list_widget.item(i).text()) for i in range(list_widget.count())]
