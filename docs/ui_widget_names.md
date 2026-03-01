# UI Widget Object Names

All widget object names sorted by prefix. **Updated to camelCase format.**

## Prefix Legend

| Prefix | Widget Type      |
|--------|------------------|
| bbox_  | QDialogButtonBox |
| btn_   | QPushButton      |
| cb_    | QComboBox        |
| chk_   | QCheckBox        |
| de_    | QDateEdit        |
| gb_    | QGroupBox        |
| lbl_   | QLabel           |
| le_    | QLineEdit        |
| lv_    | QListView        |
| pb_    | QProgressBar     |
| rb_    | QRadioButton     |
| sb_    | QSpinBox         |
| tb_    | QTextBrowser     |
| te_    | QTextEdit        |
| tree_  | QTreeView        |
| tv_    | QTableView       |

---

# Part 1: Widgets in Expdata Manager.ui

## Tab 0: Experiment Info

| Widget Name        | Type        | Description                    |
|--------------------|-------------|--------------------------------|
| de_dor             | QDateEdit   | Date of Recording              |
| de_dob             | QDateEdit   | Date of Birth                  |
| cb_acuc            | QComboBox   | ACUC Protocol                  |
| cb_species         | QComboBox   | Species                        |
| cb_genotype        | QComboBox   | Genotype                       |
| cb_sex             | QComboBox   | Sex                            |
| le_animalId        | QLineEdit   | Animal ID                      |
| le_ages            | QLineEdit   | Calculated ages                |
| le_project         | QLineEdit   | Project code                   |
| le_cuttingOS       | QLineEdit   | Cutting solution osmolarity    |
| le_holdingOS       | QLineEdit   | Holding solution osmolarity    |
| le_recordingOS     | QLineEdit   | Recording solution osmolarity  |
| btn_addInjections  | QPushButton | Add injection entry            |
| btn_rmInjections   | QPushButton | Remove selected injections     |
| btn_openExpDb      | QPushButton | Open experiment database       |
| btn_saveToExpDb    | QPushButton | Save to experiment database    |
| gb_expDbOp         | QGroupBox   | Experiment database operations |
| tree_injections    | QTreeView   | Injection history tree         |
| lbl_dor            | QLabel      | DOR label                      |
| lbl_dob            | QLabel      | DOB label                      |
| lbl_acuc           | QLabel      | ACUC label                     |
| lbl_species        | QLabel      | Species label                  |
| lbl_genotype       | QLabel      | Genotype label                 |
| lbl_sex            | QLabel      | Sex label                      |
| lbl_animalId       | QLabel      | Animal ID label                |
| lbl_ages           | QLabel      | Ages label                     |

## Tab 1: REC Writer

| Widget Name           | Type         | Description                    |
|-----------------------|--------------|--------------------------------|
| lbl_expDate           | QLabel       | Experiment date display        |
| btn_toggleBasic       | QPushButton  | Toggle basic parameters        |
| btn_toggleCustomized  | QPushButton  | Toggle customized parameters   |
| stack_parameters      | QStackedWidget | Parameter pages              |
| rb_10x                | QRadioButton | 10X objective                  |
| rb_40x                | QRadioButton | 40X objective                  |
| rb_60x                | QRadioButton | 60X objective                  |
| cb_exc                | QComboBox    | Excitation wavelength          |
| cb_emi                | QComboBox    | Emission filter                |
| cb_expoUnit           | QComboBox    | Exposure time unit             |
| cb_locType            | QComboBox    | Location type (Cell/Site)      |
| cb_side               | QComboBox    | Side (L/R)                     |
| cb_templateLoad       | QComboBox    | Template selector              |
| cb_recFiles           | QComboBox    | REC file selector              |
| sb_frames             | QSpinBox     | Number of frames               |
| sb_level              | QSpinBox     | LED level                      |
| sb_slice              | QSpinBox     | Slice number                   |
| sb_at                 | QSpinBox     | Cell/Site number               |
| le_expo               | QLineEdit    | Exposure time value            |
| le_fps                | QLineEdit    | Frames per second              |
| le_filenameSn         | QLineEdit    | TIFF filename with serial      |
| btn_templateSave      | QPushButton  | Save template                  |
| btn_templateDelete    | QPushButton  | Delete template                |
| btn_mvRowsUp          | QPushButton  | Move rows up                   |
| btn_mvRowsDown        | QPushButton  | Move rows down                 |
| btn_insertCustomProps | QPushButton  | Insert custom properties       |
| btn_rmSelectedRows    | QPushButton  | Remove selected rows           |
| btn_snInc             | QPushButton  | Increment serial number        |
| btn_snDec             | QPushButton  | Decrement serial number        |
| btn_snReset           | QPushButton  | Reset serial number            |
| btn_snCopy            | QPushButton  | Copy filename to clipboard     |
| btn_browseRecDir      | QPushButton  | Browse REC directory           |
| btn_generateTags      | QPushButton  | Generate tags from form        |
| btn_writeRec          | QPushButton  | Write REC file                 |
| tv_customized         | QTableView   | Customized parameters table    |
| te_recDir             | QTextEdit    | REC directory path             |
| te_tags               | QTextEdit    | Tag preview                    |
| lbl_obj               | QLabel       | Objective label                |
| lbl_exc               | QLabel       | Excitation label               |
| lbl_emi               | QLabel       | Emission label                 |
| lbl_expo              | QLabel       | Exposure label                 |
| lbl_fps               | QLabel       | FPS label                      |
| lbl_frames            | QLabel       | Frames label                   |
| lbl_level             | QLabel       | Level label                    |
| lbl_slice             | QLabel       | Slice label                    |
| lbl_side              | QLabel       | Side label                     |
| lbl_at                | QLabel       | AT label                       |
| lbl_recDir            | QLabel       | Directory label                |
| lbl_recFile           | QLabel       | Filename label                 |
| chk_addCustomized     | QCheckBox    | Append customized parameters   |

