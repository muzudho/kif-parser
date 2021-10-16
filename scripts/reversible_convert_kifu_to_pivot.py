import glob
import os
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from remove_all_temporary import remove_all_temporary
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.test_lib import create_sha256_by_file_path


def reversible_convert_kifu_to_pivot(debug=False, last_layer_folder='output', no_remove_output_pivot=False, template_name=""):

    # (a) Layer 1. 入力フォルダ―
    first_layer_file_pattern = './input/*.kifu'

    # (a) Layer 2. 入力フォルダ―のコピーフォルダー
    layer2_folder = 'temporary/to-pivot/kifu'
    layer2_file_pattern = './temporary/to-pivot/kifu/*.kifu'

    # (a) Layer 3. Pivotフォルダ―(なし)

    # (a) 中間Layer.
    object_folder = 'temporary/to-pivot/object'
    object_file_pattern = 'temporary/to-pivot/object/*.json'

    # (a) Layer 4. 逆入力フォルダ―
    layer4_folder = 'temporary/to-pivot/reverse-kifu'

    # (b-1) 最終レイヤーの フォルダー を空っぽにします
    clear_all_records_in_folder(last_layer_folder, echo=False)

    # (b-2) レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
    input_files = glob.glob(first_layer_file_pattern)
    for input_file in input_files:
        copy_file_to_folder(input_file, layer2_folder)

    # (b-3) レイヤー２にあるファイルのリスト
    kifu_files = glob.glob(layer2_file_pattern)

    for kifu_file in kifu_files:

        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(kifu_file)

        # (d-1) 目的のファイル（Pivot）へ変換
        object_file = convert_kifu_to_pivot(
            kifu_file, output_folder=object_folder)
        if object_file is None:
            print(
                f"[ERROR] reversible_convert_kifu_to_pivot.py reversible_convert_kifu_to_pivot(): (d-1) parse fail. kifu_file={kifu_file}")
            continue

        # ここから逆の操作を行います

        # (e-1)
        reversed_kifu_file = convert_pivot_to_kifu(
            object_file, output_folder=layer4_folder, template_name=template_name)
        if reversed_kifu_file is None:
            print(
                f"[ERROR] reversible_convert_kifu_to_pivot.py reversible_convert_kifu_to_pivot(): (e-1) parse fail. kifu_file={kifu_file}")
            continue

        # (f) レイヤー４にあるファイルの SHA256 生成
        layer4_file_sha256 = create_sha256_by_file_path(reversed_kifu_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer4_file_sha256:
            try:
                basename = os.path.basename(kifu_file)
            except:
                print(
                    f"Error: kifu_file={kifu_file} except={os.system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"[WARNING] Irreversible conversion to-pivot. basename={basename}")

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へコピーします
        copy_file_to_folder(object_file, last_layer_folder)

    # (i) 後ろから1. 変換の途中で作ったファイルは削除します
    if not debug:
        remove_all_temporary(
            echo=False, no_remove_output_pivot=no_remove_output_pivot)
