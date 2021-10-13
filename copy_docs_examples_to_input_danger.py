from scripts.copy_files_to_one_folder_by_pattern import copy_files_to_one_folder_by_pattern


def main():
    source_file_pattern_list = ('./docs/examples/*.kif',
                                './docs/examples/*.kifu',
                                './docs/examples/*.json',
                                './docs/examples/*.toml')

    for source_file_pattern in source_file_pattern_list:
        copy_files_to_one_folder_by_pattern(
            source_file_pattern, 'input')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()