import wx


'''
def wrapper(func, self=None):
    # With this instruction we change receive bound method instead of a function
    print('here here')
    bound_method = func.__get__(self, type(self))
    wx.CallLater(500, execute_every(bound_method))
    return bound_method()

def execute_every(func):

    def execute_every_setter(value):
        execute_every.was_called = value

    def has_been_called():
        return execute_every.was_called

    if not hasattr(execute_every, 'was_called'):

        print('here')
        execute_every.was_called = True

        wrapper(func)
    return wrapper
'''


def execute_every(func):
    def wrapper(self=None):
        # With this instruction we change receive bound method instead of a function
        bound_method = func.__get__(self, type(self))
        wx.CallLater(500, execute_every(bound_method))
        return bound_method()
    return wrapper