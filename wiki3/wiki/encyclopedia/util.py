import os
import markdown2

ENTRY_DIR = "entries"

def list_entries():
    return sorted([f.replace(".md", "") for f in os.listdir(ENTRY_DIR) if f.endswith(".md")])

def save_entry(title, content):
    with open(f"{ENTRY_DIR}/{title}.md", "w", encoding="utf-8") as f:
        f.write(content)

def get_entry(title):
    try:
        with open(f"{ENTRY_DIR}/{title}.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

def convert_md_to_html(markdown_text):
    return markdown2.markdown(markdown_text)
