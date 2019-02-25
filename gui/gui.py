import wx
from gui.gui_sequences.tabs import BaseTwoSplitTab
from gui.gui_sequences.tabs import TopTab
from gui.control_inputs.input_array_box import defs
from gui.gui_sequences.menu import MenuBarSequence


class _MainFrame(wx.Frame):

    def __init__(self, *args, pos=(0,0), size=(400, 300), title="", **kwargs):
        self.size = size
        print('size is ', self.size)
        self.pos = (0, 0)

        self.super_sizer = wx.BoxSizer(wx.VERTICAL)

        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER
        style = style ^ wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, None,
                          title=title,
                          style=style,
                          size=self.size,
                          pos=self.pos)

        self.Center()
        menu_bar = MenuBarSequence(parent=self)

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
        tab1 = BaseTwoSplitTab(
                    parent=notebook,
                    iface_types=(defs.DISPLAY_INTERFACE, defs.INPUT_INTERFACE),
                    outlined=False,
                    left_panel_title='Status:',
                    right_panel_title='Setup:',
                    right_panel_button_title='Configure',
        )
        tab2 = BaseTwoSplitTab(notebook)  # , (20, 20), None)
        tab3 = BaseTwoSplitTab(notebook)  # , (20, 20), None)
        tab4 = BaseTwoSplitTab(notebook)  # , (20, 20), None)
        notebook.AddPage(tab1, "Relay 1")
        notebook.AddPage(tab2, "Relay 2")
        notebook.AddPage(tab3, "Relay 3")
        notebook.AddPage(tab4, "Relay 4")

        '''
            Here goes a very important line of a code, setting notebook
            item's color to default window color instead of white color,
            chosen as is
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

        main_sizer.Layout()
        main_panel.SetSizer(main_sizer)

        self.super_sizer.Add(main_sizer, wx.EXPAND)

        self.SetMenuBar(menu_bar)
        # self.SetSizer(self.super_sizer)

        '''
            Must be called after all items are set, according to doc files. 
            If not, any items, initialized after calling SetMenuBar method
            won't be rendered
        '''

    def render(self):
        self.Show()

    def combined_inputs_states_get(self):
        pass
        # return self.top_canvas.right_panel_checkbox_matrix.values_get(True)


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
        return

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
        """
            Here we destroy all child widgets to our main frame widget
        """
        # self.main_frame.Destroy()
        self.is_closing = True