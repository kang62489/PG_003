def rec_encoding_checker(rec_path):
    """Detect the encoding of a .rec file by checking its BOM (Byte Order Mark).

    Returns the encoding string to be used when opening the file for reading or writing.
    """
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
