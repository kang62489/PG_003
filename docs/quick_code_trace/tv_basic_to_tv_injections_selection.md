# tv_basic → tv_injections: Row Selection Flow

> 📅 Created: 2026-03-03
> 🔍 Query: "Which code connects selecting a row in tv_exp_info to showing injection history in tv_inj_history?"

---

## 📁 Files Overview

- `classes/dialog_exp_db.py` - Database viewer dialog; contains signal connection, filter logic, and model setup

---

## 🔗 Code Trace

### 1. `classes/dialog_exp_db.py` — Model & View Setup (L53–70)

**Purpose**: Creates QSqlTableModel for both tables and binds them to the table views.

```python
self.model_basic = QSqlTableModel(db=self.db)
self.tv_basic.setModel(self.model_basic)
self.sm_basic = self.tv_basic.selectionModel()   # ← selection model captured here

self.model_injections = QSqlTableModel(db=self.db)
self.model_injections.setTable("INJECTION_HISTORY")
self.tv_injections.setModel(self.model_injections)
```

---

### 2. `classes/dialog_exp_db.py` — Signal Connection (L150–151)

**Purpose**: Connects the selection change of `tv_basic` to `preview_inj()`.

```python
def connect_signals(self):
    self.sm_basic.selectionChanged.connect(self.preview_inj)
```

- **Signal**: `sm_basic.selectionChanged` (fires when user selects a row in `tv_basic`)
- **Slot**: `self.preview_inj`

---

### 3. `classes/dialog_exp_db.py` — Slot: `preview_inj()` (L157–169)

**Purpose**: Reads `Animal_ID` from selected row(s) and filters `tv_injections`.

```python
def preview_inj(self):
    selected_indexes = self.sm_basic.selectedIndexes()
    if not selected_indexes:
        return

    # Get unique Animal_IDs from selected rows (column 1)
    animal_ids = list({self.model_basic.index(idx.row(), 1).data() for idx in selected_indexes})

    # Build filter and apply
    ids_str = "', '".join(animal_ids)
    self.model_injections.setFilter(f"Animal_ID IN ('{ids_str}')")
    self.model_injections.select()   # ← tv_injections refreshes automatically
```

---

## 📝 Notes

- The widget names in code are **`tv_basic`** (exp info) and **`tv_injections`** (inj history), not `tv_exp_info` / `tv_inj_history`
- `tv_injections` updates automatically because it shares `model_injections` — no manual view refresh needed
- Multi-row selection is supported: Animal_IDs from all selected rows are used in the `IN (...)` filter
