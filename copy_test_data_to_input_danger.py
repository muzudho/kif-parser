import glob
from scripts.copy_test_data_to_input_danger import copy_test_data_to_input_danger


def main():
    test_data_file_patterns = ('./test-data/*.kif',
                               './test-data/*.kifu',
                               './test-data/*.json',
                               './test-data/*.toml')

    for test_data_file_pattern in test_data_file_patterns:
        # 出力ファイル一覧
        test_data_files = glob.glob(test_data_file_pattern)
        for test_data_file in test_data_files:
            _undone_test_data_file = copy_test_data_to_input_danger(
                test_data_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
