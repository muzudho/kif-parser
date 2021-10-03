import glob
import os
from remove_all_output import remove_all_output
from scripts.copy_files_to_folder import copy_files_to_folder
from scripts.test_lib import create_sha256_by_file_path
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
import argparse
from remove_all_temporary import remove_all_temporary
import sys
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu


def __main(debug=False):
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter_last_layer_folder_clean = True
        converter_last_layer_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter_firlst_layer_file_pattern = './input/*.kifu'
    converter_layer2_folder = 'temporary/kifu'

    # 3-1. 処理対処となる各ファイル
    converter_layer2_file_pattern = './temporary/kifu/*.kifu'

    # 1. 最終フォルダーを空っぽにします
    if converter_last_layer_folder_clean:
        remove_all_output(converter_last_layer_folder_clean_echo)

    # inputフォルダーにある ? ファイルを layer2_folder へコピーします
    copy_files_to_folder(
        converter_firlst_layer_file_pattern, converter_layer2_folder)

    kifu_files = glob.glob(converter_layer2_file_pattern)

    for kifu_file in kifu_files:
        # 3-1. SHA256を生成します
        kifu_sha256 = create_sha256_by_file_path(kifu_file)

        # 5. Shift-JIS から UTF-8 へ変換 (不要)

        # 6. Pivot へ変換 (不要)
        pivot_file = convert_kifu_to_pivot(kifu_file)

        # Pivot to kifu
        reverse_kifu_file, _done_pivot_file = convert_pivot_to_kifu(
            pivot_file, output_folder='reverse-temporary/kifu')
        if reverse_kifu_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")

        # 3-4. SHA256 生成
        reverse_kifu_sha256 = create_sha256_by_file_path(reverse_kifu_file)

        # 3-5. 一致比較
        if kifu_sha256 != reverse_kifu_sha256:
            # Error
            # basename
            try:
                basename = os.path.basename(kifu_file)
            except:
                print(
                    f"Error: test_kifu.py kifu_file={kifu_file} except={sys.exc_info()[0]}")
                raise

            print(f"Not match SHA256. basename={basename}")
            return None

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Test .kif Convert.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
