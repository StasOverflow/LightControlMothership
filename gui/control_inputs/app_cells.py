import wx
from gui.control_inputs.image_cell import VariableImageCell
from gui.control_inputs.checkbox_cell import CheckBoxCell


class AppSpecificImageCell(VariableImageCell):

    def __init__(self, parent, is_input_indication=True, is_conn=False, *args, **kwargs):
        if is_conn:
            img_true = './static/images/yellow_led_button_5.png'
        else:
            if is_input_indication:
                img_true = './static/images/green_led_button_5.png'
            else:
                img_true = './static/images/red_led_button_5.png'
        img_false = './static/images/disabled_button_5.png'
        super().__init__(parent, true_image_path=img_true, false_image_path=img_false, *args, **kwargs)


class AppSpecificCheckBoxCell(CheckBoxCell):
    """
        A proxy alias for CheckBoxCell
    """
    def __init__(self, *args, **kwargs):
        super(AppSpecificCheckBoxCell, self).__init__(*args, **kwargs)
