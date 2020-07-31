import wx
import wx.grid
import defs
from gui.control_inputs.cell import Cell

PRINTIO = True


def print_decorator(func):
    def wrapped_func(*args, **kwargs):
        if PRINTIO:
            return func(*args, **kwargs)
    return wrapped_func


# print = print_decorator(print)


class InputArray(wx.BoxSizer):

    def __init__(
            self,
            parent,
            interface=defs.INPUT_INTERFACE,
            title=None,
            dimension=(1, 1),
            row_titles=None,
            col_titles=None,
            cell_titles=None,
            secret_ids=None,
            outlined=True,
            **kwargs
    ):

        # Basic Construction procedure
        super().__init__(wx.VERTICAL)
        self.cols_quantity = dimension[1]
        self.rows_quantity = dimension[0]
        self.col_titles = col_titles
        self.row_titles = row_titles
        self.parent = parent
        self.outlined = outlined
        self.cell_active_quantity = self.cols_quantity * self.rows_quantity

        # FIXME: What are secret ids ?
        if secret_ids is None:
            secret_id_array = [None for _ in range(15)]
        else:
            secret_id_array = secret_ids

        # If row or col is named, than title list should be extended
        self.additional_row = self.col_titles is not None
        self.additional_col = self.row_titles is not None

        # And whitespaces should be added in front of title lists
        if self.additional_row:
            if self.row_titles is not None:
                self.row_titles = [''] + self.row_titles
        if self.additional_col:
            if self.col_titles is not None:
                self.col_titles = [''] + self.col_titles

        # FIXME: Assigning cell titles other than '' doesn't work
        self.cell_titles = [
            '' for _ in range(self.cell_active_quantity)
        ] if cell_titles is None else cell_titles

        # Create an instance array to access data by 1D index
        self.instance_array = [
            Cell(
                self.parent, interface_type=interface,
                label=self.cell_titles[i], secret_id=secret_id_array[i],
                **kwargs,
            ) for i in range(self.cell_active_quantity)
        ]

        # Create an instance matrix to sort out stuff in 2D
        self.instance_matrix = [
            [
                self.instance_array[i + j * self.cols_quantity]
                for i in range(self.cols_quantity)
            ]
            for j in range(self.rows_quantity)
        ]

        self.title = title
        self.grid_render()

    def grid_render(self):
        if self.outlined:
            static_box = wx.StaticBox(self.parent, wx.ID_ANY, self.title)
            box_sizer = wx.StaticBoxSizer(static_box, wx.HORIZONTAL)
        else:
            box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        col_quantity = self.cols_quantity + self.additional_col
        row_quantity = self.rows_quantity + self.additional_row

        display_matrix = wx.GridSizer(row_quantity, col_quantity, hgap=15, vgap=15)

        for row_id in range(row_quantity):
            if row_id == 0 and self.additional_row:
                # Add col titles to the 0'th row
                for col_title in self.col_titles:
                    # Add Label(title) object to grid
                    label = wx.StaticText(self.parent, label=col_title)
                    display_matrix.Add(label, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
            else:
                data_row_id = row_id-self.additional_row
                for col_id in range(col_quantity):
                    # Add row titles to the 0'th col
                    if col_id == 0 and self.additional_col:
                        # Add Label(title) object to grid
                        label = wx.StaticText(self.parent, label=self.row_titles[row_id])
                        display_matrix.Add(label, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
                    else:
                        # Add cell object from instance matrix to grid
                        data_col_id = col_id - self.additional_col
                        display_matrix.Add(
                            self.instance_matrix[data_row_id][data_col_id],
                            1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND
                        )
        box_sizer.Add(display_matrix)
        self.Add(box_sizer, 0, wx.TOP, 0)

    def enable(self):
        for cell in self.instance_array:
            cell.enable()

    def disable(self):
        for cell in self.instance_array:
            cell.disable()

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

    def value_set_by_index(self, index, value):
        if index > 0 or index < len(self.instance_array):
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


def main():

    app = wx.App()
    da_frame = wx.Frame(parent=None, title='Calculator')
    da_panel = wx.Panel(parent=da_frame)

    da_panel.Centre()

    checkboxer = InputArray(
        parent=da_panel,
        title='Checkboxes:',
        dimension=(3, 5),
        col_titles=['1', '2', '3', '4', '5'],
        row_titles=['X3', 'X2', 'X1'],
    )

    da_panel.SetSizer(checkboxer)
    da_panel.Fit()

    da_frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
