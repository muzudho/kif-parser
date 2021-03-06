import os
import glob


def remove_all_input():
    input_file_patterns = ('input/*.kif',
                           'input/*.kifu',
                           'input/*.json',
                           'input/*.toml')

    for intput_file_pattern in input_file_patterns:
        # 入力ファイル一覧
        files = glob.glob(intput_file_pattern)
        for file in files:
            print(f"Remove: {file}")
            os.remove(file)
