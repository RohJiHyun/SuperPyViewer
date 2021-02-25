

class KeyListener():
    """
        function input is pygame event
    """
    def __idle(self, *args):
        return


    def __init__(self):
        self.key_pressed = self.__idle
        self.key_released = self.__idle



    def add_key_pressed_callback(self, func):
        self.key_pressed = func

    def add_key_released_callback(self, func):
        self.key_released = func









class KeyManager():
    def __init__(self, con_key_limit):
        self.key_pressed = []

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

    


KeyManager()