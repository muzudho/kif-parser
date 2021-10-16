import glob
from os import system
import os
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.test_lib import create_sha256_by_file_path


class ReversibleConvertKifToPivot():
    def __init__(self, debug=False, last_layer_folder='output', no_remove_output_pivot=False, template_name=""):
        # (a) Layer 1. 入力フォルダ―
        self._first_layer_file_pattern = './input/*.kif'

        # (a) Layer 2. 入力フォルダ―のコピーフォルダー
        self._layer2_folder = 'temporary/to-pivot/kif'
        self._layer2_file_pattern = './temporary/to-pivot/kif/*.kif'

        self._layer2b_folder = 'temporary/to-pivot/kifu'

        # (a) Layer 3. Pivotフォルダ―(なし)

        # (a) 中間Layer.
        self._object_folder = 'temporary/to-pivot/object'

        # (a) Layer 4. 逆方向のフォルダ―
        self._layer4_folder = 'temporary/to-pivot/reverse-kifu'
        self._layer5_folder = 'temporary/to-pivot/reverse-kif'

        self._debug = debug
        self._last_layer_folder = last_layer_folder
        self._no_remove_output_pivot = no_remove_output_pivot
        self._template_name = template_name

    def reversible_convert_kif_to_pivot_ready(self):
        # (b-1) 最終レイヤーの フォルダー を空っぽにします
        if not self._debug:
            clear_all_records_in_folder(self._last_layer_folder, echo=False)

        # (b-2) レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
        input_files = glob.glob(self._first_layer_file_pattern)
        for input_file in input_files:
            copy_file_to_folder(input_file, self._layer2_folder)

    def target_files(self):
        """レイヤー２にあるファイルのリスト"""
        return glob.glob(self._layer2_file_pattern)

    def reversible_convert_kif_to_pivot_one(self, kif_file):
        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(kif_file)

        # (d-1) Shift-JIS から UTF-8 へ変更
        kifu_file = convert_kif_to_kifu(
            kif_file, output_folder=self._layer2b_folder)
        if kifu_file is None:
            print(
                f"[ERROR] reversible_convert_kif_to_pivot.py reversible_convert_kifu_to_pivot: (d-1) parse fail. kif_file={kif_file}")
            return

        # (d-2) 目的のファイル（Pivot）へ変換
        object_file = convert_kifu_to_pivot(
            kifu_file, output_folder=self._object_folder)
        if object_file is None:
            print(
                f"[ERROR] reversible_convert_kif_to_pivot.py reversible_convert_kifu_to_pivot: (d-2) parse fail. kifu_file={kifu_file}")
            return

        # ここから逆の操作を行います

        # (e-1)
        reversed_kifu_file = convert_pivot_to_kifu(
            object_file, output_folder=self._layer4_folder, template_name=self._template_name)
        if reversed_kifu_file is None:
            print(
                f"[ERROR] reversible_convert_kif_to_pivot.py reversible_convert_kifu_to_pivot: (e-1) parse fail. object_file={object_file}")
            return

        # (e-2) Shift-JIS から UTF-8 へ変更
        reversed_kif_file = convert_kifu_to_kif(
            reversed_kifu_file, output_folder=self._layer5_folder)
        if reversed_kif_file is None:
            print(
                f"[ERROR] reversible_convert_kif_to_pivot.py reversible_convert_kifu_to_pivot: (e-2) parse fail. reversed_kifu_file={reversed_kifu_file}")
            return

        # (f) レイヤー５にあるファイルの SHA256 生成
        layer5_file_sha256 = create_sha256_by_file_path(reversed_kif_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer5_file_sha256:
            try:
                basename = os.path.basename(kif_file)
            except:
                print(
                    f"[ERROR] reversible_convert_kif_to_pivot.py reversible_convert_kifu_to_pivot: (g) parse fail. kif_file={kif_file} except={system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"[WARNING] Irreversible conversion. basename={basename}")

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へコピーします
        copy_file_to_folder(object_file, self._last_layer_folder)

    def reversible_convert_kif_to_pivot_clean(self):
        # (i) 後ろから1. 変換の途中で作ったファイルは削除します
        if not self._debug:
            remove_all_temporary(
                echo=False, no_remove_output_pivot=self._no_remove_output_pivot)
