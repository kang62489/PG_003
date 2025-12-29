# UI Widget Object Names

All widget object names in Expdata Manager.ui sorted by prefix.

## Prefix Legend

| Prefix | Widget Type  |
|--------|--------------|
| btn_   | QPushButton  |
| cb_    | QComboBox    |
| chk_   | QCheckBox    |
| de_    | QDateEdit    |
| gb_    | QGroupBox    |
| lbl_   | QLabel       |
| le_    | QLineEdit    |
| lv_    | QListView    |
| pb_    | QProgressBar |
| rb_    | QRadioButton |
| sb_    | QSpinBox     |
| tb_    | QTextBrowser |
| te_    | QTextEdit    |
| tree_  | QTreeView    |
| tv_    | QTableView   |

---

## btn_ - QPushButton (25)

| Name                           | Connected Function           | Used In              |
|--------------------------------|------------------------------|----------------------|
| btn_AddAbf                     | -                            | -                    |
| btn_AddInjections              | add_injections               | ctrl_exp_info.py     |
| btn_BrowseRecDir               | browse_rec_dir               | ctrl_rec_writer.py   |
| btn_DeleteTable                | delete_table                 | ctrl_rec_import.py   |
| btn_ExportSummary              | export_summary               | ctrl_rec_import.py   |
| btn_ImportRecDb                | import_recDB                 | ctrl_rec_import.py   |
| btn_InsertCustomizedProperties | insert_customized_properties | ctrl_rec_writer.py   |
| btn_LoadRecTable               | load_rec_table               | ctrl_rec_import.py   |
| btn_MvRowsDown                 | mv_rows_down                 | ctrl_rec_writer.py   |
| btn_MvRowsUp                   | mv_rows_up                   | ctrl_rec_writer.py   |
| btn_OpenExpDb                  | open_exp_db                  | ctrl_exp_info.py     |
| btn_ReadRec                    | read_rec                     | ctrl_rec_writer.py   |
| btn_RevertRec                  | revert_rec                   | ctrl_rec_writer.py   |
| btn_RmInjections               | rm_injections                | ctrl_exp_info.py     |
| btn_RmSelectedRows             | rm_selected_rows             | ctrl_rec_writer.py   |
| btn_SaveToDb                   | save_to_DB                   | ctrl_exp_info.py     |
| btn_SnCopy                     | sn_copy                      | ctrl_rec_writer.py   |
| btn_SnDec                      | sn_dec                       | ctrl_rec_writer.py   |
| btn_SnInc                      | sn_inc                       | ctrl_rec_writer.py   |
| btn_SnReset                    | sn_reset                     | ctrl_rec_writer.py   |
| btn_TemplateDelete             | template_delete              | ctrl_rec_writer.py   |
| btn_TemplateSave               | template_save                | ctrl_rec_writer.py   |
| btn_WriteRec                   | write_rec                    | ctrl_rec_writer.py   |
| btn_browse_tiffs*              | browse_tiffs                 | ctrl_tiff_stacker.py |
| btn_start_concatenation*       | start_concatenation          | ctrl_tiff_stacker.py |

## cb_ - QComboBox (14)

| Name             | Connected Function                 | Used In                            |
|------------------|------------------------------------|------------------------------------|
| cb_ABF_FILENAME  | -                                  | -                                  |
| cb_ABF_MODE      | -                                  | -                                  |
| cb_ACUC          | -                                  | view_exp_info.py, ctrl_exp_info.py |
| cb_CAM_TRIG_MODE | update_tag_output                  | ctrl_rec_writer.py                 |
| cb_EMI           | update_tag_output                  | ctrl_rec_writer.py                 |
| cb_EXC           | update_tag_output, auto_select_emi | ctrl_rec_writer.py                 |
| cb_EXP_DB_TABLE  | -                                  | ctrl_exp_info.py                   |
| cb_EXPO_UNIT     | update_tag_output                  | ctrl_rec_writer.py                 |
| cb_GENOTYPE      | -                                  | view_exp_info.py, ctrl_exp_info.py |
| cb_LOC_TYPE      | update_tag_output                  | ctrl_rec_writer.py                 |
| cb_REC_DB_TABLE  | -                                  | ctrl_rec_import.py                 |
| cb_SEX           | -                                  | view_exp_info.py, ctrl_exp_info.py |
| cb_SPECIES       | -                                  | view_exp_info.py, ctrl_exp_info.py |
| cb_TemplateLoad  | template_load                      | ctrl_rec_writer.py                 |

