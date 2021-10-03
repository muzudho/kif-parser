import glob
import os
import sys
from remove_all_output import remove_all_output
from scripts.copy_files_to_folder import copy_files_to_folder
from scripts.test_lib import create_sha256_by_file_path
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif


def __main(debug=False):
    # 1. 出力フォルダーを空っぽにします
    if not debug:
        converter_last_layer_folder_clean = True
        converter_last_layer_folder_clean_echo = False

    # 2. 指定のファイルを 指定のフォルダーへコピーします
    converter_firlst_layer_file_pattern = './input/*.kif'
    converter_layer2_folder = 'temporary/kif'

    # 3-1. 処理対処となる各ファイル
    converter_layer2_file_pattern = './temporary/kif/*.kif'

    # 1. 最終フォルダーを空っぽにします
    if converter_last_layer_folder_clean:
        remove_all_output(converter_last_layer_folder_clean_echo)

    # inputフォルダーにある ? ファイルを layer2_folder へコピーします
    copy_files_to_folder(
        converter_firlst_layer_file_pattern, converter_layer2_folder)

    kif_files = glob.glob(converter_layer2_file_pattern)

    for kif_file in kif_files:

        # SHA256 生成
        kif_sha256 = create_sha256_by_file_path(kif_file)

        # 5. Shift-JIS から UTF-8 へ変更
        kifu_file, _done_kif_file = convert_kif_to_kifu(kif_file)
        if kifu_file is None:
            return None, None

        # 6. Pivot へ変換 (不要)
        pivot_file = convert_kifu_to_pivot(kifu_file)
        if pivot_file is None:
            # Error
            print(f"convert kif to pivot_file fail. kif_file={kif_file}")
            return None

        # Pivot to kifu
        kifu_file, _done_pivot_file = convert_pivot_to_kifu(pivot_file)
        if kifu_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")
            continue

        # kifu to kif
        reverse_kif_file, _reverse_done_kifu_file = convert_kifu_to_kif(
            kifu_file, output_folder='reverse-temporary/kif')
        if reverse_kif_file is None:
            # Error
            print(
                f"convert pivot to kif fail. kifu_file={kifu_file}")
            return None

        # 3-4. ファイルをバイナリ形式で読み込んで SHA256 生成
        reverse_kif_sha256 = create_sha256_by_file_path(reverse_kif_file)

        # 3-5. 一致比較
        if kif_sha256 != reverse_kif_sha256:
            try:
                basename = os.path.basename(kif_file)
            except:
                print(f"Error: kif_file={kif_file} except={sys.exc_info()[0]}")
                raise

            _stem, extention = os.path.splitext(basename)
            if extention.lower() != '.kif':
                return ""

            # Error
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
