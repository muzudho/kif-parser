import glob
import re
import os
import json

__handicap = re.compile(r"^手合割：(.+)$")

def main():


    # KIFUファイル一覧
    files = glob.glob("./kifu/*")
    for file in files:
        data = {}

        # basename
        basename = os.path.basename(file)
        stem, extention = os.path.splitext(basename)
        if extention.lower() != '.kifu':
            return

        # insert new extention
        newPath = os.path.join('./pibot', f"{stem}.json")

        # とりあえず KIFU を読んでみます
        rowNumber = 1
        with open(file, encoding='utf-8') as f:

            s = f.read()
            text = s.rstrip()

            lines = text.split('\n')
            for line in lines:

                result = __handicap.match(line)
                if result:
                    handicap = result.group(1)
                    if handicap == '平手':
                        data[f'{rowNumber}'] = {"Handicap":"Hirate"}
                    elif handicap == '香落ち':
                        data[f'{rowNumber}'] = {"Handicap":"LostLance"}
                    elif handicap == '右香落ち':
                        data[f'{rowNumber}'] = {"Handicap":"LostRightLance"}
                    elif handicap == '角落ち':
                        data[f'{rowNumber}'] = {"Handicap":"LostBishop"}
                    elif handicap == '飛車落ち':
                        data[f'{rowNumber}'] = {"Handicap":"LostRook"}
                    elif handicap == '飛香落ち':
                        data[f'{rowNumber}'] = {"Handicap":"LostRookLance"}
                    elif handicap == '二枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"Lost2Pieces"}
                    elif handicap == '三枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"Lost3Pieces"}
                    elif handicap == '四枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"Lost4Pieces"}
                    elif handicap == '五枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"Lost5Pieces"}
                    elif handicap == '左五枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"LostLeft5Pieces"}
                    elif handicap == '六枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"Lost6Pieces"}
                    elif handicap == '左七枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"LostLeft7Pieces"}
                    elif handicap == '右七枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"LostRight7Pieces"}
                    elif handicap == '八枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"Lost8Pieces"}
                    elif handicap == '十枚落ち':
                        data[f'{rowNumber}'] = {"Handicap":"Lost10Pieces"}
                    elif handicap == 'その他':
                        data[f'{rowNumber}'] = {"Handicap":"Other"}

                    rowNumber += 1
                    continue

                data[f'{rowNumber}'] = {"Line":f"{line}"}
                rowNumber += 1

        with open(newPath, 'w', encoding='utf-8') as fOut:
            fOut.write(json.dumps(data, indent=4))

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
