def read_file_safe(filename):
    """
    Sicher lesende Dateien mit Encoding-Erkennung für Windows
    Safe file reading with encoding detection for Windows
    """
    encodings = ['utf-8', 'cp1252', 'latin1', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue

    # Last resort: ignore errors
    try:
        with open(filename, 'r', encoding='cp1252', errors='ignore') as f:
            return f.read()
    except:
        return f"ERROR: Cannot read {filename}"
