


class BaseMouseListener():
    """
        Mouse callback function input...
        callback function return None
        (x,y)
    """
    def __idle(self, *args):
        return

    def __init__(self):
        self.mouse_pressed_func = self.__idle
        self.mouse_released_callback = self.__idle
        self.mouse_motion_callback = self.__idle



    def add_mouse_pressed_callback(self, func):
        self.mouse_pressed_func = func
    def add_mouse_released_callback(self, func):
        self.mouse_released_callback = func
    def add_mouse_motion(self, func):
        self.mouse_motion_callback = func
    

    




class MouseManager():
    """
        callback is mouse listener Object
    """
    def __init__(self):
        self.mouse_listener_list = []
    


    def add_listener(self, listener : BaseMouseListener):
        self.mouse_listener_list.append(listener)
    def process_event(self, event):
        """
            event is pygame event.
        """

        if event.type == MOUSEBUTTONDOWN:
            self._mouse_pressed(event)
        elif event.type == MOUSEBUTTONUP:
            self._mouse_released(event)
        elif event.type == MOUSEMOTION:
            self._mouse_motion(event)

    def _mouse_released(self, event):
        for callback in self.mouse_listener_list:
            
            callback.mouse_released_callback(event)


    def _mouse_pressed(self, event):
        for callback in self.mouse_listener_list:
            callback.mouse_pressed_func(event)

    def _mouse_motion(self, event):
        for callback in self.mouse_listener_list:
            callback.mouse_motion_callback(event)


