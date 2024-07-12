import os
import re


def generate_toc(root_dir):
    toc = "# Table of Contents\n\n"
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, "").count(os.sep)
        indent = "  " * level
        if level > 0:
            folder_name = os.path.basename(root)
            toc += f"{indent}- {folder_name}/\n"
        for file in files:
            if file.endswith(".md") and file != "README.md":
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_dir)
                toc += f"{indent}  - [{file[:-3]}]({rel_path})\n"
    return toc


def update_readme(toc):
    with open("README.md", "r") as f:
        content = f.read()

    toc_pattern = r"# Table of Contents\n\n[\s\S]*?(?=\n#|$)"
    if re.search(toc_pattern, content):
        updated_content = re.sub(toc_pattern, toc, content)
    else:
        updated_content = toc + "\n\n" + content

    with open("README.md", "w") as f:
        f.write(updated_content)


if __name__ == "__main__":
    root_dir = "."
    toc = generate_toc(root_dir)
    update_readme(toc)
    print("Table of Contents generated and README.md updated.")
