import os
import glob
import json
import shutil
from collections import OrderedDict
import pprint

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
    donePibotFile = shutil.move(pibotFile, os.path.join('pibot-done',basename))

    return kifuFile, donePibotFile

def main():
    # KIFファイル一覧
    pibotFiles = glob.glob("./pibot/*")
    for pibotFile in pibotFiles:
        _kifuFile, _donePibotFile = convert_pibot_to_kifu(pibotFile)

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
