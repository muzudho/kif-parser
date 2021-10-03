import glob
from scripts.copy_files_to_one_folder_by_pattern_list import copy_files_to_one_folder_by_pattern_list


def main():
    test_data_file_pattern_list = ('./test-data/*.kif',
                                   './test-data/*.kifu',
                                   './test-data/*.json',
                                   './test-data/*.toml')

    copy_files_to_one_folder_by_pattern_list(
        test_data_file_pattern_list, output_folder='input')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
