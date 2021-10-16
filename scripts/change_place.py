import os
import sys


def change_place(output_folder, input_file):
    # basename
    try:
        basename = os.path.basename(input_file)
    except:
        print(
            f"[ERROR] copy_file_to_folder.py copy_file_to_folder: input_file={input_file} except={sys.exc_info()[0]}")
        raise

    return os.path.join(output_folder, basename)
