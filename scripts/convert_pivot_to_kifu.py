import os
import inspect
import json
import sys
from collections import OrderedDict
from scripts.shogidokoro_template import ShogidokoroTemplate
from scripts.shogigui_template import ShogiguiTemplate


class ConvertPivotToKifu():

    def __init__(self, input_file, debug=False):
        self._input_file = input_file
        self._debug = debug
        pass

    def _read_input(self):
        # basename
        try:
            basename = os.path.basename(self._input_file)
        except:
            print(
                f"Basename fail. input_file={self._input_file} except={sys.exc_info()[0]}")
            raise

        if not basename.lower().endswith('[kifu-pivot].json'):
            return None, None
        stem, _extention = os.path.splitext(basename)

        # Pivotファイル（JSON形式）を読込みます
        with open(self._input_file, encoding='utf-8') as f:
            data = json.loads(f.read(), object_pairs_hook=OrderedDict)

        return stem, data

    def convert_pivot_to_kifu(self, output_folder, desinated_template_name=""):
        """
        Parameters
        ----------
        desinated_template_name : str
            往復変換のときは source_template と destination_template のどちらかよく確認してください
        """
        stem, data = self._read_input()

        # .kifu テキストを作ります
        kifu_text = ""

        best_rate = 0
        shogidokoro_rate = 1
        shogigui_rate = 0
        if desinated_template_name == "shogigui":
            # 将棋GUIテンプレート
            template_obj = ShogiguiTemplate()
        else:
            # 将棋所テンプレート（デフォルト）
            template_obj = ShogidokoroTemplate()

        # 行パーサーです
        for row_number, row_data in data.items():

            if row_data["type"] == "comment":
                kifu_text += template_obj.comment_row(row_data)
            elif row_data["type"] == "explain":
                kifu_text += template_obj.explain_row(row_data)
            elif row_data["type"] == "bookmark":
                kifu_text += template_obj.bookmark_row(row_data)
            elif row_data["type"] == "movesHeader":
                kifu_text += template_obj.moves_header_row(row_data)
            elif row_data["type"] == "move":
                kifu_text += template_obj.move_row(row_data)
            elif row_data["type"] == "kvPair":
                kifu_text += template_obj.key_value_pair_row(row_data)
            elif row_data["type"] == "result":
                kifu_text += template_obj.result_row(row_data)
            elif row_data["type"] == "metadata":
                if desinated_template_name == "":
                    # テンプレート名が未指定なら、自動で選びます
                    generating_software_is_probably = row_data["generatingSoftwareIsProbably"]
                    if "shogidokoro" in generating_software_is_probably:
                        shogidokoro_rate = int(
                            generating_software_is_probably["shogidokoro"])
                        # 将棋所テンプレート
                        if best_rate < shogidokoro_rate:
                            if self._debug:
                                print(
                                    f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] 将棋所テンプレートに変えます")
                            template_obj = ShogidokoroTemplate()
                            best_rate = shogidokoro_rate

                    if "shogigui" in generating_software_is_probably:
                        shogigui_rate = int(
                            generating_software_is_probably["shogigui"])
                        # ShogiGUIテンプレート
                        if best_rate < shogigui_rate:
                            if self._debug:
                                print(
                                    f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] ShogiGUIテンプレートに変えます")
                            template_obj = ShogiguiTemplate()
                            best_rate = shogigui_rate
            else:
                # Error
                print(
                    f"[Error] {os.path.basename(__file__)} unimplemented row_number={row_number} row_data={row_data} input_file=[{self._input_file}]")
                return None

        # 最終行に空行が続くケースもあります
        kifu_text += template_obj.end_of_file()

        # stem の末尾に `[kifu-pivot]` が付いているので外します
        stem = ConvertPivotToKifu.remove_suffix(stem, '[kifu-pivot]')

        # stem の末尾に `[shogidokoro]` が付いていたら外します
        stem = ConvertPivotToKifu.remove_suffix(stem, '[shogidokoro]')

        # stem の末尾に `[shogigui]` が付いていたら外します
        stem = ConvertPivotToKifu.remove_suffix(stem, '[shogigui]')

        # New .kifu ファイル出力
        # stem の末尾に `[テンプレート名]` を付けます
        out_path = os.path.join(
            output_folder, f"{stem}[{template_obj.name}].kifu")

        if self._debug:
            print(
                f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Write to [{out_path}] desinated_template_name=[{desinated_template_name}]")

        with open(out_path, mode='w', encoding='utf-8') as f_out:
            f_out.write(kifu_text)

        return out_path

    @classmethod
    def remove_suffix(clazz, stem, suffix):
        """stem の末尾に suffix が付いていたら外します"""

        if not stem.endswith(suffix):
            return stem

        return stem[:-len(suffix)]
