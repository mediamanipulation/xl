import os
import shutil

def fix_imports_with_backup(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if not any(fname.endswith(ext) for ext in [".py", ".json", ".md", ".txt"]):
                continue

            full_path = os.path.join(dirpath, fname)

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                updated = content.replace("from gui.", "from gui.") \
                                 .replace("import gui.", "import gui.") \
                                 .replace("gui.", "gui.")  # catch edge cases

                if content != updated:
                    # Create backup file
                    backup_path = full_path + ".bak"
                    shutil.copy2(full_path, backup_path)

                    # Write updated content
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(updated)

                    print(f"✔ Fixed and backed up: {full_path}")

            except Exception as e:
                print(f"✖ Error with {full_path}: {e}")

if __name__ == "__main__":
    fix_imports_with_backup(".")  # Run at project root
