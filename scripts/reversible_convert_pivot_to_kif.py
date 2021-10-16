import glob
import os
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from scripts.remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.test_lib import create_sha256_by_file_path
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot


class ReversibleConvertPivotToKif():
    def __init__(self):
        pass

    def reversible_convert_pivot_to_kif(self, debug=False, first_layer_folder='input', no_remove_output_pivot=False, template_name=""):

        # (a) Layer 1. 入力フォルダ―
        first_layer_file_pattern = os.path.join(first_layer_folder, '*.json')

        # (a) Layer 2. 入力フォルダ―のコピーフォルダー
        layer2_folder = 'temporary/from-pivot/pivot'
        layer2_file_pattern = './temporary/from-pivot/pivot/*[[]data[]].json'
        layer2b_folder = 'temporary/from-pivot/kifu'

        # (a) Layer 3. Pivotフォルダ―(なし)

        # (a) 中間Layer.
        middle_folder = 'temporary/from-pivot/object'

        # (a) Layer 4. 逆入力フォルダ―
        layer4_folder = 'temporary/from-pivot/reverse-kifu'
        layer5_folder = 'temporary/from-pivot/reverse-pivot'

        # (a) 最終Layer.
        last_layer_folder = 'output'

        # (b-1) 最終レイヤーの フォルダー を空っぽにします
        if not debug:
            clear_all_records_in_folder(last_layer_folder, echo=False)

        # (b-2) レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
        input_files = glob.glob(first_layer_file_pattern)
        for input_file in input_files:
            copy_file_to_folder(input_file, layer2_folder)

        # (b-3) レイヤー２にあるファイルのリスト
        pivot_files = glob.glob(layer2_file_pattern)

        for pivot_file in pivot_files:
            # (c) レイヤー２にあるファイルの SHA256 生成
            layer2_file_sha256 = create_sha256_by_file_path(pivot_file)

            # (d-1) KIFUへ変換
            kifu_file = convert_pivot_to_kifu(
                pivot_file, output_folder=layer2b_folder, template_name=template_name)
            if kifu_file is None:
                print(
                    f"[ERROR] reversible_convert_pivot_to_kif.py reversible_convert_pivot_to_kif(): Parse fail. pivot_file={pivot_file}")
                continue

            # (d-2) 目的のファイル(KIF Shift-JIS)へ変換
            object_file = convert_kifu_to_kif(
                kifu_file, output_folder=last_layer_folder)
            if object_file is None:
                print(
                    f"[ERROR] reversible_convert_pivot_to_kif.py reversible_convert_pivot_to_kif(): Parse fail. pivot_file={pivot_file}")
                continue

            # ここから逆の操作を行います

            # (e-1)
            reversed_kifu_file = convert_kif_to_kifu(
                object_file, output_folder=layer4_folder, template_name=template_name)
            if reversed_kifu_file is None:
                print(
                    f"[ERROR] reversible_convert_pivot_to_kif.py reversible_convert_pivot_to_kif(): Parse fail. pivot_file={pivot_file}")
                continue

            # (e-2)
            reversed_pivot_file = convert_kifu_to_pivot(
                reversed_kifu_file, output_folder=layer5_folder, template_name=template_name)
            if reversed_pivot_file is None:
                print(
                    f"[ERROR] reversible_convert_pivot_to_kif.py reversible_convert_pivot_to_kif(): Parse fail. pivot_file={pivot_file}")
                continue

            # (f) レイヤー５にあるファイルの SHA256 生成
            layer5_file_sha256 = create_sha256_by_file_path(
                reversed_pivot_file)

            # (g) 一致比較
            if layer2_file_sha256 != layer5_file_sha256:
                try:
                    basename = os.path.basename(pivot_file)
                except:
                    print(
                        f"[ERROR] reversible_convert_pivot_to_kif.py reversible_convert_pivot_to_kif(): pivot_file={pivot_file} except={os.system.exc_info()[0]}")
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
