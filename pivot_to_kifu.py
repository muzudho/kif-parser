import os
from os import system
import argparse
import glob
from remove_all_output import clear_all_records_in_folder
from remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.test_lib import create_sha256_by_file_path
from scripts.move_file_to_folder import move_file_to_folder


def __main(debug=False):

    # (a) Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.json'

    # (a) Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/pivot'
    layer2_file_pattern = './temporary/pivot/*.json'

    # (a) Layer 3. Pivotフォルダ―(なし)

    # (a) 中間Layer.
    middle_folder = 'temporary/object'

    # (a) Layer 4. 逆方向のフォルダ―
    layer4_folder = 'temporary/reverse-pivot'

    # (a) 最終Layer.
    last_layer_folder = 'output'

    # (b-1) 最終レイヤーの フォルダー を空っぽにします
    if not debug:
        clear_all_records_in_folder(last_layer_folder, echo=False)

    # (b-2) レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
    input_files = glob.glob(layer1_file_pattern)
    for input_file in input_files:
        copy_file_to_folder(input_file, layer2_folder)

    # (b-3) レイヤー２にあるファイルのリスト
    pivot_files = glob.glob(layer2_file_pattern)

    for pivot_file in pivot_files:

        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(pivot_file)

        # (d-1) 目的のファイル（KIFU）へ変換
        object_file = convert_pivot_to_kifu(
            pivot_file, output_folder=last_layer_folder)
        if object_file is None:
            print(
                f"[ERROR] pivot_to_kifu.py __main: (d-1) parse fail. pivot_file={pivot_file}")
            continue

        # ここから逆の操作を行います

        # (e-1)
        reversed_pivot_file = convert_kifu_to_pivot(
            object_file, output_folder=layer4_folder)
        if reversed_pivot_file is None:
            print(
                f"[ERROR] pivot_to_kifu.py __main: (e-1) parse fail. object_file={object_file}")
            continue

        # (f) レイヤー４にあるファイルの SHA256 生成
        layer4_file_sha256 = create_sha256_by_file_path(reversed_pivot_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer4_file_sha256:
            try:
                basename = os.path.basename(pivot_file)
            except:
                print(
                    f"[ERROR] kif_to_pivot.py __main: (g) pivot_file={pivot_file} except={system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"[WARNING] Irreversible conversion. basename={basename}")
            # continue

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へ移動します
        move_file_to_folder(object_file, last_layer_folder)

    # (i) 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .json (PIVOT) file to .kifu file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
