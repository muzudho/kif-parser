import os
import json
import sys
from collections import OrderedDict
from scripts.kifu_specification import comment_row_p, explain_row_p, bookmark_row_p, \
    moves_header_statement_p, \
    move_statement_p, \
    key_value_pair_row_p, result_statement_p


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

    # 行パーサーです
    for row_number, row_data in data.items():

        if row_data["type"] == "comment":
            kifu_text += comment_row_p.from_pivot(row_data)
        elif row_data["type"] == "explain":
            kifu_text += explain_row_p.from_pivot(row_data)
        elif row_data["type"] == "bookmark":
            kifu_text += bookmark_row_p.from_pivot(row_data)
        elif row_data["type"] == "movesHeader":
            kifu_text += moves_header_statement_p.from_pivot(row_data)
        elif row_data["type"] == "move":
            kifu_text += move_statement_p.from_pivot(row_data)
        elif row_data["type"] == "kvPair":
            kifu_text += key_value_pair_row_p.from_pivot(row_data)
        elif row_data["type"] == "result":
            kifu_text += result_statement_p.from_pivot(row_data)
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

    stem = stem[:-6]

    # New .kifu ファイル出力
    kifuFile = os.path.join(output_folder, f"{stem}.kifu")
    with open(kifuFile, mode='w', encoding='utf-8') as fOut:
        fOut.write(kifu_text)

    return kifuFile