## chk_ - QCheckBox (3)

| Name                   | Connected Function | Used In              |
|------------------------|--------------------|----------------------|
| chk_addCustomized      | update_tag_output  | ctrl_rec_writer.py   |
| chk_includeSubfolders* | -                  | ctrl_tiff_stacker.py |
| chk_selectAllFiles*    | select_all_files   | ctrl_tiff_stacker.py |

## de_ - QDateEdit (2)

| Name   | Connected Function | Used In                                             |
|--------|--------------------|-----------------------------------------------------|
| de_DOB | auto_calculation   | view_exp_info.py, ctrl_exp_info.py                  |
| de_DOR | auto_calculation   | view_exp_info.py, ctrl_exp_info.py, ctrl_add_inj.py |

## gb_ - QGroupBox (15)

| Name              | Used In              |
|-------------------|----------------------|
| gb_animals        | view_exp_info.py     |
| gb_basics         | view_exp_info.py     |
| gb_concat_status* | view_tiff_stacker.py |
| gb_dbDisplay      | -                    |
| gb_dbOperation    | -                    |
| gb_fileIO         | view_exp_info.py     |
| gb_injections     | view_exp_info.py     |
| gb_recBasic       | view_rec_writer.py   |
| gb_recCustomized  | view_rec_writer.py   |
| gb_recDB_status   | view_rec_import.py   |
| gb_solutions      | view_exp_info.py     |
| gb_status         | view_rec_writer.py   |
| gb_tagOutput      | view_rec_writer.py   |
| gb_tagPreview     | -                    |
| gb_tiffBrowser*   | ctrl_tiff_stacker.py |

## lbl_ - QLabel (27)

| Name                | Used In            |
|---------------------|--------------------|
| lbl_ACUC            | -                  |
| lbl_AT              | -                  |
| lbl_CAM_TRIG_MODE   | view_rec_writer.py |
| lbl_DOB             | -                  |
| lbl_DOR             | -                  |
| lbl_EMI             | view_rec_writer.py |
| lbl_EXC             | view_rec_writer.py |
| lbl_EXPO            | view_rec_writer.py |
| lbl_FPS             | view_rec_writer.py |
| lbl_FRAMES          | view_rec_writer.py |
| lbl_LEVEL           | view_rec_writer.py |
| lbl_OBJ             | view_rec_writer.py |
| lbl_SLICE           | view_rec_writer.py |
| lbl_abfCell         | -                  |
| lbl_abfCm           | -                  |
| lbl_abfFilename     | -                  |
| lbl_abfHold         | -                  |
| lbl_abfMode         | -                  |
| lbl_abfProtocol     | -                  |
| lbl_abfProtocolVal  | -                  |
| lbl_abfRa           | -                  |
| lbl_abfRm           | -                  |
| lbl_abfRtBath       | -                  |
| lbl_abfSlice        | -                  |
| lbl_abfTau          | -                  |
| lbl_abfTimestamp    | -                  |
| lbl_abfTimestampVal | -                  |
| lbl_ages            | ctrl_exp_info.py   |
| lbl_agesLabel       | -                  |
| lbl_animalID        | -                  |
| lbl_cuttingOS       | -                  |
| lbl_genotype        | -                  |
| lbl_holdingOS       | -                  |
| lbl_project         | -                  |
| lbl_recDir          | ctrl_rec_writer.py |
| lbl_recordingOS     | -                  |
| lbl_serialName_2    | -                  |
| lbl_sex             | -                  |
| lbl_species         | -                  |
| lbl_tableName       | -                  |

