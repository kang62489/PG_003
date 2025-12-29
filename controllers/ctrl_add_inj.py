## Third-party imports
import pendulum
from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QColor, QFont, QStandardItem

## Local application imports
from classes import DialogCloneInfo


class CtrlAddInj(QObject):
    """A class of creating a input panel for adding"""

    def __init__(self, parent, view_addInj, ui, model):
        super().__init__()
        self.parent = parent
        self.view_addInj = view_addInj
        self.ui = ui
        self.model = model
        self.connect_signals()
        self.refresh_clone_menus()
        self.auto_cal_incubation()
        self.view_addInj.cb_InjectateTypeCtrl.setCurrentIndex(1)

    def connect_signals(self):
        self.view_addInj.de_inj_DOI.dateChanged.connect(self.auto_cal_incubation)

        self.view_addInj.cb_InjectionModeCtrl.currentIndexChanged.connect(self.injection_mode_ctrl)
        self.view_addInj.cb_InjectateTypeCtrl.currentIndexChanged.connect(self.injectate_type_ctrl)

        self.view_addInj.btn_cloneInfo.triggered.connect(self.show_clone_info)
        self.view_addInj.btn_refresh_clone_1.clicked.connect(self.refresh_clone_menus)
        self.view_addInj.btn_refresh_clone_2.clicked.connect(self.refresh_clone_menus)
        self.view_addInj.buttonBox.accepted.connect(self.accept_adding_injection)
        self.view_addInj.buttonBox.rejected.connect(self.cancel_adding_injection)

    def injection_mode_ctrl(self, index):
        if index == 1:
            self.view_addInj.container_3.setEnabled(False)
        else:
            self.view_addInj.container_3.setEnabled(True)

    def injectate_type_ctrl(self, index):
        if index == 1:
            self.view_addInj.cb_vector_2.setEnabled(False)
            self.view_addInj.container_2.setEnabled(False)
            self.view_addInj.cb_mixing_ratio.setEnabled(False)
        else:
            self.view_addInj.cb_vector_2.setEnabled(True)
            self.view_addInj.container_2.setEnabled(True)
            self.view_addInj.cb_mixing_ratio.setEnabled(True)

    def refresh_clone_menus(self):
        self.clone_red = self.parent._load_clone_JSON_file("menuList_clones_red.json")
        self.parent._update_clone_JSON_files("menuList_clones_red.json", self.clone_red)
        self.clone_green = self.parent._load_clone_JSON_file("menuList_clones_green.json")
        self.parent._update_clone_JSON_files("menuList_clones_green.json", self.clone_green)
        self.clone_dict = self.clone_red | self.clone_green

        self.clone_codes = (self.clone_red | self.clone_green).keys()
        self.view_addInj.cb_clone_1.clear()
        self.view_addInj.cb_clone_1.addItems(self.clone_codes)
        self.view_addInj.cb_clone_2.clear()
        self.view_addInj.cb_clone_2.addItems(self.clone_codes)

    def show_clone_info(self):
        self.dlg_cloneInfo = DialogCloneInfo()
        self.dlg_cloneInfo.show()

    def auto_cal_incubation(self):
        self.DOR = self.ui.de_DOR.date().toPython()
        self.DOI = self.view_addInj.de_inj_DOI.date().toPython()
        self.duration = pendulum.instance(self.DOR) - pendulum.instance(self.DOI)
        self.view_addInj.lbl_incubated_disp.setText(f"{self.duration.in_weeks()}w{self.duration.remaining_days}d")

    def accept_adding_injection(self):
        """Build injection tree with conditional children based on user selections"""

        # ========== Gather Data ==========
        inj_mode = self.view_addInj.cb_InjectionModeCtrl.currentText()
        inj_side = self.view_addInj.cb_inj_side.currentText()
        injectate_type = self.view_addInj.cb_InjectateTypeCtrl.currentText()

        # Get injection mode abbreviation
        if inj_mode.lower() == "stereotaxic":
            mode_abbr = "ST"
        elif inj_mode.lower() == "retro-orbital":
            mode_abbr = "RO"
        else:
            mode_abbr = "ST"  # Default

        # ========== Build Injectate Info ==========
        if injectate_type == "SINGLE":
            clone_code = self.view_addInj.cb_clone_1.currentText()
            clone_construct = self.clone_dict[clone_code]
            serotype = self.view_addInj.cb_vector_1.currentText()

            injectate_short = f"{serotype}-{clone_code}"
            construction_full = f"{serotype}-{clone_construct}"

        else:  # MIXED
            clone_code_1 = self.view_addInj.cb_clone_1.currentText()
            clone_code_2 = self.view_addInj.cb_clone_2.currentText()
            clone_construct_1 = self.clone_dict[clone_code_1]
            clone_construct_2 = self.clone_dict[clone_code_2]
            serotype_1 = self.view_addInj.cb_vector_1.currentText()
            serotype_2 = self.view_addInj.cb_vector_2.currentText()

            injectate_short = f"{serotype_1}-{clone_code_1} + {serotype_2}-{clone_code_2}"
            construction_full = f"{serotype_1}-{clone_construct_1} + {serotype_2}-{clone_construct_2}"

        # ========== Create Parent Row ==========
        incubation_text = f"Incubated {self.duration.in_weeks()}w{self.duration.remaining_days}d"

        # Create parent font (14px, bold)
        parent_font = QFont()
        parent_font.setPointSize(12)
        parent_font.setBold(True)

        item_DOI = QStandardItem(self.DOI.strftime("%Y_%m_%d"))
        item_DOI.setFont(parent_font)
        item_DOI.setForeground(Qt.darkGreen)  # Green color for Injection History column

        item_summary = QStandardItem(f"{mode_abbr}_{inj_side}_{injectate_short} [{incubation_text}]")
        item_summary.setFont(parent_font)

        self.model.appendRow([item_DOI, item_summary])
        parent = item_DOI

        # ========== Add Children (Conditionally) ==========
        # Create child font for column 0 labels (bold, dark red)
        child_label_font = QFont()
        child_label_font.setBold(True)

        child_row = 0

        # 1. Construction (shown in one row for both SINGLE and MIXED)
        label_construction = QStandardItem("Construction")
        label_construction.setFont(child_label_font)
        label_construction.setForeground(QColor("#8A2BE2"))
        parent.setChild(child_row, 0, label_construction)
        parent.setChild(child_row, 1, QStandardItem(construction_full))
        child_row += 1

        # 2. Volume Per Shot (always shown)
        volume = self.view_addInj.le_volume_total.text() or "undefined"
        label_volume = QStandardItem("Volume Per Shot")
        label_volume.setFont(child_label_font)
        label_volume.setForeground(QColor("#8A2BE2"))
        parent.setChild(child_row, 0, label_volume)
        parent.setChild(child_row, 1, QStandardItem(volume))
        child_row += 1

        # 3. Mixing Ratio (only for MIXED)
        if injectate_type == "MIXED":
            ratio = self.view_addInj.cb_mixing_ratio.currentText()
            if ratio in ["", "--- Select Ratio ---"]:
                ratio = "undefined"

            label_ratio = QStandardItem("Mixing Ratio")
            label_ratio.setFont(child_label_font)
            label_ratio.setForeground(QColor("#8A2BE2"))
            parent.setChild(child_row, 0, label_ratio)
            parent.setChild(child_row, 1, QStandardItem(ratio))
            child_row += 1

        # 4. Coordinates (only for Stereotaxic, not Retro-orbital)
        if inj_mode.lower() == "stereotaxic":
            # Get number of sites
            num_of_sites = self.view_addInj.cb_num_of_sites.currentText()
            label_n_sites = QStandardItem("Number of Sites")
            label_n_sites.setFont(child_label_font)
            label_n_sites.setForeground(QColor("#8A2BE2"))
            parent.setChild(child_row, 0, label_n_sites)
            parent.setChild(child_row, 1, QStandardItem(num_of_sites))
            child_row += 1

            # Get coordinates
            dv = self.view_addInj.le_DV.text() or "undefined"
            ml = self.view_addInj.le_ML.text() or "undefined"
            ap = self.view_addInj.le_AP.text() or "undefined"

            coords = f"[DV, ML, AP] = [{dv}, {ml}, {ap}]"
            label_coords = QStandardItem("Coordinates")
            label_coords.setFont(child_label_font)
            label_coords.setForeground(QColor("#8A2BE2"))
            parent.setChild(child_row, 0, label_coords)
            parent.setChild(child_row, 1, QStandardItem(coords))
            child_row += 1

        # ========== Sort model by DOI (column 0, descending = newest first) ==========
        self.model.sort(0, Qt.DescendingOrder)

        # ========== Update TreeView ==========
        self.ui.tree_injections.setModel(self.model)
        self.view_addInj.close()

    def cancel_adding_injection(self):
        self.view_addInj.close()
