import os
import json
import sys
from collections import OrderedDict
from scripts.shogidokoro_template import ShogidokoroTemplate
from scripts.shogigui_template import ShogiguiTemplate


def convert_pivot_to_kifu(pivot_file, output_folder, template_name="", debug=False):
    # basename
    try:
        basename = os.path.basename(pivot_file)
    except:
        print(f"Error: pivot_file={pivot_file} except={sys.exc_info()[0]}")
        raise

    if not basename.lower().endswith('[kifu-pivot].json'):
        return None
    stem, _extention = os.path.splitext(basename)

    # Pivotファイル（JSON形式）を読込みます
    with open(pivot_file, encoding='utf-8') as f:
        data = json.loads(f.read(), object_pairs_hook=OrderedDict)

    # .kifu テキストを作ります
    kifu_text = ""

    best_rate = 0
    shogidokoro_rate = 1
    shogigui_rate = 0
    if template_name == "shogigui":
        # 将棋GUIテンプレート
        template = ShogiguiTemplate()
    else:
        # 将棋所テンプレート（デフォルト）
        template = ShogidokoroTemplate()

    # 行パーサーです
    for row_number, row_data in data.items():

        if row_data["type"] == "comment":
            kifu_text += template.comment_row(row_data)
        elif row_data["type"] == "explain":
            kifu_text += template.explain_row(row_data)
        elif row_data["type"] == "bookmark":
            kifu_text += template.bookmark_row(row_data)
        elif row_data["type"] == "movesHeader":
            kifu_text += template.moves_header_row(row_data)
        elif row_data["type"] == "move":
            kifu_text += template.move_row(row_data)
        elif row_data["type"] == "kvPair":
            kifu_text += template.key_value_pair_row(row_data)
        elif row_data["type"] == "result":
            kifu_text += template.result_row(row_data)
        elif row_data["type"] == "metadata":
            if template_name == "":
                # テンプレート名が未指定なら、自動で選びます
                generating_software_is_probably = row_data["generatingSoftwareIsProbably"]
                if "shogidokoro" in generating_software_is_probably:
                    shogidokoro_rate = int(
                        generating_software_is_probably["shogidokoro"])
                    # 将棋所テンプレート
                    if best_rate < shogidokoro_rate:
                        # print(f"[DEBUG] 将棋所テンプレートに変えます")
                        template = ShogidokoroTemplate()
                        best_rate = shogidokoro_rate

                if "shogigui" in generating_software_is_probably:
                    shogigui_rate = int(
                        generating_software_is_probably["shogigui"])
                    # ShogiGUIテンプレート
                    if best_rate < shogigui_rate:
                        # print(f"[DEBUG] ShogiGUIテンプレートに変えます")
                        template = ShogiguiTemplate()
                        best_rate = shogigui_rate
        else:
            # Error
            print(
                f"Error: pivot_to_kifu.py unimplemented row_number={row_number} row_data={row_data} pivot_file=[{pivot_file}]")
            return None

    # 最終行に空行が続くケースもあります
    kifu_text += template.end_of_file()

    # stem の末尾に `[kifu-pivot]` が付いているので外します
    stem = remove_suffix(stem, '[kifu-pivot]')

    # stem の末尾に `[shogidokoro]` が付いていたら外します
    stem = remove_suffix(stem, '[shogidokoro]')

    # stem の末尾に `[shogigui]` が付いていたら外します
    stem = remove_suffix(stem, '[shogigui]')

    # New .kifu ファイル出力
    # stem の末尾に `[テンプレート名]` を付けます
    out_path = os.path.join(output_folder, f"{stem}[{template.name}].kifu")

    if debug:
        print(
            f"[DEBUG] convert_pivot_to_kifu.py convert_pivot_to_kifu(): Write to [{out_path}]")

    with open(out_path, mode='w', encoding='utf-8') as f_out:
        f_out.write(kifu_text)

    return out_path


def remove_suffix(stem, suffix):
    """stem の末尾に suffix が付いていたら外します"""

    if not stem.endswith(suffix):
        return stem

    return stem[:-len(suffix)]
