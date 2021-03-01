import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

def idle():
    pass


MENU_BAR =      {
                'file' : 
                        {
                            'new' : {'shortcut' : 'Ctrl+N', 'tip' : ""},
                            'open' : {'shortcut' : 'Ctrl+N', 'tip' : ""}
                        },
                'edit' : 
                        {

                        }

                }

BASE_INSPECTER = {
                    "name"                   : [{"widget" : QLabel, "args" : [""]}],
                    "rotation"               : [{"widget" : QLineEdit, "args" :["0.0"]}, {"widget" : QLineEdit, "args" :["0.0"]}, {"widget" : QLineEdit, "args" :["0.0"]}], #for X,Y,Z
                    "vertice"                : [{"widget" : QLabel, "args" : ["0"]}],
                    "face"                   : [{"widget" : QLabel, "args" : ["0"]}],
                    "selected vertex number" : [{"widget" : QLabel, "args" :["None"]}],
                    "sharable"               : [{"widget" : QComboBox, "args" :[]}],
                    "custom function"        : [{"widget" : QPushButton, "args" : ["active custom func"]}]

                 }

STATUS_BAR = {
                "mouse_x" :{"widget"},
                "mouse_y" : {},
                "mouse_status" :{},
                "camera pos" : {},
                "camera_rotation" : {}
}



class BaseUI(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.mapping_table = dict()

    def initUI(self):
        pass

    def add_to_mapping_table(self, key, obj):
        """
            regist ui component to mapping_table
            return back ui component obejct.
        """
        if key not in self.mapping_table.keys():
            self.mapping_table[key] = []
        self.mapping_table[key].append(obj)
        
        return obj

    def get_ui_component(self, key):
        """
            
            each element in mapping table is list of components. 
            using it to connect signal.
            recommend implementing it in controller class.
            
            return mapping_table elements : list
        """
        reval = []
        if key in self.mapping_table.keys():
            reval = self.mapping_table[key]
        return reval
class BaseUIMenuBar(BaseUI):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def initUI(self):
        pass
    
    def init_file_action_group(self):
        pass

    def init_edit_action_group(self):
        pass

    
class UIMenuBar(BaseUIMenuBar):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def initUI(self):
        self.menubar = self.parent.menuBar()
        self.menubar.setNativeMenuBar(False)
        for menu_key in MENU_BAR:
            p_menu = self.menubar.addMenu(menu_key)
            self.init_action_group(menu_key, p_menu)

    def init_action_group(self, key_name, parent_menu):
        topic = MENU_BAR['file']
        for key in topic:

            component = QAction(key, self.parent)
            component.setShortcut(topic[key]['shortcut'])
            component.setStatusTip(topic[key]['tip'])
            # file_action.triggerd.connect(topic[key]['callback'])
            # component.triggered.connect((qApp.quit))
            self.add_to_mapping_table(key, component)

            parent_menu.addAction(component)

        
#TODO ANIMATION UI CONTROLL CLASS
class BaseInspectorUI(BaseUI):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.docking_area = Qt.RightDockWidgetArea

    def set_size_constraint(self, layout):
        # layout.resize(0,0)
        pass


class InspectorUI(BaseInspectorUI):
    def __init__(self, parent, name="inspector"):
        super().__init__(parent=parent)
        self.name = name
        self.window = QWidget(parent)
    

    def initUI(self):
        self.make_outter_layout()
        self.parent.add_window(self.window, isdock=True, name=self.name, allowed_area = self.docking_area)

    def make_outter_layout(self):
        # self.outter_layout = QVBoxLayout()
        self.outter_layout = QFormLayout()
        for key in BASE_INSPECTER:
            # inner_comp = self.make_inner_layout(key)
            # self.outter_layout.addLayout(inner_comp)
            comp_name, comp = self.make_inner_layout(key)
            self.outter_layout.addRow(comp_name, comp)

        self.set_size_constraint(self.outter_layout)


        self.outter_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.window.setLayout(self.outter_layout)
        # self.outter_layout.setHorizontalSpacing(0)


    def make_inner_layout(self, key):
        # layout = QHBoxLayout()
        # layout.addWidget(QLabel(key))
        
        # for obj in BASE_INSPECTER[key]: #list of objects to inflate.
        #     inflated_ui = obj['widget'](*obj['args'], self.parent)
        #     self.add_to_mapping_table(key, inflated_ui)
        #     # self.mapping_table[key].append(inflated_ui)
        #     layout.addWidget(inflated_ui)
            
        
        # return layout
        layout = QHBoxLayout()
        
        
        for obj in BASE_INSPECTER[key]: #list of objects to inflate.
            inflated_ui = obj['widget'](*obj['args'], self.parent)
            self.add_to_mapping_table(key, inflated_ui)
            # self.mapping_table[key].append(inflated_ui)
            layout.addWidget(inflated_ui)
            
        self.set_size_constraint(layout)

        return QLabel(key), layout


