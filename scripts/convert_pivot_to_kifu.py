import os
import json
import sys
from collections import OrderedDict
from scripts.kifu_specification import moves_header_row_p, \
    move_row_p, \
    key_value_pair_row_p, result_row_p
from scripts.shogidokoro_template import ShogidokoroTemplate


def convert_pivot_to_kifu(pivot_file, output_folder):
    # basename
    try:
        basename = os.path.basename(pivot_file)
    except:
        print(f"Error: pivot_file={pivot_file} except={sys.exc_info()[0]}")
        raise

    if not basename.lower().endswith('[kifu-pivot].json'):
        return None
    stem, _extention = os.path.splitext(basename)

    kifuFile = ""

    # Pivotファイル（JSON形式）を読込みます
    with open(pivot_file, encoding='utf-8') as f:
        data = json.loads(f.read(), object_pairs_hook=OrderedDict)

    # .kifu テキストを作ります
    kifu_text = ""

    # ビュー
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
            kifu_text += moves_header_row_p.from_pivot(row_data)
        elif row_data["type"] == "move":
            kifu_text += move_row_p.from_pivot(row_data)
        elif row_data["type"] == "kvPair":
            kifu_text += key_value_pair_row_p.from_pivot(row_data)
        elif row_data["type"] == "result":
            kifu_text += result_row_p.from_pivot(row_data)
        elif row_data["type"] == "metadata":
            # 元の `.kifu` には無い、このアプリケーションが付けた情報なので、無視します
            pass
        else:
            # Error
            print(
                f"Error: pivot_to_kifu.py unimplemented row_number={row_number} row_data={row_data} pivot_file=[{pivot_file}]")
            return None

    # stem の末尾に `[kifu-pivot]` が付いているので外します
    if not stem.endswith('[kifu-pivot]'):
        print(f"Error stem=[{stem}]")
        return None

    stem = stem[:-len('[kifu-pivot]')]

    # New .kifu ファイル出力
    kifuFile = os.path.join(output_folder, f"{stem}.kifu")
    with open(kifuFile, mode='w', encoding='utf-8') as fOut:
        fOut.write(kifu_text)

    return kifuFile
