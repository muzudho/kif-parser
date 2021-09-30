import os
import glob
import json
import sys
import shutil
from collections import OrderedDict
from scripts.toml_specification import player_phase_p, handicap_p, zenkaku_number_p, kanji_number_p, sign_p, \
    piece_type_p, judge_statement1_p, judge_statement2_p, judge_statement3_p


def convert_pivot_to_toml(pivotFile):
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

    tomlFile = ""

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
                    kifu_text += "[Moves]\n"
                    move_section_flag = True

                moves = rowData['Moves']
                elapsedTime = rowData['ElapsedTime']
                elapsedTimeHour = 0
                elapsedTimeMinute = elapsedTime['Minute']
                if 60 < elapsedTimeMinute:
                    elapsedTimeHour = elapsedTimeMinute // 60
                    elapsedTimeMinute = elapsedTimeMinute % 60
                elapsedTimeSecond = elapsedTime['Second']
                totalElapsedTime = rowData['TotalElapsedTime']
                totalElapsedTimeHour = totalElapsedTime['Hour']
                totalElapsedTimeMinute = totalElapsedTime['Minute']
                totalElapsedTimeSecond = totalElapsedTime['Second']

                move = rowData['Move']
                move_text = ""
                # 半角スペース幅
                spaces = 14

                if 'Sign' in move:
                    sign = sign_p.from_pivot(move['Sign'])
                    move_text += f"{sign}"
                    spaces -= sign_p.half_width(sign)

                if 'DestinationFile' in move:
                    destinationFile = zenkaku_number_p.from_pivot(
                        move['DestinationFile'])
                    destinationRank = kanji_number_p.from_pivot(
                        move['DestinationRank'])
                    move_text += f"{destinationFile}{destinationRank}"
                    spaces -= 4

                if 'Destination' in move:
                    destination = move['Destination']
                    if destination == 'Same':
                        move_text += "同　"
                        spaces -= 4
                    else:
                        move_text += f"{destination}"
                        spaces -= 2

                if 'PieceType' in move:
                    pieceType = piece_type_p.from_pivot(move['PieceType'])
                    move_text += f"{pieceType}"
                    spaces -= piece_type_p.half_width(pieceType)

                if 'Drop' in move:
                    drop = move['Drop']
                    if drop:
                        move_text += "打"
                        spaces -= 2

                if 'Promotion' in move:
                    pro = move['Promotion']
                    if pro:
                        move_text += "成"
                        spaces -= 2

                if 'SourceFile' in move:
                    sourceFile = move['SourceFile']
                    sourceRank = move['SourceRank']
                    move_text += f"({sourceFile}{sourceRank})"
                    spaces -= 4

                kifu_text += f'[Moves.{moves}]\n'
                kifu_text += f"Move='{move_text}'\n"
                kifu_text += f"Elapsed={elapsedTimeHour:02}:{elapsedTimeMinute:02}:{elapsedTimeSecond:02}\n"
                kifu_text += f"Total-elapsed={totalElapsedTimeHour:02}:{totalElapsedTimeMinute:02}:{totalElapsedTimeSecond:02}\n"
            elif rowData["Type"] == "Handicap":
                kifu_text += f"Handicap='{handicap_p.from_pivot(rowData['Handicap'])}'\n"
            elif rowData["Type"] == "Player":
                kifu_text += f"{player_phase_p.from_pivot(rowData['PlayerPhase'])}='''{rowData['PlayerName']}'''\n"
            elif rowData["Type"] == "Result":
                kifu_text += f'[Result]\n'
                if 'Winner' in rowData:
                    # Example: `まで64手で後手の勝ち`
                    kifu_text += f"Last-moves='{rowData['Moves']}'\n"
                    kifu_text += f"Winner='{rowData['Winner']}'\n"
                    kifu_text += f"Judge='{rowData['Judge']}'\n"
                elif 'Reason' in rowData:
                    # Example: `まで52手で時間切れにより後手の勝ち`
                    kifu_text += f"Last-moves='{rowData['Moves']}'\n"
                    kifu_text += f"Reason='{rowData['Reason']}'\n"
                    kifu_text += f"Winner='{rowData['Winner']}'\n"
                    kifu_text += f"Judge='{rowData['Judge']}'\n"
                else:
                    # Example: `まで63手で中断`
                    kifu_text += f"Judge='{rowData['Judge']}'\n"
            else:
                # Error
                print(f"Error: rowNumberey={rowNumber} rowData={rowData}")
                return None, None

        # New .kifu ファイル出力
        tomlFile = os.path.join('toml', f"{stem}.toml")
        with open(tomlFile, mode='w', encoding='utf-8') as fOut:
            fOut.write(kifu_text)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    donePibotFile = shutil.move(
        pivotFile, os.path.join('pivot-done', basename))

    return tomlFile, donePibotFile


def main():
    # PIBOTファイル一覧
    pivot_files = glob.glob("./pivot/*.json")
    for pivot_file in pivot_files:
        _tomlFile, _donePibotFile = convert_pivot_to_toml(pivot_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
