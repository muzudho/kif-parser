import os
import glob
import json
import sys
import shutil
from collections import OrderedDict
from scripts.kifu_specification import player_phase_p, handicap_p, \
    judge_statement1_p, judge_statement2_p, judge_statement3_p, move_statement_p


def convert_pivot_to_kifu(pivotFile):
    # basename

    try:
        basename = os.path.basename(pivotFile)
    except:
        # デバッグ消す
        print(f"Error: pivotFile={pivotFile} except={sys.exc_info()[0]}")
        raise
        # return None, None

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None, None

    kifuFile = ""

    with open(pivotFile, encoding='utf-8') as f:
        data = json.loads(f.read(), object_pairs_hook=OrderedDict)

        move_section_flag = False
        kifu_text = ""

        # JSON to KIFU
        for rowNumber, rowData in data.items():

            if rowData["Type"] == "Comment":
                kifu_text += f"#{rowData['Comment']}\n"
            elif rowData["Type"] == "Explanation":
                kifu_text += f"*{rowData['Explanation']}\n"
            elif rowData["Type"] == "Move":
                # 指し手
                if not move_section_flag:
                    kifu_text += "手数----指手---------消費時間--\n"
                    move_section_flag = True

                kifu_text += move_statement_p.from_pivot(
                    moves=rowData['Moves'],
                    elapsedTime=rowData['ElapsedTime'],
                    totalElapsedTime=rowData['TotalElapsedTime'],
                    move=rowData['Move'])
            elif rowData["Type"] == "Handicap":
                kifu_text += f"手合割：{handicap_p.from_pivot(rowData['Handicap'])}\n"
            elif rowData["Type"] == "Player":
                kifu_text += f"{player_phase_p.from_pivot(rowData['PlayerPhase'])}：{rowData['PlayerName']}\n"
            elif rowData["Type"] == "Result":
                if 'Winner' in rowData:
                    # Example: `まで64手で後手の勝ち`
                    kifu_text += judge_statement1_p.from_pivot(
                        rowData['Moves'], rowData['Winner'], rowData['Judge'])
                elif 'Reason' in rowData:
                    # Example: `まで52手で時間切れにより後手の勝ち`
                    kifu_text += judge_statement3_p.from_pivot(
                        rowData['Moves'], rowData['Reason'], rowData['Winner'], rowData['Judge'])
                else:
                    # Example: `まで63手で中断`
                    kifu_text += judge_statement2_p.from_pivot(
                        rowData['Moves'], rowData['Judge'])
            else:
                # Error
                print(f"Error: rowNumberey={rowNumber} rowData={rowData}")
                return None, None

        # New .kifu ファイル出力
        kifuFile = os.path.join('kifu', f"{stem}.kifu")
        with open(kifuFile, mode='w', encoding='utf-8') as fOut:
            fOut.write(kifu_text)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    donePivotFile = shutil.move(
        pivotFile, os.path.join('pivot-done', basename))

    return kifuFile, donePivotFile


def main():
    # PIVOTファイル一覧
    pivot_files = glob.glob("./pivot/*.json")
    for pivot_file in pivot_files:
        _kifuFile, _donePivotFile = convert_pivot_to_kifu(pivot_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
