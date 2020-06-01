import os
from PIL import Image
from pathlib import Path
from invoke import task


@task
def lowercase_jpg(c):
    files = list(Path("content").rglob("*.JPG"))
    for f in files:
        old_path = str(f)
        new_path = str(f).replace(".JPG", ".jpg")
        os.rename(old_path, new_path)


@task
def remove_metadata(c):
    c.run("exiftool -r -overwrite_original -P -all= content -ext jpg -ext jpeg")


@task
def resize_images(c, pre=[lowercase_jpg, remove_metadata]):
    files = list(Path("images").rglob("*.jpg"))
    for f in files:
        filesize = f.stat().st_size
        if filesize > 300000:
            im = Image.open(f)
            width, height = im.size
            if width > 2024 or height > 2024:
                cmd = f"mogrify -verbose -resize 2024\>x2024\> {str(f)}"
                c.run(cmd)
