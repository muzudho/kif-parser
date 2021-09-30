import os
import glob
import json
import sys
import shutil
from collections import OrderedDict
from scripts.kifu_specification import player_phase_p, HandicapP, ZenkakuNumberP, KanjiNumberP, SignP, PieceTypeP, JudgeStatement1P, JudgeStatement2P, JudgeStatement3P

__handicap_p = HandicapP()
__zenkaku_number_p = ZenkakuNumberP()
__kanji_number_p = KanjiNumberP()
__sign_p = SignP()
__piece_type_p = PieceTypeP()
__judge_statement1_p = JudgeStatement1P()
__judge_statement2_p = JudgeStatement2P()
__judge_statement3_p = JudgeStatement3P()


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

                moves = rowData['Moves']
                elapsedTime = rowData['ElapsedTime']
                elapsedTimeMinute = elapsedTime['Minute']
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
                    sign = __sign_p.from_pivot(move['Sign'])
                    move_text += f"{sign}"
                    spaces -= __sign_p.half_width(sign)

                if 'DestinationFile' in move:
                    destinationFile = __zenkaku_number_p.from_pivot(
                        move['DestinationFile'])
                    destinationRank = __kanji_number_p.from_pivot(
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
                    pieceType = __piece_type_p.from_pivot(move['PieceType'])
                    move_text += f"{pieceType}"
                    spaces -= __piece_type_p.half_width(pieceType)

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

                # 左にスペースを詰めます
                move_text += ''.ljust(spaces, ' ')

                kifu_text += f"{moves:>4} {move_text}({elapsedTimeMinute:02}:{elapsedTimeSecond:02} / {totalElapsedTimeHour:02}:{totalElapsedTimeMinute:02}:{totalElapsedTimeSecond:02})\n"
            elif rowData["Type"] == "Handicap":
                kifu_text += f"手合割：{__handicap_p.from_pivot(rowData['Handicap'])}\n"
            elif rowData["Type"] == "Player":
                kifu_text += f"{player_phase_p.from_pivot(rowData['PlayerPhase'])}：{rowData['PlayerName']}\n"
            elif rowData["Type"] == "Result":
                if 'Winner' in rowData:
                    # Example: `まで64手で後手の勝ち`
                    kifu_text += __judge_statement1_p.from_pivot(
                        rowData['Moves'], rowData['Winner'], rowData['Judge'])
                elif 'Reason' in rowData:
                    # Example: `まで52手で時間切れにより後手の勝ち`
                    kifu_text += __judge_statement3_p.from_pivot(
                        rowData['Moves'], rowData['Reason'], rowData['Winner'], rowData['Judge'])
                else:
                    # Example: `まで63手で中断`
                    kifu_text += __judge_statement2_p.from_pivot(
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
    donePibotFile = shutil.move(
        pivotFile, os.path.join('pivot-done', basename))

    return kifuFile, donePibotFile


def main():
    # PIBOTファイル一覧
    pivotFiles = glob.glob("./pivot/*")
    for pivotFile in pivotFiles:
        _kifuFile, _donePibotFile = convert_pivot_to_kifu(pivotFile)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
