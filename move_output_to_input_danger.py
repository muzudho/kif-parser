from scripts.move_file_to_folder_by_pattern_list import move_file_to_folder_by_pattern_list


def main():
    output_file_patterns = ('./output/*.kif',
                            './output/*.kifu',
                            './output/*.json',
                            './output/*.toml')

    move_file_to_folder_by_pattern_list(
        output_file_patterns, output_folder='input')


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
