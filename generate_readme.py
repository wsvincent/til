import os


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
                file_path = os.path.join(relative_path, file)
                toc.append(f"{indent}  - [{file}]({file_path})\n")

    return "".join(toc)


def write_readme(content, output_file="README.md"):
    with open(output_file, "w") as f:
        f.write(content)


if __name__ == "__main__":
    root_directory = "."  # Current directory, change this if needed
    toc_content = generate_toc(root_directory)
    write_readme(toc_content)
    print("README.md with Table of Contents has been generated.")
