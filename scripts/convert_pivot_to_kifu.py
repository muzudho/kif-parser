import os
import inspect
import json
import sys
from collections import OrderedDict
from scripts.shogidokoro_template import ShogidokoroTemplate
from scripts.shogigui_template import ShogiguiTemplate


class ConvertPivotToKifu():

    def __init__(self, desinated_template_name, debug=False):
        """
        Parameters
        ----------
        desinated_template_name : str
            往復変換のときは source_template と destination_template のどちらかよく確認してください
        """
        self._debug = debug
        self._desinated_template_name = desinated_template_name

        if self._desinated_template_name == "shogigui":
            # 将棋GUIテンプレート
            self._template_obj = ShogiguiTemplate()
        else:
            # 将棋所テンプレート（デフォルト）
            self._template_obj = ShogidokoroTemplate()

    def convert_text_from_pivot_to_kifu(self, in_text):
        data = json.loads(in_text, object_pairs_hook=OrderedDict)

        # .kifu テキストを作ります
        out_text = ""

        best_rate = 0
        shogidokoro_rate = 1
        shogigui_rate = 0

        # 行パーサーです
        for row_number, row_data in data.items():

            if row_data["type"] == "comment":
                out_text += self._template_obj.comment_row(row_data)
            elif row_data["type"] == "explain":
                out_text += self._template_obj.explain_row(row_data)
            elif row_data["type"] == "bookmark":
                out_text += self._template_obj.bookmark_row(row_data)
            elif row_data["type"] == "movesHeader":
                out_text += self._template_obj.moves_header_row(row_data)
            elif row_data["type"] == "move":
                out_text += self._template_obj.move_row(row_data)
            elif row_data["type"] == "kvPair":
                out_text += self._template_obj.key_value_pair_row(row_data)
            elif row_data["type"] == "result":
                out_text += self._template_obj.result_row(row_data)
            elif row_data["type"] == "metadata":
                if self._desinated_template_name == "":
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
                            self._template_obj = ShogidokoroTemplate()
                            best_rate = shogidokoro_rate

                    if "shogigui" in generating_software_is_probably:
                        shogigui_rate = int(
                            generating_software_is_probably["shogigui"])
                        # ShogiGUIテンプレート
                        if best_rate < shogigui_rate:
                            if self._debug:
                                print(
                                    f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] ShogiGUIテンプレートに変えます")
                            self._template_obj = ShogiguiTemplate()
                            best_rate = shogigui_rate
            else:
                # Error
                print(
                    f"[Error] {os.path.basename(__file__)} unimplemented row_number={row_number} row_data={row_data}")
                return None

        # 最終行に空行が続くケースもあります
        out_text += self._template_obj.end_of_file()

        return out_text

    def convert_file_from_pivot_to_kifu(self, pivot_file, output_folder):
        # basename
        try:
            basename = os.path.basename(pivot_file)
        except:
            print(
                f"Basename fail. pivot_file={pivot_file} except={sys.exc_info()[0]}")
            raise

        if not basename.lower().endswith('[kifu-pivot].json'):
            return None
        stem, _extention = os.path.splitext(basename)

        # Pivotファイル（JSON形式）を読込みます
        with open(pivot_file, encoding='utf-8') as f:
            in_text = f.read()

        out_text = self.convert_text_from_pivot_to_kifu(in_text)
        if not out_text:
            # Error
            print(
                f"[Error] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Convert file. pivot_file=[{pivot_file}]")
            return None

        # stem の末尾に `[kifu-pivot]` が付いているので外します
        stem = ConvertPivotToKifu.remove_suffix(stem, '[kifu-pivot]')

        # stem の末尾に `[shogidokoro]` が付いていたら外します
        stem = ConvertPivotToKifu.remove_suffix(stem, '[shogidokoro]')

        # stem の末尾に `[shogigui]` が付いていたら外します
        stem = ConvertPivotToKifu.remove_suffix(stem, '[shogigui]')

        # New .kifu ファイル出力
        # stem の末尾に `[テンプレート名]` を付けます
        out_path = os.path.join(
            output_folder, f"{stem}[{self._template_obj.name}].kifu")

        if self._debug:
            print(
                f"[DEBUG] [{os.path.basename(__file__)} {inspect.currentframe().f_back.f_code.co_name}] Write to [{out_path}] desinated_template_name=[{self._desinated_template_name}]")

        with open(out_path, mode='w', encoding='utf-8') as f_out:
            f_out.write(out_text)

        return out_path

    @classmethod
    def remove_suffix(clazz, stem, suffix):
        """stem の末尾に suffix が付いていたら外します"""

        if not stem.endswith(suffix):
            return stem

        return stem[:-len(suffix)]
