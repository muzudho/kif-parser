import glob
import shutil
import os
import sys


def copy_test_data_to_input_danger(test_data_file, output_folder='input'):
    # basename
    try:
        basename = os.path.basename(test_data_file)
    except:
        print(
            f"Error: test_data_file={test_data_file} except={sys.exc_info()[0]}")
        raise

    _stem, extention = os.path.splitext(basename)
    if not (extention.lower() in ['.kif', '.kifu', '.json', '.toml']):
        return None

    # output_folderへ移動します
    undone_test_data_file = shutil.copyfile(
        test_data_file, os.path.join(output_folder, basename))
    return undone_test_data_file


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
