import glob
import shutil
import os
import sys


def move_file_to_folder_by_pattern_list(output_file_patterns, output_folder):
    """指定のファイルを、指定のフォルダーへ移動します"""

    for output_file_pattern in output_file_patterns:
        # 出力ファイル一覧
        output_files = glob.glob(output_file_pattern)
        for output_file in output_files:

            # basename
            try:
                basename = os.path.basename(output_file)
            except:
                print(
                    f"Error: output_file={output_file} except={sys.exc_info()[0]}")
                raise

            shutil.move(output_file, os.path.join(output_folder, basename))
