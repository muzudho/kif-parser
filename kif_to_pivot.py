import glob
from os import error, system
import os
from remove_all_output import clear_all_records_in_folder
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
import argparse
from remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.move_file_to_folder import move_file_to_folder
from scripts.test_lib import create_sha256_by_file_path


def __main(debug=False, template_name=""):

    # (a) Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.kif'

    # (a) Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/kif'
    layer2_file_pattern = './temporary/kif/*.kif'

    # (a) Layer 3. Pivotフォルダ―(なし)

    # (a) 中間Layer.
    object_folder = 'temporary/object'

    # (a) Layer 4. 逆方向のフォルダ―
    layer4_folder = 'temporary/reverse-kifu'
    layer5_folder = 'temporary/reverse-kif'

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
    kif_files = glob.glob(layer2_file_pattern)

    for kif_file in kif_files:

        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(kif_file)

        # (d-1) Shift-JIS から UTF-8 へ変更
        kifu_file = convert_kif_to_kifu(
            kif_file, output_folder='temporary/kifu')
        if kifu_file is None:
            print(
                f"[ERROR] kif_to_pivot.py __main: (d-1) parse fail. kif_file={kif_file}")
            continue

        # (d-2) 目的のファイル（Pivot）へ変換
        object_file = convert_kifu_to_pivot(
            kifu_file, output_folder=object_folder)
        if object_file is None:
            print(
                f"[ERROR] kif_to_pivot.py __main: (d-2) parse fail. kifu_file={kifu_file}")
            continue

        # ここから逆の操作を行います

        # (e-1)
        reversed_kifu_file = convert_pivot_to_kifu(
            object_file, output_folder=layer4_folder, template_name=template_name)
        if reversed_kifu_file is None:
            print(
                f"[ERROR] kif_to_pivot.py __main: (e-1) parse fail. object_file={object_file}")
            continue

        # (e-2) Shift-JIS から UTF-8 へ変更
        reversed_kif_file = convert_kifu_to_kif(
            reversed_kifu_file, output_folder=layer5_folder)
        if reversed_kif_file is None:
            print(
                f"[ERROR] kif_to_pivot.py __main: (e-2) parse fail. reversed_kifu_file={reversed_kifu_file}")
            continue

        # (f) レイヤー５にあるファイルの SHA256 生成
        layer5_file_sha256 = create_sha256_by_file_path(reversed_kif_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer5_file_sha256:
            try:
                basename = os.path.basename(kif_file)
            except:
                print(
                    f"[ERROR] kif_to_pivot.py __main: (g) kif_file={kif_file} except={system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"[WARNING] Irreversible conversion. basename={basename}")
            # continue

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へコピーします
        move_file_to_folder(object_file, last_layer_folder)

    # (i) 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .kif file to .json (PIVOT) file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
