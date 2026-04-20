---
keywords: encoding, utf-8, utf-16, BOM, byte order mark, rec file, rec_encoding_checker
related: none
type: trouble_shooting
---

# 2026-04-17

## Problem: `.rec` files can be UTF-8 or UTF-16 encoded

`.rec` files in this project may be saved in either UTF-8 or UTF-16 encoding depending on the software that created them. The original code hardcoded the encoding:

```python
# ctrl_rec_import.py — hardcoded UTF-16
with open(rec_path, mode="r", encoding="utf-16") as f:

# ctrl_rec_writer.py — hardcoded UTF-16-LE
with open(rec_filepath, mode="r", encoding="utf-16-LE") as f:
with open(self.rec_filepath, mode="w", encoding="utf-16-LE") as f:
```

This caused failures when reading/writing UTF-8 encoded `.rec` files.

---

## Solution: BOM detection via `rec_encoding_checker()`

### What is a BOM?

A BOM (Byte Order Mark) is a few special bytes at the very start of a file that indicate its encoding:

| Encoding | BOM bytes (hex) |
|----------|----------------|
| UTF-16 LE | `FF FE` |
| UTF-16 BE | `FE FF` |
| UTF-8 with BOM | `EF BB BF` |
| UTF-8 (no BOM) | *(none)* |

### Shared function: `functions/rec_encoding_checker.py`

```python
def rec_encoding_checker(rec_path):
    with open(rec_path, "rb") as f:
        raw = f.read(4)  # Only need the first few bytes for BOM detection

    # UTF-16 BOM: FF FE (little-endian) or FE FF (big-endian)
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return "utf-16"

    # UTF-8 BOM: EF BB BF
    elif raw[:3] == b"\xef\xbb\xbf":
        return "utf-8-sig"

    # No BOM — assume plain UTF-8
    return "utf-8"
```

### How it's used

The function is called inline in the `encoding=` argument of `open()`, so the `with open(...)` structure stays clean and unchanged:

```python
# Reading
with open(rec_path, mode="r", encoding=rec_encoding_checker(rec_path)) as f:
    original_content = f.read().splitlines()

# Writing — detects encoding from the existing file, writes back with same encoding
with open(self.rec_filepath, mode="w", encoding=rec_encoding_checker(self.rec_filepath)) as f:
    f.write("\n".join(contents_to_be_written))
```

This guarantees that a file is always **written back with the same encoding it was read in**.

---

## Files changed

| File | Change |
|------|--------|
| `functions/rec_encoding_checker.py` | ✨ New — shared BOM detection function |
| `functions/__init__.py` | ✨ New — makes `functions/` a Python package |
| `controllers/ctrl_rec_import.py` | `rec_content_scanner()` — replaced hardcoded `utf-16` |
| `controllers/ctrl_rec_writer.py` | `scan_rec_commments()`, `write_rec()`, `revert_rec()` — replaced hardcoded `utf-16-LE` |
