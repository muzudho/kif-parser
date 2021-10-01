import os
import glob
import json
import sys
import shutil
from collections import OrderedDict
from scripts.toml_specification import player_phase_p, handicap_p, \
    judge_statement1_p, judge_statement2_p, judge_statement3_p, move_statement_p
import argparse
from remove_all_temporary import remove_all_temporary


def convert_pivot_to_toml(pivot_file, output_folder='temporary/toml', done_folder='temporary/pivot-done'):

    # basename
    try:
        basename = os.path.basename(pivot_file)
    except:
        print(f"Error: pivot_file={pivot_file} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None, None

    toml_file = ""

    with open(pivot_file, encoding='utf-8') as f:
        data = json.loads(f.read(), object_pairs_hook=OrderedDict)

        move_section_flag = False
        kifu_text = ""

        # JSON to KIFU
        for rowNumber, rowData in data.items():

            if rowData["type"] == "Comment":
                comment = rowData["comment"]
                kifu_text += f'#{comment}\n'
            elif rowData["type"] == "Explanation":
                explanation = rowData["explanation"]
                kifu_text += f"*{explanation}\n"
            elif rowData["type"] == "Move":
                # 指し手

                if not move_section_flag:
                    kifu_text += "[moves]\n"
                    move_section_flag = True

                kifu_text += move_statement_p.from_pivot(
                    moves=rowData["moves"],
                    elapsedTime=rowData["elapsedTime"],
                    totalElapsedTime=rowData["totalElapsedTime"],
                    move=rowData["move"])

            elif rowData["type"] == "Handicap":
                handicap = handicap_p.from_pivot(rowData["handicap"])
                kifu_text += f"handicap='{handicap}'\n"
            elif rowData["type"] == "Player":
                player_phase = player_phase_p.from_pivot(
                    rowData["playerPhase"])
                player_name = rowData["playerName"]
                kifu_text += f"{player_phase}='''{player_name}'''\n"
            elif rowData["type"] == "Result":
                if "reason" in rowData:
                    # Example: `まで52手で時間切れにより後手の勝ち`
                    moves = rowData["moves"]
                    reason = rowData['reason']
                    winner = rowData["winner"]
                    judge = rowData["judge"]
                    kifu_text += judge_statement3_p.from_pivot(
                        moves, reason, winner, judge)
                elif "winner" in rowData:
                    # Example: `まで64手で後手の勝ち`
                    moves = rowData["moves"]
                    winner = rowData["winner"]
                    judge = rowData["judge"]
                    kifu_text += judge_statement1_p.from_pivot(
                        moves, winner, judge)
                else:
                    # Example: `まで63手で中断`
                    moves = rowData["moves"]
                    judge = rowData["judge"]
                    kifu_text += judge_statement2_p.from_pivot(
                        moves, judge)
            else:
                # Error
                print(f"Error: rowNumberey={rowNumber} rowData={rowData}")
                return None, None

        # New .kifu ファイル出力
        toml_file = os.path.join(output_folder, f"{stem}.toml")
        with open(toml_file, mode='w', encoding='utf-8') as fOut:
            fOut.write(kifu_text)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    done_pivot_file = shutil.move(
        pivot_file, os.path.join(done_folder, basename))

    return toml_file, done_pivot_file


def main(debug=False):
    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot/*.json")
    for pivot_file in pivot_files:
        _tomlFile, _donePivotFile = convert_pivot_to_toml(pivot_file)

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary()


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .json (PIVOT) file to .toml file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    main(debug=args.debug)
