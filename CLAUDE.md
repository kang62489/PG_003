## PG_003 - Acetylcholine Imaging Acquisition and Analysis
The project is a GUI tool for recording metadata of the tiff and abf files during the experiment and generate tags for writing to the recording files (*.rec). It is written in Python and uses PySide6 for the GUI.

## Documentation
1. When create new markdown files (except README.md), always save them to the `docs/` folder. If `docs/` does not exist, create one.
2. When using plan mode creates new markdown plans, always save them to the `.claude/plans/` folder. If `plans/` does not exist, create one.

## Code Style
1. Follow the naming convention in `docs/ui_widget_names.md` for naming UI widgets.

## Answering Questions
1. Try using step-by-step approach to answer the questions.
2. Try using simple examples with actual data/numbers for explanation.
3. Use "-" or "=" to create separation lines for separating different points/sessions.
4. Use emoji to make the text lively.
5. Try using clear topic senentences for each section of your answers or plans.

## Others
1. When user greets, use the command (date +"%A, %B %d, %Y, %I:%M %p — (UTC%:::z)") to get and greet back in one line (e.g. good morning, good afternoon, or other appropriate greetings) with ", now it is" + current datetime + timezone from the system.
2. When user greets, check and show if CLAUDE.md is loaded.
3. When user asks "where should we continue", check if `continue_from_here.md` exists. If so, read and summarize the TODO list in the file. If not, show messages "No left works! + happy emoji"