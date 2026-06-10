# This program will sort and organize all of the files I recovered from an iMac using PhotoRec.
# Group together photos, screenshots, icons from browser cache, and documents automatically

import os
import shutil
import hashlib
from pathlib import Path
from PIL import Image, UnidentifiedImageError

# Config

SRC = Path(r"C:\your\path\to\source")
DEST = Path(r"C:\your\path\to\destination")

MIN_FILE_SIZE = 120 * 1024  # 120 KB to filter out small cached images
MIN_WIDTH = 100
MIN_HEIGHT = 100

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}

VIDEO_EXTS = {".mov", ".mp4", ".avi"}

# Setup output folders

folders = {
    "photos": DEST / "photos",
    "videos": DEST / "videos",
    "screenshots": DEST / "screenshots",
    "small_images": DEST / "small_images",
    "documents": DEST / "documents",
    "duplicates": DEST / "duplicates",
    "failed": DEST / "failed"
}

for folder in folders.values():
    folder.mkdir(parents=True, exist_ok=True)

# Hash tracking for deduplication

seen_hashes = set()

def file_hash(path: Path) -> str:
    """SHA256 hash of file"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

# Classification logic

def classify_image(path: Path): # Returns category based on size + dimensions
    try:
        size = path.stat().st_size
        if size < MIN_FILE_SIZE:
            return "small_images"
        
        with Image.open(path) as img:
            w, h = img.size

        # Tiny UI icons and other small images
        #if w < MIN_WIDTH or h < MIN_HEIGHT:
            #return "small_images"
        
        # Likely screenshots (wide aspect ratio)
        aspect = w / h
        if aspect > 1.8:
            return "screenshots"
        
        return "photos"
    
    except UnidentifiedImageError:
        return "documents"
    except Exception as e:
        print(f"Image classification failed: {path}")
        print(e)
        return None
    
# Safe file moving to avoid name collisions from PhotoRec naming conventions

def safe_move(src: Path, dest_dir: Path): # Moves file without overwriting existing files
    
    dest_dir.mkdir(parents = True, exist_ok=True)

    target = dest_dir / src.name

    counter = 1
    while target.exists():
        target = dest_dir / f"{src.stem}_{counter}{src.suffix}"
        counter += 1

    shutil.move(str(src), str(target))

# Main function to drive the program

def main():

    total = sum(len(files) for _, _, files in os.walk(SRC))
   
    processed = 0
    
    for root, _, files in os.walk(SRC):
        for name in files:
            path = Path(root) / name

            try:
                # Skip non-files
                if not path.is_file():
                    continue

                processed += 1

                if processed % 100 == 0:
                    pct = (processed / total) * 100
                    print(f"[{pct:.1f}%] {processed}/{total}")

                # Hash for duplication // uncomment to enable deduplication !!
                #h = file_hash(path)

                #if h in seen_hashes:
                #    safe_move(path, folders["duplicates"])
                #    continue

                #seen_hashes.add(h)

                # Route images
                if path.suffix.lower() in IMAGE_EXTS:
                    
                    category = classify_image(path)

                    if category is None:
                        safe_move(path, folders["failed"])
                        continue

                    safe_move(path, folders[category])

                elif path.suffix.lower() in VIDEO_EXTS:

                    safe_move(path, folders["videos"])

                else:

                    safe_move(path, folders["documents"])
            except Exception as e:
                print(f"Failed: {path}")
                print(f"Reason: {e}")

                try:
                    safe_move(path, folders["failed"])
                except Exception:
                    pass

                continue
                
    print("Done processing.")

# Calls the main function

if __name__ == "__main__":
    main()