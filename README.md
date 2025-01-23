---
Established: 2025-01-22
Last Updated: 2025-01-23
Description: A Python GUI made by myself to assist recording metadata during the experiment
tags:
  - python
  - GUI
---
# OUTPUT
The GUI (version 1.1) now has two tabs, one for input basic experiment information, the other for generate tags which used for paste to the comment dialog of PCO.Camware saving process.

Below are the appearances of the GUI
![](<metadata-generator-tab0.png>)
![](<metadata-generator-tab1.png>)

Here are the three formats of output files (single dataFrame JSON, multi-dataFrame JSON, MARKDOWN)
![](<three-types-of-data-formats.png>)
# MEMO
Here are some useful concepts which applied to this program
- Validators
	- QIntValidator
	- QRegularExpression, QRegularExpressionValidator
- QDialogButtonBoxs
- Import classes from files in other folders
- Clear widgets in a layout
- Clear layout from a widget
- Use Path to read files in the relative directory
- Use .bat file to activate venv and run the script

> [!caution]
> Wrongly connect the EnterPressed signal to the function of save file caused TypeError
> 	Fixed by reconnecting to self.accept()
> In f"" string expression, be careful not to put double quotation marks in side double quotationmarks to avoid unmatched "("

> [!info]
> The code of .bat file

```batch
SET dirPath=%CD%
SET venvPath="%dirPath%\.venv\Scripts\activate.bat"
SET pyPath="%dirPath%\.venv\Scripts\python.exe"
SET progPath="%dirPath%\main.py"

CALL %venvPath%
%pyPath% %progPath%

```