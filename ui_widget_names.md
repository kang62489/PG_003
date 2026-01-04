# UI Widget Object Names

All widget object names sorted by prefix.

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

## btn_ - QPushButton (25)

| #  | Name                           | Connected Function           | Used In              |
|----|--------------------------------|------------------------------|----------------------|
| 1  | btn_AddAbf                     | -                            | -                    |
| 2  | btn_AddInjections              | add_injections               | ctrl_exp_info.py     |
| 3  | btn_browseRecDir               | browse_rec_dir               | ctrl_rec_writer.py   |
| 4  | btn_deleteTable                | delete_table                 | ctrl_rec_import.py   |
| 5  | btn_exportSummary              | export_summary               | ctrl_rec_import.py   |
| 6  | btn_importRecDb                | import_rec_db                | ctrl_rec_import.py   |
| 7  | btn_insertCustomProps          | insert_custom_props          | ctrl_rec_writer.py   |
| 8  | btn_loadRecTable               | load_rec_table               | ctrl_rec_import.py   |
| 9  | btn_mvRowsDown                 | mv_rows_down                 | ctrl_rec_writer.py   |
| 10 | btn_mvRowsUp                   | mv_rows_up                   | ctrl_rec_writer.py   |
| 11 | btn_OpenExpDb                  | open_exp_db                  | ctrl_exp_info.py     |
| 12 | btn_ReadRec                    | read_rec                     | ctrl_rec_writer.py   |
| 13 | btn_RevertRec                  | revert_rec                   | ctrl_rec_writer.py   |
| 14 | btn_RmInjections               | rm_injections                | ctrl_exp_info.py     |
| 15 | btn_rmSelectedRows             | rm_selected_rows             | ctrl_rec_writer.py   |
| 16 | btn_SaveToDb                   | save_to_db                   | ctrl_exp_info.py     |
| 17 | btn_snCopy                     | sn_copy                      | ctrl_rec_writer.py   |
| 18 | btn_snDec                      | sn_dec                       | ctrl_rec_writer.py   |
| 19 | btn_snInc                      | sn_inc                       | ctrl_rec_writer.py   |
| 20 | btn_snReset                    | sn_reset                     | ctrl_rec_writer.py   |
| 21 | btn_templateDelete             | template_delete              | ctrl_rec_writer.py   |
| 22 | btn_templateSave               | template_save                | ctrl_rec_writer.py   |
| 23 | btn_writeRec                   | write_rec                    | ctrl_rec_writer.py   |
| 24 | btn_browseTiffs*               | browse_tiffs                 | ctrl_tiff_stacker.py |
| 25 | btn_startConcat*               | start_concat                 | ctrl_tiff_stacker.py |

## cb_ - QComboBox (14)

| #  | Name             | Connected Function                 | Used In                            |
|----|------------------|------------------------------------|------------------------------------|
| 26 | cb_ABF_FILENAME  | -                                  | -                                  |
| 27 | cb_ABF_MODE      | -                                  | -                                  |
| 28 | cb_ACUC          | -                                  | view_exp_info.py, ctrl_exp_info.py |
| 29 | cb_CAM_TRIG_MODE | update_tag_output                  | ctrl_rec_writer.py                 |
| 30 | cb_emi           | update_tag_output                  | ctrl_rec_writer.py                 |
| 31 | cb_exc           | update_tag_output, auto_select_emi | ctrl_rec_writer.py                 |
| 32 | cb_EXP_DB_TABLE  | -                                  | ctrl_exp_info.py                   |
| 33 | cb_expoUnit      | update_tag_output                  | ctrl_rec_writer.py                 |
| 34 | cb_GENOTYPE      | -                                  | view_exp_info.py, ctrl_exp_info.py |
| 35 | cb_locType       | update_tag_output                  | ctrl_rec_writer.py                 |
| 36 | cb_recDbTable    | -                                  | ctrl_rec_import.py                 |
| 37 | cb_SEX           | -                                  | view_exp_info.py, ctrl_exp_info.py |
| 38 | cb_SPECIES       | -                                  | view_exp_info.py, ctrl_exp_info.py |
| 39 | cb_templateLoad  | template_load                      | ctrl_rec_writer.py                 |

## chk_ - QCheckBox (3)
todo: 1. 40 -> chk_screaming_snake_case 2. 41 -> chk_IncludeSubDirs 3. 42 -> fix to pascal case

