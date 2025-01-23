
SET dirPath=%CD%
SET venv=\.venv\Scripts\activate.bat
SET py=\main.py
SET venvPath=%dirPath%%venv%
SET pyPath=%dirPath%%py%

CALL %venvPath%
python %pyPath%