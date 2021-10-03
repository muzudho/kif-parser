import glob
from os import error
from scripts.move_file_to_folder import move_file_to_folder


def main():
    source_file_pattern_list = ('./output/*.kif',
                                './output/*.kifu',
                                './output/*.json',
                                './output/*.toml')

    for source_file_pattern in source_file_pattern_list:
        source_file_list = glob.glob(source_file_pattern)
        for source_file in source_file_list:
            move_file_to_folder(source_file, 'input')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
