class ContextMenuItem:
    def __init__(self, menu=None, context_register_callback=None, **kwargs):
        print("init context")
        self.menu = menu
        self.contextRegisterCallback = context_register_callback

    def contextMenuEvent(self, event):
        # if not self.activated:
        #     return
        print("menu event")
        if self.contextRegisterCallback:
            self.contextRegisterCallback(self)

        self.menu.exec_(event.screenPos())
