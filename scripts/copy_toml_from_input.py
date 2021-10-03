import glob
import os
import shutil
import sys


def copy_toml_from_input(output_folder='temporary/toml'):
    """inputフォルダーにある `*.toml` ファイルを output_folder へコピーします"""

    input_files = glob.glob("./input/*.toml")
    for input_file in input_files:
        # basename
        try:
            basename = os.path.basename(input_file)
        except:
            print(f"Error: input_file={input_file} except={sys.exc_info()[0]}")
            raise

        copy_file = os.path.join(output_folder, basename)
        shutil.copyfile(input_file, copy_file)
