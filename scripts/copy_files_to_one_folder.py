import glob
import shutil
import os
import sys


def copy_files_to_one_folder(file_pattern_list, output_folder):

    for file_pattern in file_pattern_list:
        # 出力ファイル一覧
        file_list = glob.glob(file_pattern)
        for file in file_list:
            # basename
            try:
                basename = os.path.basename(file)
            except:
                print(
                    f"Error: file={file} except={sys.exc_info()[0]}")
                raise

            #_stem, extention = os.path.splitext(basename)
            # if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
            #    return None

            shutil.copyfile(
                file, os.path.join(output_folder, basename))
