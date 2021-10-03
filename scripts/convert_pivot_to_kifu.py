import os
import json
import sys
import shutil
from collections import OrderedDict
from scripts.kifu_specification import player_phase_p, handicap_statement_p, \
    judge_statement1_p, judge_statement2_p, judge_statement3_p, move_statement_p, \
    variation_label_statement_p, start_time_statement_p, end_time_statement_p


def convert_pivot_to_kifu(pivot_file, output_folder, done_folder):
    # basename

    try:
        basename = os.path.basename(pivot_file)
    except:
        print(f"Error: pivot_file={pivot_file} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None, None

    kifuFile = ""

    with open(pivot_file, encoding='utf-8') as f:
        data = json.loads(f.read(), object_pairs_hook=OrderedDict)

    move_section_flag = False
    kifu_text = ""

    # JSON to KIFU
    for row_number, row_data in data.items():

        if row_data["type"] == "comment":
            comment = row_data["comment"]
            kifu_text += f'#{comment}\n'
        elif row_data["type"] == "explanation":
            explanation = row_data["explanation"]
            kifu_text += f"*{explanation}\n"
        elif row_data["type"] == "bookmark":
            bookmark = row_data["bookmark"]
            kifu_text += f"&{bookmark}\n"
        elif row_data["type"] == "move":
            # 指し手
            if not move_section_flag:
                kifu_text += "手数----指手---------消費時間--\n"
                move_section_flag = True

            kifu_text += move_statement_p.from_pivot(
                moves=row_data["moves"],
                elapsedTime=row_data["elapsedTime"],
                totalElapsedTime=row_data["totalElapsedTime"],
                move=row_data["move"])
        elif row_data["type"] == "startTime":
            kifu_text += start_time_statement_p.from_pivot(
                row_data["startTime"])
        elif row_data["type"] == "endTime":
            kifu_text += end_time_statement_p.from_pivot(
                row_data["endTime"])
        elif row_data["type"] == "handicap":
            kifu_text += handicap_statement_p.from_pivot(row_data["handicap"])
        elif row_data["type"] == "player":
            player_phase = player_phase_p.from_pivot(
                row_data["playerPhase"])
            player_name = row_data["playerName"]
            kifu_text += f"{player_phase}：{player_name}\n"
        elif row_data["type"] == "variationLabel":
            moves = variation_label_statement_p.from_pivot(
                row_data["moves"])
            kifu_text += variation_label_statement_p.from_pivot(moves)
        elif row_data["type"] == "result":
            if "reason" in row_data:
                # Example: `まで52手で時間切れにより後手の勝ち`
                moves = row_data["moves"]
                reason = row_data['reason']
                winner = row_data["winner"]
                judge = row_data["judge"]
                kifu_text += judge_statement3_p.from_pivot(
                    moves, reason, winner, judge)
            elif "winner" in row_data:
                # Example: `まで64手で後手の勝ち`
                moves = row_data["moves"]
                winner = row_data["winner"]
                judge = row_data["judge"]
                kifu_text += judge_statement1_p.from_pivot(
                    moves, winner, judge)
            else:
                # Example: `まで63手で中断`
                moves = row_data["moves"]
                judge = row_data["judge"]
                kifu_text += judge_statement2_p.from_pivot(
                    moves, judge)
        elif row_data["type"] == "appendix":
            # 元の `.kifu` には無い、このアプリケーションが付けた情報なので、無視します
            pass
        else:
            # Error
            print(
                f"Error: pivot_to_kifu.py unimplemented row_number={row_number} row_data={row_data}")
            return None, None

    # New .kifu ファイル出力
    kifuFile = os.path.join(output_folder, f"{stem}.kifu")
    with open(kifuFile, mode='w', encoding='utf-8') as fOut:
        fOut.write(kifu_text)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    done_pivot_file = shutil.move(
        pivot_file, os.path.join(done_folder, basename))

    return kifuFile, done_pivot_file
