# This script will identify duplicates of image files that are slightly altered (compressed, rotated, etc.) and move them to a "duplicates" folder

from pathlib import Path
import shutil

from PIL import Image, ImageOps, ImageFile
import imagehash
ImageFile.LOAD_TRUNCATED_IMAGES = True

PHOTOS = Path(r"C:\your\path\to\source\photos")
DUPES = Path(r"C:\your\path\to\duplicates\folder")

DUPES.mkdir(parents=True, exist_ok=True)

IMAGE_EXTS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tiff"
}

seen = []

files = [
    f for f in PHOTOS.rglob("*")
    if f.is_file() and f.suffix.lower() in IMAGE_EXTS
]

total = len(files)

THRESHOLD = 2 # Controls the aggressiveness of deduplication; 2 is a good starting point, then gradually increase to 5 or 6 if necessary

for index, file, in enumerate(files, start=1):

    if index % 100 == 0:
        print(f"Processed {index}/{total}")

    try:
        with Image.open(file) as img:

            # Normalize phone camera orientation
            img = ImageOps.exif_transpose(img)

            phash = imagehash.phash(img)

        duplicate_found = False

        for existing_hash, existing_file in seen:

            distance = phash - existing_hash
            
            if distance <= THRESHOLD:

                duplicate_found = True

                current_size = file.stat().st_size
                existing_size = existing_file.stat().st_size

                # Keep the larger file
                if current_size > existing_size:

                    target = DUPES / existing_file.name

                    counter = 1
                    while target.exists():
                        target = (
                            DUPES /
                            f"{existing_file.stem}_{counter}{existing_file.suffix}"
                        )
                        counter += 1

                    shutil.move(str(existing_file), str(target))

                    seen.remove((existing_hash, existing_file))
                    seen.append((phash, file))

                else:

                    target = DUPES / file.name

                    counter = 1
                    while target.exists():
                        target = (
                            DUPES /
                            f"{file.stem}_{counter}{file.suffix}"
                        )
                        counter += 1

                    shutil.move(str(file), str(target))
                    
                break

        if not duplicate_found:
            seen.append((phash, file))

    except Exception as e:
        print(f"Failed: {file}")
        print(e)

print("Done.")