| #  | Name                   | Connected Function | Used In              |
|----|------------------------|--------------------|----------------------|
| 40 | chk_addCustomized      | update_tag_output  | ctrl_rec_writer.py   |
| 41 | chk_includeSubfolders* | -                  | ctrl_tiff_stacker.py |
| 42 | chk_selectAllFiles*    | select_all_files   | ctrl_tiff_stacker.py |

## de_ - QDateEdit (2)

| #  | Name   | Connected Function | Used In                                             |
|----|--------|--------------------|-----------------------------------------------------|
| 43 | de_DOB | auto_calculation   | view_exp_info.py, ctrl_exp_info.py                  |
| 44 | de_DOR | auto_calculation   | view_exp_info.py, ctrl_exp_info.py, ctrl_add_inj.py |

## gb_ - QGroupBox (15)

| #  | Name              | Used In              |
|----|-------------------|----------------------|
| 45 | gb_animals        | view_exp_info.py     |
| 46 | gb_basics         | view_exp_info.py     |
| 47 | gb_concat_status* | view_tiff_stacker.py |
| 48 | gb_dbDisplay      | -                    |
| 49 | gb_dbOperation    | -                    |
| 50 | gb_fileIO         | view_exp_info.py     |
| 51 | gb_injections     | view_exp_info.py     |
| 52 | gb_recBasic       | view_rec_writer.py   |
| 53 | gb_recCustomized  | view_rec_writer.py   |
| 54 | gb_recDB_status   | view_rec_import.py   |
| 55 | gb_solutions      | view_exp_info.py     |
| 56 | gb_status         | view_rec_writer.py   |
| 57 | gb_tagOutput      | view_rec_writer.py   |
| 58 | gb_tagPreview     | -                    |
| 59 | gb_tiffBrowser*   | ctrl_tiff_stacker.py |

## lbl_ - QLabel (27)

| #  | Name                | Used In            |
|----|---------------------|--------------------|
| 60 | lbl_ACUC            | -                  |
| 61 | lbl_AT              | -                  |
| 62 | lbl_CAM_TRIG_MODE   | view_rec_writer.py |
| 63 | lbl_DOB             | -                  |
| 64 | lbl_DOR             | -                  |
| 65 | lbl_EMI             | view_rec_writer.py |
| 66 | lbl_EXC             | view_rec_writer.py |
| 67 | lbl_EXPO            | view_rec_writer.py |
| 68 | lbl_FPS             | view_rec_writer.py |
| 69 | lbl_FRAMES          | view_rec_writer.py |
| 70 | lbl_LEVEL           | view_rec_writer.py |
| 71 | lbl_OBJ             | view_rec_writer.py |
| 72 | lbl_SLICE           | view_rec_writer.py |
| 73 | lbl_abfCell         | -                  |
| 74 | lbl_abfCm           | -                  |
| 75 | lbl_abfFilename     | -                  |
| 76 | lbl_abfHold         | -                  |
| 77 | lbl_abfMode         | -                  |
| 78 | lbl_abfProtocol     | -                  |
| 79 | lbl_abfProtocolVal  | -                  |
| 80 | lbl_abfRa           | -                  |
| 81 | lbl_abfRm           | -                  |
| 82 | lbl_abfRtBath       | -                  |
| 83 | lbl_abfSlice        | -                  |
| 84 | lbl_abfTau          | -                  |
| 85 | lbl_abfTimestamp    | -                  |
| 86 | lbl_abfTimestampVal | -                  |
| 87 | lbl_ages            | ctrl_exp_info.py   |
| 88 | lbl_agesLabel       | -                  |
| 89 | lbl_animalID        | -                  |
| 90 | lbl_cuttingOS       | -                  |
| 91 | lbl_genotype        | -                  |
| 92 | lbl_holdingOS       | -                  |
| 93 | lbl_project         | -                  |
| 94 | lbl_recDir          | ctrl_rec_writer.py |
| 95 | lbl_recordingOS     | -                  |
| 96 | lbl_serialName_2    | -                  |
| 97 | lbl_sex             | -                  |
| 98 | lbl_species         | -                  |
| 99 | lbl_tableName       | -                  |

## le_ - QLineEdit (20)

