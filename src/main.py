from textnode import TextNode
import os
import shutil
from page import copy_dir, generate_page_recursive

copy_dir("static", "public")
generate_page_recursive("content", "template.html", "public")
