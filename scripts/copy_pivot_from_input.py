import os
import glob
import sys
import shutil


def copy_pivot_from_input(output_folder='temporary/pivot'):
    """inputフォルダーにある `*.json` ファイルを pivotフォルダーへコピーします"""

    input_files = glob.glob("./input/*.json")
    for input_file in input_files:
        # basename
        try:
            basename = os.path.basename(input_file)
        except:
            print(f"Error: input_file={input_file} except={sys.exc_info()[0]}")
            raise

        copy_file = os.path.join(output_folder, basename)
        shutil.copyfile(input_file, copy_file)
