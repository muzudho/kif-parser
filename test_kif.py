import glob
import os
import sys
from remove_all_output import clear_all_records_in_folder
from scripts.copy_files_to_folder import copy_files_to_folder
from scripts.test_lib import create_sha256_by_file_path
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif


def __main(debug=False):

    # Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.kif'

    # Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/kif'
    layer2_file_pattern = './temporary/kif/*.kif'

    # Layer 3. Pivotフォルダ―
    layer3_folder = 'temporary/pivot'

    # 最終Layer.
    last_layer_folder = 'output'

    # 1. 最終レイヤーの フォルダー を空っぽにします
    if not debug:
        clear_all_records_in_folder(last_layer_folder, echo=False)

    # 2. レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
    copy_files_to_folder(layer1_file_pattern, layer2_folder)

    # 3. レイヤー２にあるファイルのリスト
    kif_files = glob.glob(layer2_file_pattern)

    for kif_file in kif_files:

        # レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(kif_file)

        # Shift-JIS から UTF-8 へ変更
        kifu_file = convert_kif_to_kifu(kif_file)
        if kifu_file is None:
            return None, None

        # 4. Pivot へ変換
        pivot_file = convert_kifu_to_pivot(
            kifu_file, output_folder=layer3_folder)
        if pivot_file is None:
            # Error
            print(f"convert kif to pivot_file fail. kif_file={kif_file}")
            return None

        # 5. Pivot から 目的の棋譜ファイルへ変換
        kifu_file = convert_pivot_to_kifu(
            pivot_file, output_folder='temporary/kifu')
        if kifu_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")
            continue

        # kifu to kif
        reverse_kif_file = convert_kifu_to_kif(
            kifu_file, output_folder='reverse-temporary/kif')
        if reverse_kif_file is None:
            # Error
            print(
                f"convert pivot to kif fail. kifu_file={kifu_file}")
            return None

        # 3-4. ファイルをバイナリ形式で読み込んで SHA256 生成
        reverse_kif_sha256 = create_sha256_by_file_path(reverse_kif_file)

        # 3-5. 一致比較
        if layer2_file_sha256 != reverse_kif_sha256:
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

    # 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
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
