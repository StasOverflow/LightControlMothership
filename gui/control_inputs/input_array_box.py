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


# print = print_decorator(print)


class InputArray(wx.BoxSizer):

    @staticmethod
    def zeroer(value):
        return 1 if value is not None else 0

    def __init__(
            self,
            parent,
            interface=defs.INPUT_INTERFACE,
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
            In case table's rows or cols labels are not None, we create 
            display matrix one row or(and) col larger then initial dimension
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

        self.instance_array = [
            Cell(
                self.parent, interface_type=interface,
                label=self.cell_titles[i],
                **kwargs
            ) for i in range(self.cols_quantity * self.rows_quantity)
        ]

        self.instance_matrix = [
            [
                self.instance_array[i + j * self.cols_quantity]
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
        for row_index in range(len(self.instance_matrix) + self.addit_row):
            if row_index == 0 and self.addit_row:
                for col_title in self.col_titles:
                    label = wx.StaticText(self.parent, label=col_title)
                    display_matrix.Add(label, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
            else:
                integer = 0
                fxd_row_id = row_index-self.addit_row
                for col_index in range(len(self.instance_matrix[fxd_row_id]) + self.addit_col):
                    integer += 1
                    if col_index == 0 and self.addit_col:
                        label = wx.StaticText(self.parent, label=self.row_titles[row_index])
                        display_matrix.Add(label, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
                    else:
                        fxd_col_id = col_index - self.addit_col
                        display_matrix.Add(
                            self.instance_matrix[fxd_row_id][fxd_col_id],
                            1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND
                        )
        static_box_sizer.Add(display_matrix)
        self.Add(static_box_sizer, 0)

    @property
    def values(self):
        value_list = list()
        for instance in self.instance_array:
            value_list.append(instance.checked)
        return value_list

    @values.setter
    def values(self, new_array):
        for index in range(len(self.instance_array)):
            self.value_set_by_index(index, new_array[index])

    def value_set_by_index(self, index, value=True):
        if index > len(self.instance_array):
            index = len(self.instance_array)
        elif index < 0:
            index = 0
        self.instance_array[index].checked = value

    @property
    def instance_array(self):
        return self._instance_array

    @instance_array.setter
    def instance_array(self, new_array):
        self._instance_array = new_array

    @property
    def visible_instances(self):
        array = list()
        for instance in self.instance_array:
            array.append(instance.is_visible)
        return array

    @visible_instances.setter
    def visible_instances(self, new_array):
        for index, bool_value in enumerate(new_array):
            self.instance_array[index].is_visible = bool_value


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
