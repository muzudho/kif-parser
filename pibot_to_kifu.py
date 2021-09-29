import os
import glob
import json
import shutil
from collections import OrderedDict
import pprint
from scripts.terms import en_to_handicap, en_to_player_phase, en_to_sign


def convert_pibot_to_kifu(pibotFile):
    # basename
    basename = os.path.basename(pibotFile)
    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None, None

    kifuFile = ""

    with open(pibotFile, encoding='utf-8') as f:
        data = json.loads(f.read(), object_pairs_hook=OrderedDict)
        pprint.pprint(data, width=40)

        kifu_text = ""

        # TODO JSON to KIFU
        for rowNumber, rowData in data.items():

            if rowData["Type"] == "Comment":
                kifu_text += f"#{rowData['Comment']}\n"
            elif rowData["Type"] == "Handicap":
                kifu_text += f"手合割：{en_to_handicap(rowData['Handicap'])}\n"
            elif rowData["Type"] == "Player":
                kifu_text += f"{en_to_player_phase(rowData['PlayerPhase'])}：{rowData['PlayerName']}\n"
            elif rowData["Type"] == "Result":
                kifu_text += f"まで{rowData['Moves']}手で{en_to_player_phase(rowData['Winner'])}の勝ち\n"
            elif rowData["Type"] == "Move":
                # 指し手
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

                if 'Sign' in move:
                    sign = move['Sign']
                    move_text += f"{sign}"

                if 'DestinationFile' in move:
                    destinationFile = move['DestinationFile']
                    destinationRank = move['DestinationRank']
                    move_text += f"{destinationFile}{destinationRank}"

                if 'Destination' in move:
                    destination = move['Destination']
                    move_text += f"{destination}"

                if 'PieceType' in move:
                    pieceType = move['PieceType']
                    move_text += f"{pieceType}"

                if 'SourceFile' in move:
                    sourceFile = move['SourceFile']
                    sourceRank = move['SourceRank']
                    move_text += f"{sourceFile}{sourceRank}"

                kifu_text += f"{moves:4} {move_text} ({elapsedTimeMinute:2}:{elapsedTimeSecond:2}) ({totalElapsedTimeHour:2}:{totalElapsedTimeMinute:2}:{totalElapsedTimeSecond:2})\n"
            else:
                print(f"krowNumberey={rowNumber} rowData={rowData}")
                kifu_text += f"krowNumberey={rowNumber} rowData={rowData}\n"

        # New .kifu ファイル出力
        kifuFile = os.path.join('kifu', f"{stem}.kifu")
        with open(kifuFile, mode='w', encoding='utf-8') as fOut:
            print(f"kifu_text={kifu_text}")
            fOut.write(kifu_text)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    donePibotFile = shutil.move(
        pibotFile, os.path.join('pibot-done', basename))

    return kifuFile, donePibotFile


def main():
    # KIFファイル一覧
    pibotFiles = glob.glob("./pibot/*")
    for pibotFile in pibotFiles:
        _kifuFile, _donePibotFile = convert_pibot_to_kifu(pibotFile)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
