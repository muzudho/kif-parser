import os
import glob
from scripts.change_place import change_place
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from scripts.copy_file import copy_file
from scripts.remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_kifu import convert_pivot_to_kifu
from scripts.convert_kifu_to_pivot import convert_kifu_to_pivot
from scripts.test_lib import create_sha256_by_file_path


class ReversibleConvertPivotToKifu():
    def __init__(self, debug=False, first_layer_folder='input', no_remove_output_pivot=False, template_name=""):
        # (a) Layer 1. 入力フォルダ―
        self._first_layer_folder = first_layer_folder
        self._first_layer_file_pattern = os.path.join(
            first_layer_folder, '*.json')

        # (a) Layer 2. 入力フォルダ―のコピーフォルダー
        self._layer2_folder = 'temporary/from-pivot/pivot'
        self._layer2_file_pattern = 'temporary/from-pivot/pivot/*[[]kifu-pivot[]].json'

        # (a) Layer 3. Pivotフォルダ―(なし)

        # (a) 中間Layer.
        self._middle_folder = 'temporary/from-pivot/object'

        # (a) Layer 4. 逆方向のフォルダ―
        self._layer4_folder = 'temporary/from-pivot/reverse-pivot'

        # (a) 最終Layer.
        self._last_layer_folder = 'output'

        self._debug = debug
        self._first_layer_folder = first_layer_folder
        self._no_remove_output_pivot = no_remove_output_pivot
        self._template_name = template_name

    def clean_last_layer_folder(self):
        # (b-1) 最終レイヤーの フォルダー を空っぽにします
        clear_all_records_in_folder(self._last_layer_folder, echo=False)

    def outside_input_files(self):
        return glob.glob(self._first_layer_file_pattern)

    @property
    def layer1_folder(self):
        """レイヤー１フォルダ―"""
        return self._first_layer_folder

    @property
    def layer2_folder(self):
        """レイヤー２フォルダ―"""
        return self._layer2_folder

    def target_files(self):
        """レイヤー２にあるファイルのリスト"""
        return glob.glob(self._layer2_file_pattern)

    def round_trip_translate(self, input_file):
        """
        Returns
        -------
        str
            最終成果ファイルへのパス
        """

        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(input_file)

        # (d-1) 目的のファイル（KIFU）へ変換
        object_file = convert_pivot_to_kifu(
            input_file, output_folder=self._middle_folder, template_name=self._template_name, debug=self._debug)
        if object_file is None:
            print(
                f"[ERROR] reversible_convert_pivot_to_kifu.py reversible_convert_pivot_to_kifu: (d-1) parse fail. input_file={input_file}")
            return None

        # ここから逆の操作を行います

        # (e-1)
        reversed_pivot_file = convert_kifu_to_pivot(
            object_file, output_folder=self._layer4_folder, debug=self._debug)
        if reversed_pivot_file is None:
            print(
                f"[ERROR] reversible_convert_pivot_to_kifu.py reversible_convert_pivot_to_kifu: (e-1) parse fail. object_file={object_file}")
            return None

        # (f) レイヤー４にあるファイルの SHA256 生成
        layer4_file_sha256 = create_sha256_by_file_path(
            reversed_pivot_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer4_file_sha256:
            try:
                basename = os.path.basename(input_file)
            except:
                print(
                    f"Basename fail. (g) input_file={input_file} except={os.system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"[WARNING] Irreversible conversion. basename={basename}")
            # continue

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へコピーします
        copy = change_place(self._last_layer_folder, object_file)
        copy_file(object_file, copy, debug=self._debug)

        return object_file

    def clean_temporary(self):
        # (i) 後ろから1. 変換の途中で作ったファイルは削除します
        if not self._debug:
            remove_all_temporary(
                echo=False, no_remove_output_pivot=self._no_remove_output_pivot)
