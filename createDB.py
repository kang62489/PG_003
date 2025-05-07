"""Create an initial database of (expInfo.db)"""
# Modules
import sqlite3
from tabulate import tabulate
import pandas as pd
from rich import print
from util.constants import MODELS_DIR

# Connect to a database
# conn = sqlite3.connect(MODELS_DIR / "expInfo.db")
conn = sqlite3.connect(MODELS_DIR / "records.db")

# Create a cursor for database operations
cursor = conn.cursor()

## Dangerous code
# cursor.execute("DROP TABLE IF EXISTS ACh_Dynamics")

## Create a table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS ACh_Dynamics (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         DOR TEXT,
#         Experimenters TEXT,
#         ACUC_Protocol TEXT,
#         Animal_ID TEXT,
#         Species TEXT,
#         Genotype TEXT,
#         Sex TEXT,
#         DOB TEXT,
#         Ages TEXT,
#         DOI TEXT,
#         Incubation TEXT,
#         CuttingOS TEXT,
#         HoldingOS TEXT,
#         RecordingOS TEXT,
#         Enable_R TEXT,
#         Enable_L TEXT,
#         Inj_Volume_R TEXT,
#         Inj_Volume_Unit_R TEXT,
#         Inj_Mode_R TEXT,
#         Inj_Coord_DV_R TEXT,
#         Inj_Coord_AP_R TEXT,
#         Inj_Coord_ML_R TEXT,
#         Inj_virus_R TEXT,
#         Inj_Volume_L TEXT,
#         Inj_Volume_Unit_L TEXT,
#         Inj_Mode_L TEXT,
#         Inj_Coord_DV_L TEXT,
#         Inj_Coord_AP_L TEXT,
#         Inj_Coord_ML_L TEXT,
#         Inj_virus_L TEXT
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS ACh_Sensor_Specificity (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         DOR TEXT,
#         Experimenters TEXT,
#         ACUC_Protocol TEXT,
#         Animal_ID TEXT,
#         Species TEXT,
#         Genotype TEXT,
#         Sex TEXT,
#         DOB TEXT,
#         Ages TEXT,
#         DOI TEXT,
#         Incubation TEXT,
#         CuttingOS TEXT,
#         HoldingOS TEXT,
#         RecordingOS TEXT,
#         Enable_R TEXT,
#         Enable_L TEXT,
#         Inj_Volume_R TEXT,
#         Inj_Volume_Unit_R TEXT,
#         Inj_Mode_R TEXT,
#         Inj_Coord_DV_R TEXT,
#         Inj_Coord_AP_R TEXT,
#         Inj_Coord_ML_R TEXT,
#         Inj_virus_R TEXT,
#         Inj_Volume_L TEXT,
#         Inj_Volume_Unit_L TEXT,
#         Inj_Mode_L TEXT,
#         Inj_Coord_DV_L TEXT,
#         Inj_Coord_AP_L TEXT,
#         Inj_Coord_ML_L TEXT,
#         Inj_virus_L TEXT
#     )
# ''')

# # 

# conn.commit()
conn.close()



