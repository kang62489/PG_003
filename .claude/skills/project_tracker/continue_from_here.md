# Log of the project progress 2026-03-02 Mon

List of modified files:
- `main.py` (new — main GUI entry point, already created before this session)
- `utils/params.py` (new — app constants and UI sizes, already created before this session)

## Current GUI Structure (already created)
```
PG_005/
├── main.py              # QMainWindow + QTabWidget (w_main) with 3 tabs
└── utils/
    └── params.py        # APP_NAME, APP_VERSION, UISizes, paths
```

### Tabs in `w_main` (all currently empty QWidget — no views/controls yet):
1. `tab_dor_query`      → "Query by DOR"
2. `tab_abf_preview`    → "ABF Quick Check"
3. `tab_analysis_list`  → "Analysis List"

### Already working in `main.py`:
- Window title: "RADIO - Response Associated Distribution Imaging Observer"
- Fixed size: 1600 x 850
- Status bar: showing APP_STATUS_MESSAGE
- Fusion style, Windows dark mode disabled

## What have we done this session?
- Reviewed project documentation (`docs/PROJECT_SUMMARY.md`, `docs/DEPENDENCY_DIAGRAM.md`)
- Compared actual file structure against what's documented — found several discrepancies
- User removed the empty `ui/` folder
- Discussed how to add/enable a `QStatusBar` in `QMainWindow`

## Documentation discrepancies found (not yet fixed!)
- `PROJECT_SUMMARY.md` says `doc/` but actual folder is `docs/`
- `PROJECT_SUMMARY.md` lists `scripts/` folder (with `migrate_database.py`) — does NOT exist
- `PROJECT_SUMMARY.md` lists `utils/` folder as "currently unused" — is now actively used
- `docs/knowledgebase/` folder exists but NOT listed in `PROJECT_SUMMARY.md`
- `docs/PI_MEETING_PREP.md` exists but NOT listed in `PROJECT_SUMMARY.md`
- `DEPENDENCY_DIAGRAM.md` refers to `doc/examples/` — should be `docs/examples/`
- Root-level files not documented anywhere: `RUN_BATCH.md`, `README.md`, `.python-version`

## What should we do next? (TODOs)
- [ ] **Continue GUI — add views and controls for each tab of `w_main`**:
      → `tab_dor_query`      ("Query by DOR") — query the database by DOR
      → `tab_abf_preview`    ("ABF Quick Check") — quick preview of ABF files
      → `tab_analysis_list`  ("Analysis List") — list of analyses to run/review
- [ ] Fix documentation discrepancies in `docs/PROJECT_SUMMARY.md` and `docs/DEPENDENCY_DIAGRAM.md`
