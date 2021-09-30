import glob
import re
import os
import json
import shutil
from scripts.kifu_specification import CommentP, ExplanationP, PlayerPhaseP, PlayerNameP, HandicapP, PieceTypeP, ZenkakuNumberP, KanjiNumberP, SignP, JudgeP, MoveStatementP, MoveP, ElapsedTimeP, TotalElapsedTimeP, JudgeStatement1P, JudgeStatement2P

__comment_p = CommentP()
__explanation_p = ExplanationP()
__handicap_p = HandicapP()
__player_name_p = PlayerNameP()
__move_statement_p = MoveStatementP()
__move_p = MoveP()
__elapsed_time_p = ElapsedTimeP()
__total_elapsed_time_p = TotalElapsedTimeP()
__judge_statement1_p = JudgeStatement1P()
__judge_statement2_p = JudgeStatement2P()


def convert_kifu_to_pibot(file):
    """KIFUファイルを読込んで、JSONファイルを出力します
    """
    player_phase_p = PlayerPhaseP()
    piece_type_p = PieceTypeP()
    zenkaku_number_p = ZenkakuNumberP()
    kanji_number_p = KanjiNumberP()
    sign_p = SignP()
    judge_p = JudgeP()

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
            result = __move_statement_p.match(line)
            if result:
                data[f'{rowNumber}'] = {
                    "Type": "Move",
                    "Moves": f"{result.group(1)}"
                }

                # 消費時間の解析
                elapsedTime = result.group(3)
                if elapsedTime:
                    result2 = __elapsed_time_p.match(elapsedTime)
                    if result2:
                        data[f'{rowNumber}']['ElapsedTime'] = {}
                        data[f'{rowNumber}']['ElapsedTime']['Minute'] = int(
                            result2.group(1))
                        data[f'{rowNumber}']['ElapsedTime']['Second'] = int(
                            result2.group(2))

                # 累計の消費時間の解析
                totalElapsedTime = result.group(4)
                if totalElapsedTime:
                    result2 = __total_elapsed_time_p.match(totalElapsedTime)
                    if result2:
                        data[f'{rowNumber}']['TotalElapsedTime'] = {}
                        data[f'{rowNumber}']['TotalElapsedTime']['Hour'] = int(
                            result2.group(1))
                        data[f'{rowNumber}']['TotalElapsedTime']['Minute'] = int(
                            result2.group(2))
                        data[f'{rowNumber}']['TotalElapsedTime']['Second'] = int(
                            result2.group(3))

                # 指し手の詳細の解析
                move = result.group(2)
                if sign_p.contains(move):
                    data[f'{rowNumber}']['Move'] = {
                        "Sign": sign_p.to_pibot(move)}
                else:

                    result2 = __move_p.match(move)
                    if result2:
                        data[f'{rowNumber}']['Move'] = {}

                        destinationFile = result2.group(1)
                        if destinationFile:
                            data[f'{rowNumber}']['Move']['DestinationFile'] = zenkaku_number_p.to_pibot(
                                destinationFile)

                        destinationRank = result2.group(2)
                        if destinationRank:
                            data[f'{rowNumber}']['Move']['DestinationRank'] = kanji_number_p.to_pibot(
                                destinationRank)

                        destination = result2.group(3)
                        if destination:
                            if destination == '同　':
                                data[f'{rowNumber}']['Move']['Destination'] = 'Same'
                            else:
                                # Error
                                print(f"Error: destination={destination}")
                                return None, None

                        pieceType = result2.group(4)
                        if pieceType:
                            data[f'{rowNumber}']['Move']['PieceType'] = piece_type_p.to_pibot(
                                pieceType)

                        dropOrPromotion = result2.group(5)
                        if dropOrPromotion:
                            if dropOrPromotion == '打':
                                data[f'{rowNumber}']['Move']['Drop'] = True
                            elif dropOrPromotion == '成':
                                data[f'{rowNumber}']['Move']['Promotion'] = True
                            else:
                                # Error
                                print(
                                    f"Error: dropOrPromotion={dropOrPromotion}")
                                return None, None

                        source = result2.group(6)
                        if source:
                            # Example `(77)`
                            square = int(source[1:-1])
                            data[f'{rowNumber}']['Move']['SourceFile'] = square//10
                            data[f'{rowNumber}']['Move']['SourceRank'] = square % 10

                        unknown = result2.group(7)
                        if unknown:
                            data[f'{rowNumber}']['Move']['Unknown'] = unknown

                    else:
                        data[f'{rowNumber}']['Move'] = {"Unknown": move}

                rowNumber += 1
                continue

            # コメントの解析
            result = __comment_p.match(line)
            if result:
                data[f'{rowNumber}'] = {
                    "Type": "Comment",
                    "Comment": f"{result.group(1)}"
                }

                rowNumber += 1
                continue

            # 指し手等の解説の解析
            result = __explanation_p.match(line)
            if result:
                data[f'{rowNumber}'] = {
                    "Type": "Explanation",
                    "Explanation": f"{result.group(1)}",
                }

                rowNumber += 1
                continue

            # プレイヤー名の解析
            result = __player_name_p.match(line)
            if result:
                data[f'{rowNumber}'] = {
                    "Type": "Player",
                    "PlayerPhase": f"{player_phase_p.to_pibot(result.group(1))}",
                    "PlayerName": f"{result.group(2)}",
                }

                rowNumber += 1
                continue

            # 指し手のテーブルの先頭行
            if line == '手数----指手---------消費時間--':
                # Ignored
                rowNumber += 1
                continue

            result = __handicap_p.match(line)
            if result:
                handicap = result.group(1)
                data[f'{rowNumber}'] = {
                    "Type": "Handicap",
                    "Handicap": __handicap_p.to_pibot(handicap),
                }

                rowNumber += 1
                continue

            # Example: `まで64手で後手の勝ち`
            result = __judge_statement1_p.match(line)
            if result:
                moves = result.group(1)
                playerPhase = result.group(2)
                judge = result.group(3)
                data[f'{rowNumber}'] = {
                    "Type": "Result",
                    "Moves": f"{moves}",
                    "Winner": f"{player_phase_p.to_pibot(playerPhase)}",
                    "Judge": f"{judge_p.to_pibot(judge)}",
                }

                rowNumber += 1
                continue

            # Example: `まで63手で中断`
            result = __judge_statement2_p.match(line)
            if result:
                moves = result.group(1)
                judge = result.group(2)
                data[f'{rowNumber}'] = {
                    "Type": "Result",
                    "Moves": f"{moves}",
                    "Judge": f"{judge_p.to_pibot(judge)}",
                }

                rowNumber += 1
                continue

            # 解析漏れ
            print(f"Error: rowNumber={rowNumber} line={line}")
            return None, None

    with open(outPath, 'w', encoding='utf-8') as fOut:
        fOut.write(json.dumps(data, indent=4, ensure_ascii=False))

    # ファイルの移動
    donePath = shutil.move(file, os.path.join('kifu-done', basename))
    return outPath, donePath


def main():

    # KIFUファイル一覧
    files = glob.glob("./kifu/*")
    for file in files:
        _outPath, _donePath = convert_kifu_to_pibot(file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
