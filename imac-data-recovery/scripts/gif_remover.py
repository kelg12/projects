# This script identifies files with .gif extensions within a given path and bulk deletes them all (PLEASE USE WITH CAUTION)
# Only used this as there was over 40,000 GIFs extracted and every single one of them was some junk cached web icon

from pathlib import Path

ROOT = Path(r"C:\your\path\to\GIFs")

deleted = 0

for file in ROOT.rglob("*"):
    if file.is_file() and file.suffix.lower() == ".gif":
        try:
            file.unlink()
            deleted += 1

            if deleted % 100 == 0:
                print(f"Deleted {deleted} GIFs...")

        except Exception as e:
            print(f"Failed to delete {file}")
            print(e)

print(f"\nDone. Deleted {deleted} GIF files.")
