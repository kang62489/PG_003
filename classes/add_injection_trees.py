## Modules
# Standard library imports
import json

# Local application imports
from controllers.handlers_add_injection import ADD_INJECTION_HANDLERS
from util.constants import MODELS_DIR
from views.view_add_injections import ADD_INJECTION_VIEW


class ADD_INJECTION_TREES:
    def __init__(self, ui, model):
        self.ui = ui
        self.model = model
        self.clone_list = self.prepare_clone_list()
        # Initiate the input panel when click the button "Add"
        self.view_addInj = ADD_INJECTION_VIEW(self.clone_list, parent=self.ui)

        # Initiate handlers
        self.handlers_addInj = ADD_INJECTION_HANDLERS(self, self.view_addInj, self.ui, self.model)

    def _load_clone_JSON_file(self, filename):
        with open(MODELS_DIR / filename, "r") as f:
            loaded = json.load(f)
            sorted_clones = dict(sorted(loaded.items()))
            return sorted_clones

    def _update_clone_JSON_files(self, filename, new_clone_dict):
        with open(MODELS_DIR / filename, "w") as f:
            json.dump(new_clone_dict, f, indent=4)

    def prepare_clone_list(self):
        # Load clone list from JSON files (also update the JSON files)
        clone_red = self._load_clone_JSON_file("menuList_clones_red.json")
        self._update_clone_JSON_files("menuList_clones_red.json", clone_red)
        clone_green = self._load_clone_JSON_file("menuList_clones_green.json")
        self._update_clone_JSON_files("menuList_clones_green.json", clone_green)

        # Combine the two colors of clone lists and then short only the clone number-color
        clone_list = (clone_red | clone_green).keys()
        return clone_list
