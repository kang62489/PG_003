SET dirPath=%CD%
SET venvPath="%dirPath%\.venv\Scripts\activate.bat"
SET pyPath="%dirPath%\.venv\Scripts\python.exe"
SET progPath="%dirPath%\main.py"

CALL %venvPath%
%pyPath% %progPath%