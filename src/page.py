import os
import shutil
import pathlib
from block_markdown import markdown_to_html_node, extract_title


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    file = open(from_path)
    file_content = file.read()
    template_file = open(template_path)
    template_content = template_file.read()

    content = markdown_to_html_node(file_content).to_html()
    title = extract_title(file_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", content)

    destination_file = open(dest_path, "w")
    destination_file.write(template_content)

    file.close()
    template_file.close()
    destination_file.close()


def generate_page_recursive(src, template_path, dest):
    if os.path.isfile(src):
        generate_page(
            src,
            template_path,
            os.path.join(dest, pathlib.PurePath(src).name.replace("md", "html")),
        )
    else:
        dir_content = os.listdir(src)
        for file in dir_content:
            new_dest = dest
            if os.path.isdir(os.path.join(src, file)) and not os.path.exists(
                os.path.join(dest, file)
            ):
                os.mkdir(os.path.join(dest, file))
                new_dest = os.path.join(dest, file)

            generate_page_recursive(
                os.path.join(src, file),
                template_path,
                new_dest,
            )
