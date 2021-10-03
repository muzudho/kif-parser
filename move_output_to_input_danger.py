from os import error
from scripts.move_file_to_folder_by_pattern import move_file_to_folder_by_pattern


def main():
    output_file_pattern_list = ('./output/*.kif',
                                './output/*.kifu',
                                './output/*.json',
                                './output/*.toml')

    for output_file_pattern in output_file_pattern_list:
        move_file_to_folder_by_pattern(output_file_pattern, 'input')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