## le_ - QLineEdit (20)

| Name             | Connected Function | Used In                                |
|------------------|--------------------|----------------------------------------|
| le_EXPO          | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| le_FPS           | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| le_FRAMES        | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| le_LEVEL         | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| le_abfCell       | -                  | -                                      |
| le_abfCm         | -                  | -                                      |
| le_abfHold       | -                  | -                                      |
| le_abfRa         | -                  | -                                      |
| le_abfRm         | -                  | -                                      |
| le_abfRtBath     | -                  | -                                      |
| le_abfSlice      | -                  | -                                      |
| le_abfTau        | -                  | -                                      |
| le_animalID      | -                  | view_exp_info.py, ctrl_exp_info.py     |
| le_cuttingOS     | -                  | view_exp_info.py, ctrl_exp_info.py     |
| le_experimenters | -                  | ctrl_exp_info.py                       |
| le_filenameSN    | sn_validate        | ctrl_rec_writer.py, view_rec_writer.py |
| le_holdingOS     | -                  | view_exp_info.py, ctrl_exp_info.py     |
| le_project       | -                  | view_exp_info.py                       |
| le_recDir        | validate_rec_dir   | ctrl_rec_writer.py, view_rec_writer.py |
| le_recordingOS   | -                  | view_exp_info.py, ctrl_exp_info.py     |

## lv_ - QListView (1)

| Name         | Connected Function | Used In                                    |
|--------------|--------------------|--------------------------------------------|
| lv_recFiles* | -                  | ctrl_tiff_stacker.py, view_tiff_stacker.py |

## pb_ - QProgressBar (1)

| Name              | Connected Function | Used In              |
|-------------------|--------------------|----------------------|
| pb_concatenation* | -                  | ctrl_tiff_stacker.py |

## rb_ - QRadioButton (3)

| Name   | Connected Function | Used In            |
|--------|--------------------|--------------------|
| rb_10X | update_tag_output  | view_rec_writer.py |
| rb_40X | update_tag_output  | view_rec_writer.py |
| rb_60X | update_tag_output  | view_rec_writer.py |

## sb_ - QSpinBox (2)

| Name     | Connected Function | Used In                                |
|----------|--------------------|----------------------------------------|
| sb_AT    | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| sb_SLICE | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |

## tb_ - QTextBrowser (3)

| Name             | Used In              |
|------------------|----------------------|
| tb_concatenator* | ctrl_tiff_stacker.py |
| tb_recDB         | ctrl_rec_import.py   |
| tb_status        | ctrl_rec_writer.py   |

## te_ - QTextEdit (1)

| Name    | Connected Function | Used In            |
|---------|--------------------|--------------------|
| te_tags | update_tag_output  | ctrl_rec_writer.py |

## tree_ - QTreeView (1)

| Name            | Connected Function | Used In                                             |
|-----------------|--------------------|-----------------------------------------------------|
| tree_injections | rm_injections      | view_exp_info.py, ctrl_exp_info.py, ctrl_add_inj.py |

## tv_ - QTableView (3)

| Name          | Used In                                |
|---------------|----------------------------------------|
| tv_abf        | -                                      |
| tv_customized | view_rec_writer.py, ctrl_rec_writer.py |
| tv_recDB      | view_rec_import.py, ctrl_rec_import.py |

## Other - System/Container Widgets

| Name          | Type          |
|---------------|---------------|
| MainWindow    | QMainWindow   |
| centralwidget | QWidget       |
| menubar       | QMenuBar      |
| statusbar     | QStatusBar    |
| tabs          | QTabWidget    |
| tab_ABF       | QWidget (tab) |
| tab_EXP       | QWidget (tab) |
| tab_REC       | QWidget (tab) |
| tab_REC_DB    | QWidget (tab) |

---

**Total: 97 named widgets in UI file + 9 system widgets**

*Widgets marked with asterisk are planned for future TIFF Stacker tab (not yet in UI file)*