## Tab 2: ABF Note

| Widget Name           | Type         | Description                    |
|-----------------------|--------------|--------------------------------|
| gb_cellIdentity       | QGroupBox    | Cell identity section          |
| gb_cellParams         | QGroupBox    | Cell parameters section        |
| gb_protocolLog        | QGroupBox    | Protocol log section           |
| gb_recordingTracker   | QGroupBox    | Recording tracker section      |
| sb_abfSlice           | QSpinBox     | Slice number                   |
| sb_abfAt              | QSpinBox     | Cell/Site number               |
| cb_abfSide            | QComboBox    | Side (L/R)                     |
| cb_abfAtType          | QComboBox    | Cell/Site type                 |
| cb_currentAbf         | QComboBox    | Current ABF file               |
| le_abfRt              | QLineEdit    | Rt (total resistance)          |
| le_abfRm              | QLineEdit    | Rm (membrane resistance)       |
| le_abfCm              | QLineEdit    | Cm (membrane capacitance)      |
| le_abfRa              | QLineEdit    | Ra (access resistance)         |
| le_abfTau             | QLineEdit    | Tau (time constant)            |
| le_abfHold            | QLineEdit    | Holding potential              |
| le_abfProtocol        | QLineEdit    | Protocol name                  |
| le_currentImageSn     | QLineEdit    | Current image serial number    |
| btn_clearCellParams   | QPushButton  | Clear cell parameters          |
| btn_logCellParams     | QPushButton  | Log cell parameters            |
| btn_logProtocol       | QPushButton  | Log protocol                   |
| btn_toggleCellParams  | QPushButton  | Toggle cell params columns     |
| btn_deleteSelected    | QPushButton  | Delete selected rows           |
| btn_exportXlsx        | QPushButton  | Export to XLSX                 |
| btn_syncFromRecWriter | QPushButton  | Sync from REC Writer           |
| btn_abfInc            | QPushButton  | Next ABF file                  |
| btn_abfDec            | QPushButton  | Previous ABF file              |
| tv_abf                | QTableView   | ABF log table                  |
| lbl_abfSlice          | QLabel       | Slice label                    |
| lbl_abfSide           | QLabel       | Side label                     |
| lbl_abfAt             | QLabel       | At label                       |
| lbl_abfRt             | QLabel       | Rt label                       |
| lbl_abfRm             | QLabel       | Rm label                       |
| lbl_abfCm             | QLabel       | Cm label                       |
| lbl_abfRa             | QLabel       | Ra label                       |
| lbl_abfTau            | QLabel       | Tau label                      |
| lbl_abfHold           | QLabel       | Hold label                     |
| lbl_currentImageSN    | QLabel       | Current image SN label         |
| lbl_currentAbf        | QLabel       | Current ABF label              |

## Tab 3: REC Database

| Widget Name        | Type         | Description                    |
|--------------------|--------------|--------------------------------|
| gb_dbOperation     | QGroupBox    | Database operation section     |
| gb_dbDisplay       | QGroupBox    | Database display section       |
| tb_recDb           | QTextBrowser | Status text browser            |
| tv_recDb           | QTableView   | Database table view            |
| cb_recDbTable      | QComboBox    | Table name selector            |
| btn_importRecDb    | QPushButton  | Import REC files to database   |
| btn_loadRecTable   | QPushButton  | Load selected table            |
| btn_exportSummary  | QPushButton  | Export summary                 |
| btn_deleteTable    | QPushButton  | Delete table                   |
| lbl_tableName      | QLabel       | Table name label               |

## Tab 4: Concatenator

