import os
import re
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
        cmd = f"mogrify -verbose -format jpeg -layers Dispose -resize 1024\>x1024\> -quality 75% {str(f)}"
        c.run(cmd)
