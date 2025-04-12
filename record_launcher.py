import os


def record(path_to_disk, new_name=None):

    # Specify the directory path
    directory_path = "/path/to/your/directory"

    # List all files and directories in the specified path
    entries = os.listdir(directory_path)

    for entry in entries:
        print(entry)


if __name__ == "__main__":
    print()
