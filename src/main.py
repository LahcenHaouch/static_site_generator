from textnode import TextNode
import os
import shutil
from block_markdown import generate_page


def copy_dir(src, dist):

    if not os.path.exists(src):
        return

    if os.path.isfile(src):
        shutil.copy(src, os.path.join(dist, os.path.dirname(src)))
    else:

        new_dir = os.path.join(dist, src)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        for el in os.listdir(src):
            el_path = os.path.join(src, el)

            copy_dir(el_path, dist)


copy_dir("static", "public")
generate_page("content/index.md", "template.html", "public/index.html")
