import os
import json
import sys
from collections import OrderedDict
from scripts.kifu_specification import comment_p, explain_p, bookmark_p, \
    moves_header_statement_p, \
    judge_statement1_p, judge_statement2_p, judge_statement3_p, move_statement_p, \
    key_value_pair_statement_p


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
            kifu_text += comment_p.from_pivot(row_data)
        elif row_data["type"] == "explain":
            kifu_text += explain_p.from_pivot(row_data)
        elif row_data["type"] == "bookmark":
            kifu_text += bookmark_p.from_pivot(row_data)
        elif row_data["type"] == "movesHeader":
            kifu_text += moves_header_statement_p.from_pivot(row_data)
        elif row_data["type"] == "move":
            kifu_text += move_statement_p.from_pivot(row_data)
        elif row_data["type"] == "kvPair":
            kifu_text += key_value_pair_statement_p.from_pivot(row_data)
        elif row_data["type"] == "result":
            if "reason" in row_data:
                # Example: `まで52手で時間切れにより後手の勝ち`
                num = row_data["num"]  # Move num
                reason = row_data['reason']
                winner = row_data["winner"]
                judge = row_data["judge"]
                kifu_text += judge_statement3_p.from_pivot(
                    num, reason, winner, judge)
            elif "winner" in row_data:
                # Example: `まで64手で後手の勝ち`
                num = row_data["num"]
                winner = row_data["winner"]
                judge = row_data["judge"]
                kifu_text += judge_statement1_p.from_pivot(
                    num, winner, judge)
            else:
                # Example: `まで63手で中断`
                num = row_data["num"]
                judge = row_data["judge"]
                kifu_text += judge_statement2_p.from_pivot(
                    num, judge)
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
