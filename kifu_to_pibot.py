import glob
import re
import os
import json
import shutil
from scripts.terms import player_phase_to_en, handicap_to_en, piece_type_to_en, japanese_to_number

__comment = re.compile(r"^#(.+)$")
__explanation = re.compile(r"^\*(.+)$")
__handicap = re.compile(r"^手合割：(.+)$")
__playerName = re.compile(r"^(先手|後手|下手|上手)：(.+)$")

# Example: `   1 ７六歩(77)    (00:01 / 00:00:01)`
# Example: `  22 同　角(88)    (00:01 / 00:00:11)`
__move = re.compile(r"^\s*(\d+)\s+([^ ]+)\s+\(([0-9:]+) / ([0-9:]+)\)(.*)$")

# Example: `７六歩(77)`
# Example: `同　角(88)`
# Example: `４九角打`
__move_detail = re.compile(r"^(１|２|３|４|５|６|７|８|９)?(一|二|三|四|五|六|七|八|九)?(同　)?(玉|飛|龍|竜|角|馬|金|銀|成銀|全|桂|成桂|圭|香|成香|杏|歩|と)(打|成)?(\(\d+\))?(.*)$")

# Example: `00:01`
__elapsed_time = re.compile(r"^(\d+):(\d+)$")

# Example: `00:00:16`
__total_elapsed_time = re.compile(r"^(\d+):(\d+):(\d+)$")

# Example: `まで64手で後手の勝ち`
__result1 = re.compile(r"^まで(\d+)手で(先手|後手|下手|上手)の勝ち$")

def parse_kifu_file_to_pibot(file):
    """KIFUファイルを読込んで、JSONファイルを出力します
    """
    data = {}

    # basename
    basename = os.path.basename(file)
    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kifu':
        return

    # insert new extention
    outPath = os.path.join('pibot', f"{stem}.json")

    # とりあえず KIFU を読んでみます
    rowNumber = 1
    with open(file, encoding='utf-8') as f:

        s = f.read()
        text = s.rstrip()

        lines = text.split('\n')
        for line in lines:

            # 指し手の解析
            result = __move.match(line)
            if result:
                data[f'{rowNumber}'] = {"Moves":f"{result.group(1)}"}

                # 消費時間の解析
                elapsedTime = result.group(3)
                if elapsedTime:
                    result2 = __elapsed_time.match(elapsedTime)
                    if result2:
                        data[f'{rowNumber}']['ElapsedTime'] = {}
                        data[f'{rowNumber}']['ElapsedTime']['Minute'] = int(result2.group(1))
                        data[f'{rowNumber}']['ElapsedTime']['Second'] = int(result2.group(2))

                # 累計の消費時間の解析
                totalElapsedTime = result.group(4)
                if totalElapsedTime:
                    result2 = __total_elapsed_time.match(totalElapsedTime)
                    if result2:
                        data[f'{rowNumber}']['TotalElapsedTime'] = {}
                        data[f'{rowNumber}']['TotalElapsedTime']['Hour'] = int(result2.group(1))
                        data[f'{rowNumber}']['TotalElapsedTime']['Minute'] = int(result2.group(2))
                        data[f'{rowNumber}']['TotalElapsedTime']['Second'] = int(result2.group(3))

                # 指し手の詳細の解析
                move = result.group(2)
                if move == '投了':
                    data[f'{rowNumber}']['Move'] = {"Sign":"Resign"}
                else:

                    result2 = __move_detail.match(move)
                    if result2:
                        data[f'{rowNumber}']['Move'] = {}

                        destinationFile = result2.group(1)
                        if destinationFile:
                            data[f'{rowNumber}']['Move']['DestinationFile'] = japanese_to_number(destinationFile)

                        destinationRank = result2.group(2)
                        if destinationRank:
                            data[f'{rowNumber}']['Move']['DestinationRank'] = japanese_to_number(destinationRank)

                        destination = result2.group(3)
                        if destination:
                            if destination=='同　':
                                data[f'{rowNumber}']['Move']['Destination'] = 'Same'
                            else:
                                data[f'{rowNumber}']['Move']['Destination'] = 'Unknown'

                        pieceType = result2.group(4)
                        if pieceType:
                            data[f'{rowNumber}']['Move']['PieceType'] = piece_type_to_en(pieceType)

                        dropOrPromotion = result2.group(5)
                        if dropOrPromotion:
                            if dropOrPromotion=='打':
                                data[f'{rowNumber}']['Move']['Drop'] = True
                            elif dropOrPromotion=='成':
                                data[f'{rowNumber}']['Move']['Promotion'] = True
                            else:
                                data[f'{rowNumber}']['Move']['DropOrPromotion'] = 'Unknown'

                        source = result2.group(6)
                        if source:
                            # Example `(77)`
                            square = int(source[1:-1])
                            data[f'{rowNumber}']['Move']['SourceFile'] = square//10
                            data[f'{rowNumber}']['Move']['SourceRank'] = square%10

                        unknown = result2.group(7)
                        if unknown:
                            data[f'{rowNumber}']['Move']['Unknown'] = unknown

                    else:
                        data[f'{rowNumber}']['Move'] = {"Unknown":move}

                rowNumber += 1
                continue

            # コメントの解析
            result = __comment.match(line)
            if result:
                data[f'{rowNumber}'] = {"Comment":f"{result.group(1)}"}

                rowNumber += 1
                continue

            # 指し手等の解説の解析
            result = __explanation.match(line)
            if result:
                data[f'{rowNumber}'] = {"Explanation":f"{result.group(1)}"}

                rowNumber += 1
                continue

            # プレイヤー名の解析
            result = __playerName.match(line)
            if result:
                data[f'{rowNumber}'] = {
                    "PlayerPhase":f"{player_phase_to_en(result.group(1))}",
                    "PlayerName":f"{result.group(2)}",
                }

                rowNumber += 1
                continue

            # 指し手のテーブルの先頭行
            if line == '手数----指手---------消費時間--':
                # Ignored
                rowNumber += 1
                continue

            result = __handicap.match(line)
            if result:
                handicap = result.group(1)
                data[f'{rowNumber}'] = {"Handicap":handicap_to_en(handicap)}

                rowNumber += 1
                continue

            # Example: `まで64手で後手の勝ち`
            result = __result1.match(line)
            if result:
                moves = result.group(1)
                playerPhase = result.group(2)
                data[f'{rowNumber}'] = {
                    "Winner":f"{playerPhase}",
                    "Moves":f"{moves}",
                }

                rowNumber += 1
                continue

            # 解析漏れ
            data[f'{rowNumber}'] = {"Unknown":f"{line}"}
            rowNumber += 1

    with open(outPath, 'w', encoding='utf-8') as fOut:
        fOut.write(json.dumps(data, indent=4, ensure_ascii=False))

    # ファイルの移動
    donePath = shutil.move(file, os.path.join('kifu-done',basename))
    return outPath, donePath

def main():

    # KIFUファイル一覧
    files = glob.glob("./kifu/*")
    for file in files:
        _outPath, _donePath = parse_kifu_file_to_pibot(file)

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
