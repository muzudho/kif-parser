import glob
from os import system
import os
from remove_all_output import clear_all_records_in_folder
from remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.test_lib import create_sha256_by_file_path


def reversible_convert_kif_to_kifu(debug=False, no_remove_output_pivot=False):

    # (a) Layer 1. 入力フォルダ―
    layer1_file_pattern = './input/*.kif'

    # (a) Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/no-pivot/kif'
    layer2_file_pattern = './temporary/no-pivot/kif/*.kif'

    # (a) Layer 3. Pivotフォルダ―(なし)

    # (a) 中間Layer.
    object_folder = 'temporary/no-pivot/object'

    # (a) Layer 4. 逆方向のフォルダ―
    layer4_folder = 'temporary/no-pivot/reverse-kif'

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

        # (d-1) 目的のファイル（KIFU UTF-8）へ変換
        object_file = convert_kif_to_kifu(
            kif_file, output_folder=object_folder)
        if object_file is None:
            print(
                f"[ERROR] reversible_convert_kif_to_kifu.py reversible_convert_kif_to_kifu(): (d-1) parse fail. kif_file=[{kif_file}]")
            continue

        # ここから逆の操作を行います

        # (e-1) UTF-8 から Shift-JIS へ変換
        reversed_kif_file = convert_kifu_to_kif(
            object_file, output_folder=layer4_folder)

        # (f) レイヤー４にあるファイルの SHA256 生成
        layer4_file_sha256 = create_sha256_by_file_path(reversed_kif_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer4_file_sha256:
            try:
                basename = os.path.basename(kif_file)
            except:
                print(
                    f"[ERROR] reversible_convert_kif_to_kifu.py reversible_convert_kif_to_kifu(): (g) parse fail. kif_file={kif_file} except={system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"[WARNING] Irreversible conversion. basename={basename}")

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へコピーします
        copy_file_to_folder(object_file, last_layer_folder)

    # (i) 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
        remove_all_temporary(
            echo=False, no_remove_output_pivot=no_remove_output_pivot)