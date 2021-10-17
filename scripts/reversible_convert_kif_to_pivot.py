import glob
import os
import inspect
from scripts.change_place import change_place
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from scripts.convert_kifu_to_pivot import ConvertKifuToPivot
from scripts.convert_pivot_to_kifu import ConvertPivotToKifu
from scripts.copy_file import copy_file
from scripts.remove_all_temporary import remove_all_temporary
from scripts.convert_kif_to_kifu import ConvertKifToKifu
from scripts.convert_kifu_to_kif import ConvertKifuToKif
from scripts.test_lib import create_sha256_by_file_path


class ReversibleConvertKifToPivot():
    def __init__(self, source_template, debug=False, last_layer_folder='output', no_remove_output_pivot=False):
        if debug:
            print(
                f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] source_template=[{source_template}]")

        # (a) Layer 1. 入力フォルダ―
        self._first_layer_folder = 'input'
        self._first_layer_file_pattern = 'input/*.kif'

        # (a) Layer 2. 入力フォルダ―のコピーフォルダー
        self._layer2_folder = 'temporary/to-pivot/kif'
        self._layer2_file_pattern = 'temporary/to-pivot/kif/*.kif'

        self._layer2b_folder = 'temporary/to-pivot/kifu'

        # (a) Layer 3. Pivotフォルダ―(なし)

        # (a) 中間Layer.
        self._object_folder = 'temporary/to-pivot/object'

        # (a) Layer 4. 逆方向のフォルダ―
        self._layer4_folder = 'temporary/to-pivot/reverse-kifu'
        self._layer5_folder = 'temporary/to-pivot/reverse-kif'

        self._source_template = source_template
        self._debug = debug
        self._last_layer_folder = last_layer_folder
        self._no_remove_output_pivot = no_remove_output_pivot

    def clean_last_layer_folder(self):
        # (b-1) 最終レイヤーの フォルダー を空っぽにします
        clear_all_records_in_folder(self._last_layer_folder, echo=False)

    def outside_input_files(self):
        """レイヤー１フォルダ―にあるファイル"""
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
        if self._debug:
            print(
                f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] source_template=[{self._source_template}]")

        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(input_file)

        # (d-1) Shift-JIS から UTF-8 へ変更
        kif2kifu = ConvertKifToKifu()
        kifu_file = kif2kifu.convert_kif_to_kifu(
            input_file, output_folder=self._layer2b_folder, debug=self._debug)
        if kifu_file is None:
            print(
                f"[ERROR] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] (d-1) parse fail. input_file={input_file}")
            return None

        # (d-2) 目的のファイル（Pivot）へ変換
        kifu2pivot = ConvertKifuToPivot(
            debug=self._debug)
        object_file = kifu2pivot.convert_kifu_to_pivot(
            kifu_file, output_folder=self._object_folder)
        if object_file is None:
            print(
                f"[ERROR] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] (d-2) parse fail. kifu_file={kifu_file}")
            return None

        # ここから逆の操作を行います

        # (e-1)
        rev_kifu2pivot = ConvertPivotToKifu(object_file, debug=self._debug)
        reversed_kifu_file = rev_kifu2pivot.convert_pivot_to_kifu(
            output_folder=self._layer4_folder, desinated_template_name=self._source_template)
        if reversed_kifu_file is None:
            print(
                f"[ERROR] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] (e-1) parse fail. object_file={object_file}")
            return None

        # (e-2) Shift-JIS から UTF-8 へ変更
        rev_kif2kifu = ConvertKifuToKif()
        reversed_kif_file = rev_kif2kifu.convert_kifu_to_kif(
            reversed_kifu_file, output_folder=self._layer5_folder, debug=self._debug)
        if reversed_kif_file is None:
            print(
                f"[ERROR] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] (e-2) parse fail. reversed_kifu_file={reversed_kifu_file}")
            return None

        # (f) レイヤー５にあるファイルの SHA256 生成
        layer5_file_sha256 = create_sha256_by_file_path(reversed_kif_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer5_file_sha256:
            try:
                basename = os.path.basename(input_file)
            except:
                print(
                    f"Basename fail. (g) parse fail. input_file={input_file} except={os.system.exc_info()[0]}")
                raise

            # 不可逆な変換だが、とりあえず通します
            print(
                f"[WARNING] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Irreversible conversion. basename={basename}")

        # (h) 後ろから2. 中間レイヤー フォルダ―の中身を 最終レイヤー フォルダ―へコピーします
        copy = change_place(self._last_layer_folder, object_file)
        copy_file(object_file, copy, debug=self._debug)

        return object_file

    def clean_temporary(self):
        # (i) 後ろから1. 変換の途中で作ったファイルは削除します
        if not self._debug:
            remove_all_temporary(
                echo=False, no_remove_output_pivot=self._no_remove_output_pivot)
