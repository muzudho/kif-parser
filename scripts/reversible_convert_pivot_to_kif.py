import glob
import os
import inspect
from scripts.change_place import change_place
from scripts.clear_all_records_in_folder import clear_all_records_in_folder
from scripts.copy_file import copy_file
from scripts.remove_all_temporary import remove_all_temporary
from scripts.convert_pivot_to_kifu import ConvertPivotToKifu
from scripts.convert_kifu_to_kif import ConvertKifuToKif
from scripts.test_lib import create_sha256_by_file_path
from scripts.convert_kif_to_kifu import ConvertKifToKifu
from scripts.convert_kifu_to_pivot import ConvertKifuToPivot


class ReversibleConvertPivotToKif():
    def __init__(self, destination_template, debug=False, first_layer_folder='input', no_remove_output_pivot=False):
        if debug:
            print(
                f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] destination_template=[{destination_template}]")

        # (a) Layer 1. 入力フォルダ―
        self._first_layer_folder = first_layer_folder
        self._first_layer_file_pattern = os.path.join(
            first_layer_folder, '*.json')

        # (a) Layer 2. 入力フォルダ―のコピーフォルダー
        self._layer2_folder = 'temporary/from-pivot/pivot'
        self._layer2_file_pattern = 'temporary/from-pivot/pivot/*[[]kifu-pivot[]].json'
        self._layer2b_folder = 'temporary/from-pivot/kifu'

        # (a) Layer 3. Pivotフォルダ―(なし)

        # (a) 中間Layer.
        self._middle_folder = 'temporary/from-pivot/object'

        # (a) Layer 4. 逆入力フォルダ―
        self._layer4_folder = 'temporary/from-pivot/reverse-kifu'
        self._layer5_folder = 'temporary/from-pivot/reverse-pivot'

        # (a) 最終Layer.
        self._last_layer_folder = 'output'

        self._destination_template = destination_template
        self._debug = debug
        self._first_layer_folder = first_layer_folder
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
                f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] destination_template=[{self._destination_template}]")

        # (c) レイヤー２にあるファイルの SHA256 生成
        layer2_file_sha256 = create_sha256_by_file_path(input_file)

        # (d-1) KIFUへ変換
        pivot2kifu = ConvertPivotToKifu(
            desinated_template_name=self._destination_template, debug=self._debug)
        kifu_file = pivot2kifu.convert_file_from_pivot_to_kifu(
            input_file, output_folder=self._layer2b_folder)
        if kifu_file is None:
            print(
                f"[ERROR] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Parse fail. input_file={input_file}")
            return None

        # (d-2) 目的のファイル(KIF Shift-JIS)へ変換
        kifu2kif = ConvertKifuToKif()
        object_file = kifu2kif.convert_kifu_to_kif(
            kifu_file, output_folder=self._middle_folder, debug=self._debug)
        if object_file is None:
            print(
                f"[ERROR] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Parse fail. input_file={input_file}")
            return None

        # ここから逆の操作を行います

        # (e-1)
        rev_kifu2kif = ConvertKifToKifu()
        reversed_kifu_file = rev_kifu2kif.convert_kif_to_kifu(
            object_file, output_folder=self._layer4_folder, debug=self._debug)
        if reversed_kifu_file is None:
            print(
                f"[ERROR] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Parse fail. input_file={input_file}")
            return None

        # (e-2)
        rev_pivot2kifu = ConvertKifuToPivot(
            debug=self._debug)
        reversed_pivot_file = rev_pivot2kifu.convert_file_from_kifu_to_pivot(
            reversed_kifu_file, output_folder=self._layer5_folder)
        if reversed_pivot_file is None:
            print(
                f"[ERROR] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Parse fail. input_file={input_file}")
            return None

        # (f) レイヤー５にあるファイルの SHA256 生成
        layer5_file_sha256 = create_sha256_by_file_path(
            reversed_pivot_file)

        # (g) 一致比較
        if layer2_file_sha256 != layer5_file_sha256:
            try:
                basename = os.path.basename(input_file)
            except:
                print(
                    f"Basename fail. input_file={input_file} except={os.system.exc_info()[0]}")
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
