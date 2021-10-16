import glob
from os import system
import os
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from scripts.remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import convert_kif_to_kifu
from scripts.convert_kifu_to_kif import convert_kifu_to_kif
from scripts.copy_file_to_folder import copy_file_to_folder
from scripts.test_lib import create_sha256_by_file_path


class ReversibleConvertKifToKifu():
    def __init__(self, debug=False, no_remove_output_pivot=False):
        # (a) Layer 1. 入力フォルダ―
        self._first_layer_file_pattern = './input/*.kif'

        # (a) Layer 2. 入力フォルダ―のコピーフォルダー
        self._layer2_folder = 'temporary/no-pivot/kif'
        self._layer2_file_pattern = 'temporary/no-pivot/kif/*.kif'

        # (a) Layer 3. Pivotフォルダ―(なし)

        # (a) 中間Layer.
        self._object_folder = 'temporary/no-pivot/object'

        # (a) Layer 4. 逆方向のフォルダ―
        self._layer4_folder = 'temporary/no-pivot/reverse-kif'

        # (a) 最終Layer.
        self._last_layer_folder = 'output'

        self._debug = debug
        self._no_remove_output_pivot = no_remove_output_pivot

    def clean_last_layer_folder(self):
        # (b-1) 最終レイヤーの フォルダー を空っぽにします
        clear_all_records_in_folder(self._last_layer_folder, echo=False)

    def outside_input_files(self):
        """レイヤー１フォルダ―にあるファイル"""
        return glob.glob(self._first_layer_file_pattern)

    @property
    def layer2_folder(self):
        """レイヤー２フォルダ―"""
        return self._layer2_folder

    def target_files(self):
        """レイヤー２にあるファイルのリスト"""
        return glob.glob(self._layer2_file_pattern)

    def round_trip_translate(self, input_file):
        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(input_file)

        # (d-1) 目的のファイル（KIFU UTF-8）へ変換
        object_file = convert_kif_to_kifu(
            input_file, output_folder=self._object_folder)
        if object_file is None:
            print(
                f"[ERROR] reversible_convert_kif_to_kifu.py reversible_convert_kif_to_kifu(): (d-1) parse fail. input_file=[{input_file}]")
            return

        # ここから逆の操作を行います

        # (e-1) UTF-8 から Shift-JIS へ変換
        reversed_kif_file = convert_kifu_to_kif(
            object_file, output_folder=self._layer4_folder)

        # (f) レイヤー４にあるファイルの SHA256 生成
        layer4_file_sha256 = create_sha256_by_file_path(reversed_kif_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer4_file_sha256:
            try:
                basename = os.path.basename(input_file)
            except:
                print(
                    f"[ERROR] reversible_convert_kif_to_kifu.py reversible_convert_kif_to_kifu(): (g) parse fail. input_file={input_file} except={system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(f"[WARNING] Irreversible conversion. basename={basename}")

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へコピーします
        copy_file_to_folder(
            object_file, self._last_layer_folder, debug=self._debug)

    def clean_temporary(self):
        # (i) 後ろから1. 変換の途中で作ったファイルは削除します
        if not self._debug:
            remove_all_temporary(
                echo=False, no_remove_output_pivot=self._no_remove_output_pivot)
