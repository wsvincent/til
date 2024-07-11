import os


def build_readme():
    with open("README.md", "w") as readme:
        readme.write("# Today I Learned\n\n")
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".md") and file != "README.md":
                    with open(os.path.join(root, file), "r") as entry:
                        readme.write(entry.read() + "\n\n")


if __name__ == "__main__":
    build_readme()