| Widget Name           | Type         | Description                    |
|-----------------------|--------------|--------------------------------|
| gb_tiffBrowser        | QGroupBox    | TIFF browser section           |
| gb_concat_status      | QGroupBox    | Concatenation status section   |
| lv_recFiles           | QListView    | REC files list                 |
| tb_concatenator       | QTextBrowser | Concatenation log              |
| pb_concatenation      | QProgressBar | Progress bar                   |
| btn_browseTiffs       | QPushButton  | Browse for TIFFs               |
| btn_startConcat       | QPushButton  | Start concatenation            |
| chk_includeSubfolders | QCheckBox    | Include subfolders             |
| chk_selectAllFiles    | QCheckBox    | Select all files               |

## System/Container Widgets

| Widget Name    | Type          |
|----------------|---------------|
| MainWindow     | QMainWindow   |
| centralwidget  | QWidget       |
| menubar        | QMenuBar      |
| statusbar      | QStatusBar    |
| tabs           | QTabWidget    |
| tab_EXP        | QWidget (tab) |
| tab_REC        | QWidget (tab) |
| tab_ABF        | QWidget (tab) |
| tab_REC_DB     | QWidget (tab) |
| tab_CONCAT     | QWidget (tab) |

---

# Part 2: Widgets Created in Python Files

## dialog_exp_db.py

| Widget Name         | Type         | Description                    |
|---------------------|--------------|--------------------------------|
| btn_loadToTab0      | QPushButton  | Load to Tab 0                  |
| btn_delete          | QPushButton  | Delete selected                |
| btn_exportSelected  | QPushButton  | Export selected                |
| btn_exportDatabases | QPushButton  | Export databases               |
| tv_basic            | QTableView   | Basic info table               |
| tv_injections       | QTableView   | Injection history table        |
| lbl_expList         | QLabel       | Experiment list label          |
| lbl_injHistory      | QLabel       | Injection history label        |

## view_add_inj.py (DialogInjManager)

| Widget Name          | Type              | Description                    |
|----------------------|-------------------|--------------------------------|
| buttonBox            | QDialogButtonBox  | OK/Cancel buttons              |
| btn_cloneInfo        | QAction           | Clone info action              |
| btn_refresh_clone_1  | QPushButton       | Refresh clone 1 menu           |
| btn_refresh_clone_2  | QPushButton       | Refresh clone 2 menu           |
| cb_InjectionModeCtrl | QComboBox         | Injection mode control         |
| cb_InjectateTypeCtrl | QComboBox         | Injectate type control         |
| cb_clone_1           | QComboBox         | Clone 1 selector               |
| cb_clone_2           | QComboBox         | Clone 2 selector               |
| cb_vector_1          | QComboBox         | Vector 1 selector              |
| cb_vector_2          | QComboBox         | Vector 2 selector              |
| cb_inj_side          | QComboBox         | Injection side                 |
| cb_mixing_ratio      | QComboBox         | Mixing ratio                   |
| cb_num_of_sites      | QComboBox         | Number of sites                |
| de_inj_DOI           | QDateEdit         | Date of Injection              |
| le_volume_total      | QLineEdit         | Volume per shot                |
| le_DV                | QLineEdit         | DV coordinate                  |
| le_ML                | QLineEdit         | ML coordinate                  |
| le_AP                | QLineEdit         | AP coordinate                  |
| lbl_incubated_disp   | QLabel            | Incubation period display      |

## dialog_save_template.py

| Widget Name | Type             | Description                    |
|-------------|------------------|--------------------------------|
| buttonBox   | QDialogButtonBox | OK/Cancel buttons              |
| le_filename | QLineEdit        | Template filename              |
| lbl_message | QLabel           | Message label                  |

## dialog_confirm.py

| Widget Name | Type             | Description                    |
|-------------|------------------|--------------------------------|
| buttonBox   | QDialogButtonBox | Yes/No buttons                 |
| lbl_message | QLabel           | Confirmation message           |
| le_passcode | QLineEdit        | Passcode input (for protected) |
| lbl_passcode| QLabel           | Passcode label                 |

## dialog_insert_props.py

| Widget Name    | Type         | Description                    |
|----------------|--------------|--------------------------------|
| btn_addRow     | QPushButton  | Add row                        |
| btn_rmRow      | QPushButton  | Remove row                     |
| btn_ok         | QPushButton  | OK button                      |
| btn_cancel     | QPushButton  | Cancel button                  |
| lbl_properties | QLabel       | Properties label               |
| lbl_values     | QLabel       | Values label                   |

## dialog_clone_info.py

| Widget Name  | Type             | Description                    |
|--------------|------------------|--------------------------------|
| buttonBox    | QDialogButtonBox | Close button                   |
| tv_cloneInfo | QTableView       | Clone info table               |

---

**Naming Convention:** `prefix_camelCaseName`
- Prefix indicates widget type (btn_, cb_, le_, etc.)
- Name uses camelCase starting with lowercase
- Examples: `btn_saveToDb`, `cb_templateLoad`, `le_filenameSn`