| #   | Name             | Connected Function | Used In                                |
|-----|------------------|--------------------|----------------------------------------|
| 100 | le_expo          | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| 101 | le_fps           | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| 102 | le_FRAMES        | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| 103 | le_LEVEL         | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| 104 | le_abfCell       | -                  | -                                      |
| 105 | le_abfCm         | -                  | -                                      |
| 106 | le_abfHold       | -                  | -                                      |
| 107 | le_abfRa         | -                  | -                                      |
| 108 | le_abfRm         | -                  | -                                      |
| 109 | le_abfRtBath     | -                  | -                                      |
| 110 | le_abfSlice      | -                  | -                                      |
| 111 | le_abfTau        | -                  | -                                      |
| 112 | le_animalID      | -                  | view_exp_info.py, ctrl_exp_info.py     |
| 113 | le_cuttingOS     | -                  | view_exp_info.py, ctrl_exp_info.py     |
| 114 | le_experimenters | -                  | ctrl_exp_info.py                       |
| 115 | le_filenameSn    | sn_validate        | ctrl_rec_writer.py, view_rec_writer.py |
| 116 | le_holdingOS     | -                  | view_exp_info.py, ctrl_exp_info.py     |
| 117 | le_project       | -                  | view_exp_info.py                       |
| 118 | le_recDir        | validate_rec_dir   | ctrl_rec_writer.py, view_rec_writer.py |
| 119 | le_recordingOS   | -                  | view_exp_info.py, ctrl_exp_info.py     |

## lv_ - QListView (1)

| #   | Name         | Connected Function | Used In                                    |
|-----|--------------|--------------------|--------------------------------------------|
| 120 | lv_recFiles* | -                  | ctrl_tiff_stacker.py, view_tiff_stacker.py |

## pb_ - QProgressBar (1)

| #   | Name              | Connected Function | Used In              |
|-----|-------------------|--------------------|----------------------|
| 121 | pb_concatenation* | -                  | ctrl_tiff_stacker.py |

## rb_ - QRadioButton (3)

| #   | Name   | Connected Function | Used In            |
|-----|--------|--------------------|--------------------|
| 122 | rb_10x | update_tag_output  | view_rec_writer.py |
| 123 | rb_40x | update_tag_output  | view_rec_writer.py |
| 124 | rb_60x | update_tag_output  | view_rec_writer.py |

## sb_ - QSpinBox (2)

| #   | Name     | Connected Function | Used In                                |
|-----|----------|--------------------|----------------------------------------|
| 125 | sb_at    | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |
| 126 | sb_slice | update_tag_output  | ctrl_rec_writer.py, view_rec_writer.py |

## tb_ - QTextBrowser (3)

| #   | Name             | Used In              |
|-----|------------------|----------------------|
| 127 | tb_concatenator* | ctrl_tiff_stacker.py |
| 128 | tb_recDb         | ctrl_rec_import.py   |
| 129 | tb_status        | ctrl_rec_writer.py   |

## te_ - QTextEdit (1)

| #   | Name    | Connected Function | Used In            |
|-----|---------|--------------------|--------------------|
| 130 | te_tags | update_tag_output  | ctrl_rec_writer.py |

## tree_ - QTreeView (1)

| #   | Name            | Connected Function | Used In                                             |
|-----|-----------------|--------------------|-----------------------------------------------------|
| 131 | tree_injections | rm_injections      | view_exp_info.py, ctrl_exp_info.py, ctrl_add_inj.py |

## tv_ - QTableView (3)

| #   | Name          | Used In                                |
|-----|---------------|----------------------------------------|
| 132 | tv_abf        | -                                      |
| 133 | tv_customized | view_rec_writer.py, ctrl_rec_writer.py |
| 134 | tv_recDb      | view_rec_import.py, ctrl_rec_import.py |

## Other - System/Container Widgets

| #   | Name          | Type          |
|-----|---------------|---------------|
| 135 | MainWindow    | QMainWindow   |
| 136 | centralwidget | QWidget       |
| 137 | menubar       | QMenuBar      |
| 138 | statusbar     | QStatusBar    |
| 139 | tabs          | QTabWidget    |
| 140 | tab_ABF       | QWidget (tab) |
| 141 | tab_EXP       | QWidget (tab) |
| 142 | tab_REC       | QWidget (tab) |
| 143 | tab_REC_DB    | QWidget (tab) |

---

# Part 2: Widgets Created in Python Files

## bbox_ - QDialogButtonBox (5)

| #   | Name      | Connected Function      | Used In                 |
|-----|-----------|-------------------------|-------------------------|
| 144 | buttonBox | accept_inj, cancel_inj  | view_add_inj.py         |
| 145 | buttonBox | accept                  | dialog_clone_info.py    |
| 146 | buttonBox | accept, reject          | dialog_save_template.py |
| 147 | buttonBox | accept, reject          | dialog_confirm.py       |
| 148 | buttonBox | check_passcode, reject  | dialog_confirm.py       |

## btn_ - QPushButton/QAction (11)

