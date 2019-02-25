import wx
import wx.grid
from itertools import chain
from gui.control_inputs import defs
from gui.control_inputs.cell import Cell

PRINTIO = True


def print_decorator(func):
    def wrapped_func(*args, **kwargs):
        if PRINTIO:
            return func(*args, **kwargs)
    return wrapped_func


print = print_decorator(print)


class InputArray(wx.BoxSizer):

    @staticmethod
    def zeroer(value):
        return 1 if value is not None else 0

    def __init__(
            self,
            parent,
            iface_type=defs.DISPLAY_INTERFACE,
            title=None,
            dimension=(1, 1),
            row_titles=None,
            col_titles=None,
            cell_titles=None,
            orientation=wx.HORIZONTAL,
            outlined=True,
            *args,
            **kwargs,
    ):
        self.outlined = outlined
        super().__init__(orientation)
        self.cols_quantity = dimension[1]
        self.rows_quantity = dimension[0]
        self.col_titles = col_titles
        self.row_titles = row_titles
        self.parent = parent

        '''
            In case table's rows or cols labels are not None, then we should create 
            display display matrix one row or col larger then initial dimension
        '''
        self.addit_row = self.zeroer(self.col_titles)
        self.addit_col = self.zeroer(self.row_titles)
        if self.addit_row:
            if self.row_titles is not None:
                self.row_titles = [''] + self.row_titles
        if self.addit_col:
            if self.col_titles is not None:
                self.col_titles = [''] + self.col_titles

        self.cell_titles = [
            '' for _ in range(self.rows_quantity * self.cols_quantity)
        ] if cell_titles is None else cell_titles
        self.check_box_instance_matrix = [
            [
                Cell(self.parent, interface_type=iface_type, label=self.cell_titles[i + j * self.cols_quantity])
                for i in range(self.cols_quantity)
            ]
            for j in range(self.rows_quantity)
        ]
        # print(self.check_box_instance_matrix)

        self.title = title
        self.grid_render()

    def grid_render(self):
        if self.outlined:
            static_box = wx.StaticBox(self.parent, wx.ID_ANY, self.title)
            static_box_sizer = wx.StaticBoxSizer(static_box, wx.HORIZONTAL)
        else:
            static_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        display_matrix = wx.GridSizer(0)
        display_matrix.SetHGap(15)
        display_matrix.SetVGap(15)
        display_matrix.SetCols(self.cols_quantity + self.addit_col)
        display_matrix.SetRows(self.rows_quantity + self.addit_row)
        for row_index in range(len(self.check_box_instance_matrix) + self.addit_row):
            if row_index == 0 and self.addit_row:
                for col_title in self.col_titles:
                    label = wx.StaticText(self.parent, label=col_title)
                    display_matrix.Add(label, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
            else:
                integer = 0
                fxd_row_id = row_index-self.addit_row
                for col_index in range(len(self.check_box_instance_matrix[fxd_row_id]) + self.addit_col):
                    integer += 1
                    if col_index == 0 and self.addit_col:
                        label = wx.StaticText(self.parent, label=self.row_titles[row_index])
                        display_matrix.Add(label, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
                    else:
                        fxd_col_id = col_index - self.addit_col
                        display_matrix.Add(
                            self.check_box_instance_matrix[fxd_row_id][fxd_col_id],
                            1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND
                        )
                        self.check_box_instance_matrix[fxd_row_id][fxd_col_id].checked = True
        static_box_sizer.Add(display_matrix)
        self.Add(static_box_sizer, 0)

    def _input_interface_state_set(self, state=defs.DISPLAY_INTERFACE):
        pass
        # checbox_iterable_list = list(chain.from_iterable(zip(*self.check_box_instance_matrix)))
        # for item in checbox_iterable_list:
            # item.DoEnable(False if state == defs.DISPLAY_INTERFACE else True)

    def input_interface_enable(self):
        self._input_interface_state_set(state=defs.INPUT_INTERFACE)

    def input_interface_disable(self):
        self._input_interface_state_set(state=defs.DISPLAY_INTERFACE)

    def values_get(self, as_matrix=False):
        vals = list()
        print('-' * 35)
        if as_matrix:
            for row in self.check_box_instance_matrix:
                row_list = list()
                for instance in row:
                    row_list.append(instance.checked)
                vals.append(row_list)
                print(row_list)
        else:
            checbox_iterable_list = list(chain.from_iterable(self.check_box_instance_matrix))
            for checkbox in checbox_iterable_list:
                instance = checkbox.checked
                vals.append(instance)
            print(vals)
        print('-' * 35)
        return vals


class Supapanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)


def main():

    app = wx.App()
    da_frame = wx.Frame(parent=None, title='Calculator')
    da_panel = Supapanel(parent=da_frame)

    da_panel.Centre()

    checkboxer = InputArray(
        parent=da_panel,
        title='Checkboxes:',
        dimension=(3, 5),
        col_titles=['1', '2', '3', '4', '5'],
        row_titles=['X3', 'X2', 'X1'],
        orientation=wx.VERTICAL
    )

    da_panel.SetSizer(checkboxer)
    da_panel.Fit()

    da_frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
