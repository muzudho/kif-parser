import os
import glob
import json
import sys
import shutil
from collections import OrderedDict
from scripts.kifu_specification import player_phase_p, handicap_p, \
    judge_statement1_p, judge_statement2_p, judge_statement3_p, move_statement_p, \
    variation_label_statement_p
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output


def copy_pivot_from_input(output_folder='temporary/kif'):
    """inputフォルダーにある `*.json` ファイルを pivotフォルダーへコピーします"""

    input_files = glob.glob("./input/*.pivot")
    for input_file in input_files:
        # basename
        try:
            basename = os.path.basename(input_file)
        except:
            print(f"Error: input_file={input_file} except={sys.exc_info()[0]}")
            raise

        copy_file = os.path.join(output_folder, basename)
        shutil.copyfile(input_file, copy_file)


def convert_pivot_to_kifu(pivot_file, output_folder='temporary/kifu', done_folder='temporary/pivot-done'):
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

            if row_data["type"] == "Comment":
                comment = row_data["comment"]
                kifu_text += f'#{comment}\n'
            elif row_data["type"] == "Explanation":
                explanation = row_data["explanation"]
                kifu_text += f"*{explanation}\n"
            elif row_data["type"] == "Bookmark":
                bookmark = row_data["bookmark"]
                kifu_text += f"&{bookmark}\n"
            elif row_data["type"] == "Move":
                # 指し手
                if not move_section_flag:
                    kifu_text += "手数----指手---------消費時間--\n"
                    move_section_flag = True

                kifu_text += move_statement_p.from_pivot(
                    moves=row_data["moves"],
                    elapsedTime=row_data["elapsedTime"],
                    totalElapsedTime=row_data["totalElapsedTime"],
                    move=row_data["move"])
            elif row_data["type"] == "Handicap":
                handicap = handicap_p.from_pivot(row_data["handicap"])
                kifu_text += f"手合割：{handicap}\n"
            elif row_data["type"] == "Player":
                player_phase = player_phase_p.from_pivot(
                    row_data["playerPhase"])
                player_name = row_data["playerName"]
                kifu_text += f"{player_phase}：{player_name}\n"
            elif row_data["type"] == "VariationLabel":
                moves = variation_label_statement_p.from_pivot(
                    row_data["moves"])
                kifu_text += variation_label_statement_p.to_pivot(moves)
            elif row_data["type"] == "Result":
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
            else:
                # Error
                print(
                    f"Error: unimplemented row_number={row_number} row_data={row_data}")
                return None, None

        # New .kifu ファイル出力
        kifuFile = os.path.join(output_folder, f"{stem}.kifu")
        with open(kifuFile, mode='w', encoding='utf-8') as fOut:
            fOut.write(kifu_text)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    donePivotFile = shutil.move(
        pivot_file, os.path.join(done_folder, basename))

    return kifuFile, donePivotFile


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output(echo=False)

    copy_pivot_from_input()

    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot/*.json")
    for pivot_file in pivot_files:
        kifu_file, _done_pivot_file = convert_pivot_to_kifu(
            pivot_file, output_folder='output')

        if kifu_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .json (PIVOT) file to .kifu file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
