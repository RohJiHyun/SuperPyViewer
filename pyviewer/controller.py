



class UIController():
    def __init__(self, root_view, model):
        pass

    def compile(self):
        pass





class InspectorController():
    def __init__(self, inspector, world):
        self.inspector = inspector


    def compile(self):
        self._extract_ui()
        self._connect_to_world()

    def _extract_ui(self):
        #rotation
        self.rot_x, self.rot_y, self.rot_z = self.inspector.get_ui_component("rotation")

        (self.face_label, ) = self.inspector.get_ui_component("face")

        (self.vertice, ) = self.inspector.get_ui_component('vertice')
        (self.selected_v_idx, ) = self.inspector.get_ui_component("selected vertex number")

    def _connect_to_world(self):
        # data = self.world.data_container_list[0]
        # self.rot_x.set_text(str(data.rot_x))
        # self.rot_y.set_text(str(data.rot_y))
        # self.rot_z.set_text(str(data.rot_z))
        # self.rot_x.textChanged.connect()
        # self.rot_y
        # self.rot_z
        pass
    