| #   | Name                 | Connected Function  | Used In                |
|-----|----------------------|---------------------|------------------------|
| 149 | btn_addRow           | add_row             | dialog_insert_props.py |
| 150 | btn_cancel           | cancel              | dialog_insert_props.py |
| 151 | btn_cloneInfo        | show_clone_info     | view_add_inj.py        |
| 152 | btn_delete           | delete              | dialog_exp_db.py       |
| 153 | btn_exportDatabases  | export_databases    | dialog_exp_db.py       |
| 154 | btn_exportSelected   | export_selected     | dialog_exp_db.py       |
| 155 | btn_loadToTab0       | load_to_tab0        | dialog_exp_db.py       |
| 156 | btn_ok               | ok                  | dialog_insert_props.py |
| 157 | btn_refresh_clone_1  | refresh_clone_menus | view_add_inj.py        |
| 158 | btn_refresh_clone_2  | refresh_clone_menus | view_add_inj.py        |
| 159 | btn_rmRow            | rm_row              | dialog_insert_props.py |

## cb_ - QComboBox (9)

| #   | Name                 | Connected Function  | Used In         |
|-----|----------------------|---------------------|-----------------|
| 160 | cb_clone_1           | -                   | view_add_inj.py |
| 161 | cb_clone_2           | -                   | view_add_inj.py |
| 162 | cb_inj_side          | -                   | view_add_inj.py |
| 163 | cb_InjectionModeCtrl | injection_mode_ctrl | view_add_inj.py |
| 164 | cb_InjectateTypeCtrl | injectate_type_ctrl | view_add_inj.py |
| 165 | cb_mixing_ratio      | -                   | view_add_inj.py |
| 166 | cb_num_of_sites      | -                   | view_add_inj.py |
| 167 | cb_vector_1          | -                   | view_add_inj.py |
| 168 | cb_vector_2          | -                   | view_add_inj.py |

## de_ - QDateEdit (1)

| #   | Name       | Connected Function  | Used In         |
|-----|------------|---------------------|-----------------|
| 169 | de_inj_DOI | auto_cal_incubation | view_add_inj.py |

## lbl_ - QLabel (20)

| #   | Name               | Used In                 |
|-----|--------------------|-------------------------|
| 170 | lbl_clone_1        | view_add_inj.py         |
| 171 | lbl_clone_2        | view_add_inj.py         |
| 172 | lbl_coordinate     | view_add_inj.py         |
| 173 | lbl_expList        | dialog_exp_db.py        |
| 174 | lbl_incubated      | view_add_inj.py         |
| 175 | lbl_incubated_disp | view_add_inj.py         |
| 176 | lbl_inj_DOI        | view_add_inj.py         |
| 177 | lbl_injHistory     | dialog_exp_db.py        |
| 178 | lbl_inj_mode       | view_add_inj.py         |
| 179 | lbl_inj_side       | view_add_inj.py         |
| 180 | lbl_injectate_type | view_add_inj.py         |
| 181 | lbl_message        | dialog_save_template.py |
| 182 | lbl_message        | dialog_confirm.py       |
| 183 | lbl_mixing_ratio   | view_add_inj.py         |
| 184 | lbl_passcode       | dialog_confirm.py       |
| 185 | lbl_properties     | dialog_insert_props.py  |
| 186 | lbl_values         | dialog_insert_props.py  |
| 187 | lbl_vector_1       | view_add_inj.py         |
| 188 | lbl_vector_2       | view_add_inj.py         |
| 189 | lbl_volume_per_shot| view_add_inj.py         |

## le_ - QLineEdit (6)

| #   | Name            | Connected Function | Used In                 |
|-----|-----------------|--------------------|-------------------------|
| 190 | le_AP           | -                  | view_add_inj.py         |
| 191 | le_DV           | -                  | view_add_inj.py         |
| 192 | le_filename     | -                  | dialog_save_template.py |
| 193 | le_ML           | -                  | view_add_inj.py         |
| 194 | le_passcode     | -                  | dialog_confirm.py       |
| 195 | le_volume_total | -                  | view_add_inj.py         |

## tv_ - QTableView (3)

| #   | Name          | Used In              |
|-----|---------------|----------------------|
| 196 | tv_basic      | dialog_exp_db.py     |
| 197 | tv_cloneInfo  | dialog_clone_info.py |
| 198 | tv_injections | dialog_exp_db.py     |

---

**Summary:**
- Part 1 (UI file): 134 widgets + 9 system widgets = 143
- Part 2 (Python files): 55 widgets (including 5 bbox_ needing rename)
- **Grand Total: 198 widgets**

*Widgets marked with asterisk are planned for future TIFF Stacker tab (not yet in UI file)*
