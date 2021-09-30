import os
import glob
import json
import sys
import shutil
from collections import OrderedDict
from scripts.kifu_terms import PlayerPhaseP, en_to_handicap, number_to_zenkaku, number_to_kanji, en_to_sign, en_to_piece_type, sign_half_width, piece_type_half_width, en_to_judge

__player_phase_p = PlayerPhaseP()


def convert_pibot_to_kifu(pibotFile):
    # basename

    try:
        basename = os.path.basename(pibotFile)
    except:
        # デバッグ消す
        print(f"Error: pibotFile={pibotFile} except={sys.exc_info()[0]}")
        raise
        # return None, None

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None, None

    kifuFile = ""

    with open(pibotFile, encoding='utf-8') as f:
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
                    sign = en_to_sign(move['Sign'])
                    move_text += f"{sign}"
                    spaces -= sign_half_width(sign)

                if 'DestinationFile' in move:
                    destinationFile = number_to_zenkaku(
                        move['DestinationFile'])
                    destinationRank = number_to_kanji(move['DestinationRank'])
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
                    pieceType = en_to_piece_type(move['PieceType'])
                    move_text += f"{pieceType}"
                    spaces -= piece_type_half_width(pieceType)

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
                kifu_text += f"手合割：{en_to_handicap(rowData['Handicap'])}\n"
            elif rowData["Type"] == "Player":
                kifu_text += f"{__player_phase_p.from_en(rowData['PlayerPhase'])}：{rowData['PlayerName']}\n"
            elif rowData["Type"] == "Result":
                kifu_text += f"まで{rowData['Moves']}手で{__player_phase_p.from_en(rowData['Winner'])}の{en_to_judge(rowData['Judge'])}\n"
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
        pibotFile, os.path.join('pibot-done', basename))

    return kifuFile, donePibotFile


def main():
    # PIBOTファイル一覧
    pibotFiles = glob.glob("./pibot/*")
    for pibotFile in pibotFiles:
        _kifuFile, _donePibotFile = convert_pibot_to_kifu(pibotFile)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
