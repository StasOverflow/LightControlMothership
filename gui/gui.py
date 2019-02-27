import wx
from gui.gui_sequences.tabs.tabs import BaseTwoSplitTab
from gui.gui_sequences.tabs.tabs import TopTab, BtmTab
from gui.control_inputs.input_array_box import defs
from gui.gui_sequences.menu.menu import MenuBarSequence
from settings import Settings


class _MainFrame(wx.Frame):

    def __init__(self, *args, pos=(0,0), size=(400, 300), title="", **kwargs):
        self.size = size
        print('size is ', self.size)
        self.pos = (0, 0)

        self.super_sizer = wx.BoxSizer(wx.VERTICAL)

        self.settings = Settings()

        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER
        style = style ^ wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, None,
                          title=title,
                          style=style,
                          size=self.size,
                          pos=self.pos)

        self.Center()
        self.menu_bar = MenuBarSequence(parent=self, **kwargs)

        main_panel = wx.Panel(parent=self, size=self.size)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        print(main_panel.GetBackgroundColour())

        # Top of the page sequence
        top_page_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_canvas = TopTab(parent=main_panel, iface_types=(defs.INPUT_INTERFACE, defs.DISPLAY_INTERFACE))

        top_page_sizer.Add(self.top_canvas, 1, wx.EXPAND)

        # Bottom of the page sequence
        bottom_page_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btm_canvas = wx.Panel(parent=main_panel)

        bottom_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)

        notebook = wx.Notebook(self.btm_canvas)
        self.btm_tab1 = BtmTab(parent=notebook)
        self.btm_tab2 = BtmTab(parent=notebook)
        self.btm_tab3 = BtmTab(parent=notebook)
        self.btm_tab4 = BtmTab(parent=notebook)

        notebook.AddPage(self.btm_tab1, "Relay 1")
        notebook.AddPage(self.btm_tab2, "Relay 2")
        notebook.AddPage(self.btm_tab3, "Relay 3")
        notebook.AddPage(self.btm_tab4, "Relay 4")

        '''
            Here goes a very important line of a code, setting notebook
            item's color to default window color instead of white color,
            chosen by default, when creating widget
        '''
        notebook.SetOwnBackgroundColour((240, 240, 240, 255))

        bottom_inner_sizer.Add(notebook, 5, wx.EXPAND | wx.CENTER)

        bottom_page_sizer.Add(bottom_inner_sizer, 1, wx.EXPAND)
        self.btm_canvas.SetSizer(bottom_page_sizer)

        other_panel = wx.Panel(parent=main_panel)

        '''
            Second parameter in every main_sizer.Add method call is a proportion
            value for every element of the window
        '''
        main_sizer.Add(top_page_sizer, 38,  wx.EXPAND)
        main_sizer.Add(self.btm_canvas, 48, wx.EXPAND | wx.CENTER)
        main_sizer.Add(other_panel, 3, wx.EXPAND | wx.CENTER)

        main_panel.SetSizer(main_sizer)
        main_panel.Layout()

        # self.super_sizer.Add(main_sizer, wx.EXPAND)

        '''
            Must be called after all items are set, according to doc files. 
            If not, any items, initialized after calling SetMenuBar method
            won't be rendered
        '''
        self.SetMenuBar(self.menu_bar)
        # self.SetSizer(self.super_sizer)

    def settings_update(self):
        """
            Update settings canvas values, specified inside

            Yet unspecified:
                self.top_canvas.left_panel.status.value

        """
        self.top_canvas.left_panel.device_port.value = self.settings.device_port
        self.top_canvas.left_panel.slave_id.value = self.settings.slave_id
        self.top_canvas.left_panel.refresh_rate.value = self.settings.refresh_rate

    def state_update(self, state):
        self.btm_tab1.left_panel.checkbox_matrix.check_box_instance_matrix[0][4].checked = state

    def render(self):
        self.Show()


class GuiApp:
    def __init__(self, size=(400, 300), title="", *args, **kwargs):
        self.application = wx.App(False)
        self.main_frame = _MainFrame(*args, size=size, title=title, **kwargs)
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
