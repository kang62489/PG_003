## Modules
# Standard library imports
import json

# Third-party imports
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QComboBox

# Local application imports
from util.constants import MODELS_DIR, MenuOptions


class HelperComboEditor(QObject):
    def __init__(self, target_combobox, target_combobox_model, parent_widget):
        """
        target_combobox: the target combobox to be made editable
        target_combobox_model: the model of the target combobox, created by the ModelDynamicList class in model_dynamic_list.py,
        this model was initialized in the class ViewExpInfo. A loadMenu function in the class was also removed.
        parent_widget: for set eventfilter (detect ESC key)
        """
        super().__init__()
        self.target_combobox = target_combobox
        self.target_combobox_model = target_combobox_model
        self.parent_widget = parent_widget

        # For detecting ESC key to cancel editing
        self.parent_widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        The event filter to handle ESC key to cancel editing in combobox.
        obj: the parent widget which eventFilter is installed.
        event: the event to be filtered
        """
        if event.type() == QEvent.KeyPress:
            focused_widget = QApplication.focusWidget()
            if event.key() == Qt.Key_Escape and isinstance(focused_widget, QComboBox):
                """Check the "ESC" is pressed and the focused widget is a combobox"""
                focused_widget.setEditable(False)
                return True
        return super().eventFilter(obj, event)

    def add_new_item_to_menu(self):
        """Enable editing mode to add a new item to the combobox

        Note: No lambda needed here because target_combobox is stored as instance variable.

        Why you might use lambda with a generic function:
        If you want ONE function to handle MULTIPLE comboboxes:

        # Generic function with parameters (reusable):
        def add_item(self, cb, model):
            cb.setEditable(True)
            ...

        # Use lambda to apply to many comboboxes:
        btn1.clicked.connect(lambda: self.add_item(comboBox_ACUC, model1))
        btn2.clicked.connect(lambda: self.add_item(comboBox_Species, model2))
        btn3.clicked.connect(lambda: self.add_item(comboBox_Genotype, model3))

        # Without lambda (separate method for each):
        def add_item_ACUC(self): ...
        def add_item_Species(self): ...
        def add_item_Genotype(self): ...
        """
        self.target_combobox.setEditable(True)
        self.target_combobox.clearEditText()
        self.target_combobox.setFocus()
        try:
            self.target_combobox.lineEdit().returnPressed.disconnect()
        except RuntimeError:
            # For the first time, there is no connection to disconnect
            pass

        self.target_combobox.lineEdit().returnPressed.connect(self.on_edit_done)

    def on_edit_done(self):
        new_item = self.target_combobox.currentText()
        self.target_combobox_model.list_of_options.append(new_item)
        """Update the menulist of the combobox saved in the JSON file"""
        self.update_menuList_JSON_files()
        self.target_combobox.setEditable(False)
        """Set the new item as the current item, now the saved items are sorted, need to find it's index"""
        # self.target_combobox.setCurrentIndex(self.target_combobox.count() - 1)
        index_of_new_item = self.target_combobox_model.list_of_options.index(new_item)
        self.target_combobox.setCurrentIndex(index_of_new_item)

    def update_menuList_JSON_files(self):
        for model_name, file_name in MenuOptions.MENU_LIST_FILES.items():
            if model_name == self.target_combobox_model.name:
                file_path = MODELS_DIR / file_name
                break
            with open(file_path, "w") as f:
                json.dump(self.target_combobox_model.list_of_options, f, indent=4)

            # The updateList method defined in model_dynamic_list.py. It is used to sort the list_of_options
            # That's also why emit layoutChanged here (Not at the self.target_combobox_model.list_of_options.apppend(new_item))
            # Therefore the new searching item index in on_edit_done() can work properly
            self.target_combobox_model.updateList(self.target_combobox_model.list_of_options)
            self.target_combobox_model.layoutChanged.emit()

    def remove_new_item_from_menu(self):
        item_to_be_removed = self.target_combobox.currentText()
        self.target_combobox_model.list_of_options.remove(item_to_be_removed)
        self.update_menuList_JSON_files()
        self.target_combobox.setCurrentIndex(0)
