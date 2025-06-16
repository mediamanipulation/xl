# convert_spanish_entities_parser.py

import sys
from pathlib import Path
from bs4 import BeautifulSoup, Comment

# ─── 1) Entity mappings ─────────────────────────────────────────
SPANISH_FRIENDLY = {
    'Á': '&Aacute;', 'á': '&aacute;',
    'É': '&Eacute;', 'é': '&eacute;',
    'Í': '&Iacute;', 'í': '&iacute;',
    'Ñ': '&Ntilde;', 'ñ': '&ntilde;',
    'Ó': '&Oacute;', 'ó': '&oacute;',
    'Ú': '&Uacute;', 'ú': '&uacute;',
    'Ü': '&Uuml;',   'ü': '&uuml;',
    '«': '&laquo;',  '»': '&raquo;',
    '¿': '&iquest;','¡': '&iexcl;',
    '€': '&euro;',   '₧': '&#8359;'
}

def replace_in_text(text: str, mapping: dict) -> str:
    """
    Replace each key in mapping with its value in the given text.
    Uses str.translate for C-level performance.
    """
    table = str.maketrans(mapping)
    return text.translate(table)

# ─── 2) Main ────────────────────────────────────────────────────
def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_spanish_entities_parser.py <file.html>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"Error: '{path}' not found.")
        sys.exit(1)

    # Read & parse
    html = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')  # or 'lxml' if available

    # Walk all text nodes, skipping comments and script/style
    for node in soup.find_all(string=True):
        if isinstance(node, Comment) or node.parent.name in ('script', 'style'):
            continue

        new_txt = replace_in_text(str(node), SPANISH_FRIENDLY)
        if new_txt != node:
            node.replace_with(new_txt)

    # Overwrite same file
    path.write_text(str(soup), encoding='utf-8')
    print(f"✅ Done: friendly named entities inserted into '{path.name}'")

if __name__ == "__main__":
    main()
