import glob
import os
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from scripts.remove_all_temporary import remove_all_temporary
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.test_lib import create_sha256_by_file_path


class ReversibleConvertKifuToPivot():
    def __init__(self, debug=False, last_layer_folder='output', no_remove_output_pivot=False, template_name=""):
        # (a) Layer 1. 入力フォルダ―
        self._first_layer_file_pattern = './input/*.kifu'

        # (a) Layer 2. 入力フォルダ―のコピーフォルダー
        self._layer2_folder = 'temporary/to-pivot/kifu'
        self._layer2_file_pattern = './temporary/to-pivot/kifu/*.kifu'

        # (a) Layer 3. Pivotフォルダ―(なし)

        # (a) 中間Layer.
        self._object_folder = 'temporary/to-pivot/object'

        # (a) Layer 4. 逆入力フォルダ―
        self._layer4_folder = 'temporary/to-pivot/reverse-kifu'

        self._debug = debug
        self._last_layer_folder = last_layer_folder
        self._no_remove_output_pivot = no_remove_output_pivot
        self._template_name = template_name

    def ready_folder(self):
        # (b-1) 最終レイヤーの フォルダー を空っぽにします
        clear_all_records_in_folder(self._last_layer_folder, echo=False)

        # (b-2) レイヤー１フォルダ―にあるファイルを レイヤー２フォルダ―へコピーします
        input_files = glob.glob(self._first_layer_file_pattern)
        for input_file in input_files:
            copy_file_to_folder(input_file, self._layer2_folder)

    def target_files(self):
        """レイヤー２にあるファイルのリスト"""
        return glob.glob(self._layer2_file_pattern)

    def round_trip_translate(self, input_file):

        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(input_file)

        # (d-1) 目的のファイル（Pivot）へ変換
        object_file = convert_kifu_to_pivot(
            input_file, output_folder=self._object_folder)
        if object_file is None:
            print(
                f"[ERROR] reversible_convert_kifu_to_pivot.py reversible_convert_kifu_to_pivot(): (d-1) parse fail. input_file={input_file}")
            return

        # ここから逆の操作を行います

        # (e-1)
        reversed_kifu_file = convert_pivot_to_kifu(
            object_file, output_folder=self._layer4_folder, template_name=self._template_name)
        if reversed_kifu_file is None:
            print(
                f"[ERROR] reversible_convert_kifu_to_pivot.py reversible_convert_kifu_to_pivot(): (e-1) parse fail. input_file={input_file}")
            return

        # (f) レイヤー４にあるファイルの SHA256 生成
        layer4_file_sha256 = create_sha256_by_file_path(reversed_kifu_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer4_file_sha256:
            try:
                basename = os.path.basename(input_file)
            except:
                print(
                    f"Error: input_file={input_file} except={os.system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"[WARNING] Irreversible conversion to-pivot. basename={basename}")

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へコピーします
        copy_file_to_folder(object_file, self._last_layer_folder)

    def clean_temporary(self):
        # (i) 後ろから1. 変換の途中で作ったファイルは削除します
        if not self._debug:
            remove_all_temporary(
                echo=False, no_remove_output_pivot=self._no_remove_output_pivot)
