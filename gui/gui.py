import wx
from gui.main_frame.main_frame_content import MainFrame


class GuiApp:
    def __init__(self, size=None, title="", *args, **kwargs):
        self.application = wx.App(False)
        self.main_frame = MainFrame(*args, size=size, title=title, **kwargs)
        self.is_closing = False

    @property
    def is_closing(self):
        return self._is_closing

    @is_closing.setter
    def is_closing(self, value):
        self._is_closing = value

    def start(self):
        """
            The usage of 'MainLoop' method of wxpython app (that can only be ran in a main
            thread) makes impossible to run this function anywhere but the Main Thread, therefore
            it should be summoned at the end of other threads the application uses
            e.g:

                def __init__(self):
                    some_thread = threading.Thread(*args, **kwargs)
                    some_other_thread = threading.Thread(*args, **kwargs)
                    app = GuiApp(*args, **kwargs)

                def launch_app(self):
                    some_thread.start()
                    some_other_thread.start()
                    app.start()
        """
        self.main_frame.render()
        self.application.MainLoop()
        self.close()

    def close(self):
        self.is_closing = True
