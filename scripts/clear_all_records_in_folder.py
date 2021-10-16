import os
import glob


def clear_all_records_in_folder(folder, echo=True):
    basename_pattern_list = ('*.kif',
                             '*.kifu',
                             '*.json',
                             '*.toml')

    for basename_pattern in basename_pattern_list:

        file_pattern = os.path.join(folder, basename_pattern)

        # 出力ファイル一覧
        files = glob.glob(file_pattern)
        for file in files:
            if echo:
                print(f"Remove: {file}")
            os.remove(file)
