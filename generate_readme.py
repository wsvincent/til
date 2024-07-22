import os


def get_md_title(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                return line[2:]  # Return the title without the '# '
    return os.path.splitext(os.path.basename(file_path))[
        0
    ]  # Return filename without extension if no title found


def generate_toc(root_dir):
    toc = ["# Table of Contents\n"]

    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, "").count(os.sep)
        indent = "  " * level
        relative_path = os.path.relpath(root, root_dir)

        md_files = [f for f in files if f.endswith(".md")]

        if md_files:
            if level > 0:
                folder_name = os.path.basename(root)
                toc.append(f"{indent}- [{folder_name}]({relative_path})\n")

            for file in md_files:
                file_path = os.path.join(root, file)
                title = get_md_title(file_path)
                file_link = os.path.join(relative_path, file)
                toc.append(f"{indent}  - [{title}]({file_link})\n")

    return "".join(toc)


def write_readme(content, output_file="README.md"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    root_directory = "."  # Current directory, change this if needed
    toc_content = generate_toc(root_directory)
    write_readme(toc_content)
    print("README.md with Table of Contents has been generated.")
