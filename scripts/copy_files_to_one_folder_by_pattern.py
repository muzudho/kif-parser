import glob
import shutil
import os
import sys


def copy_files_to_one_folder_by_pattern(file_pattern, dst_folder):

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

        # `.` や `*` や `/` がここを通ってきてないか、最終チェックしておきます
        _stem, extention = os.path.splitext(basename)
        if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
            print(
                f"Error: record file move fail. copy_files_to_one_folder_by_pattern.py file=[{file}] file_pattern=[{file_pattern}]")
            continue

        shutil.copyfile(
            file, os.path.join(dst_folder, basename))
