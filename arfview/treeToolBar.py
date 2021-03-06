from PySide import QtCore,QtGui
import pyqtgraph as pg
from arfview import datatree
import numpy as np

class treeToolBar(QtGui.QToolBar):
    def __init__(self, tree_view): 
        super(treeToolBar, self).__init__()
        self.tree_view = tree_view
        self.check_multiple_win = None
        self.initUI()

    def initUI(self):
        checkMultipleAction = QtGui.QAction('Check Multiple',self)
        checkMultipleAction.triggered.connect(self.check_multiple)
        uncheckAllAction = QtGui.QAction('Uncheck All', self)
        uncheckAllAction.triggered.connect(self.uncheck_all)
        self.addAction(checkMultipleAction)
        self.addAction(uncheckAllAction)

    def check_multiple(self):
        self.check_multiple_win = _checkMultipleWindow(self)
        self.check_multiple_win.show()

    def uncheck_all(self):
        dsets = self.tree_view.all_dataset_elements()
        for d in dsets:
             d.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
        
class _checkMultipleWindow(QtGui.QDialog):
    def __init__(self, treeToolBar):
        super(_checkMultipleWindow, self).__init__()
        self.tree_view = treeToolBar.tree_view
        self.initUI()
        
    def initUI(self):
        self.attribute_label = QtGui.QLabel("Check entries with attribute")
        self.value_label = QtGui.QLabel("equal to")
        self.value_menu = QtGui.QComboBox()
        self.attribute_menu = attributeMenu(self.tree_view, self.value_menu)
        
        self.ok_button=QtGui.QPushButton("OK")
        self.ok_button.pressed.connect(self.button_pressed)
        
        ledge=0
        uedge=0
        
        layout=QtGui.QGridLayout()
        layout.addWidget(self.attribute_label, uedge+1, ledge)
        layout.addWidget(self.value_label, uedge+2, ledge)
        layout.addWidget(self.attribute_menu, uedge+1, ledge+1)
        layout.addWidget(self.value_menu, uedge+2,ledge+1)
        layout.setRowStretch(3, 2)
        layout.addWidget(self.ok_button, 3, 0)
        self.setLayout(layout)

    def button_pressed(self):
        key = self.attribute_menu.attribute
        value = self.attribute_menu.attribute_value
        dsets = self.tree_view.all_dataset_elements()
        for d in dsets:
            dataset = d.getData()
            attribute_objects = [dataset.attrs, dataset.parent.attrs]
            for attrs in attribute_objects:
                if key in attrs.keys() and attrs[key] == value:
                    d.setCheckState(0, QtCore.Qt.CheckState.Checked)

        self.close()
            
class attributeMenu(QtGui.QComboBox):
    def __init__(self, tree_view, value_menu):
        super(attributeMenu, self).__init__()
        self.tree_view = tree_view
        self.value_menu = value_menu
        self.attribute = None
        self.attribute_value = None
        
        # adding all attribute keys in tree
        self.addItem('')
        dsets = self.tree_view.all_dataset_elements()
        attributes = []
        for d in dsets:
            dataset = d.getData()
            for a in dataset.attrs.keys() + dataset.parent.attrs.keys():
                 if a not in attributes:
                    attributes.append(a)
                    self.addItem(a)

        self.activated[str].connect(self.attribute_selected)
        self.value_menu.activated[str].connect(self.value_selected)
        
    def attribute_selected(self,text):
        self.attribute = text
        self.value_menu.clear()
        self.value_menu.addItem('')
        dsets = self.tree_view.all_dataset_elements()
        values = []
        for d in dsets:
            dataset = d.getData()
            attribute_objects= [dataset.attrs, dataset.parent.attrs]
            for attrs in attribute_objects:
                if self.attribute not in attrs.keys(): continue
                #avoiding problems with array comparison
                if isinstance(attrs[self.attribute], np.ndarray):
                    is_new_value = not np.any([np.array_equal(attrs[self.attribute],v)
                                               for v in values])
                else:
                    is_new_value = attrs[self.attribute] not in values
                if is_new_value:
                    values.append(attrs[self.attribute])
                    if self.attribute == 'datatype':
                        new_value = datatree.named_types[attrs[self.attribute]]
                    else:
                        new_value = str(attrs[self.attribute])
                    try:
                        self.value_menu.addItem(new_value)
                    except:
                        pass
                    
    def value_selected(self, text):
        if self.attribute == 'datatype':
            inverse_types = {value:key for key,value in
                             datatree.named_types.iteritems()}
            self.attribute_value = inverse_types[text]
        elif text.isdigit():
            self.attribute_value = float(text)
        else:
            self.attribute_value = text

        
            