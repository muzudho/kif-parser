import glob
import re
import os
import json
import shutil
from scripts.kifu_specification import CommentP, ExplanationP, BookmarkP, player_phase_p, player_statement_p, handicap_p, PieceTypeP, ZenkakuNumberP, KanjiNumberP, sign_p, MoveStatementP, MoveP, ElapsedTimeP, TotalElapsedTimeP, JudgeStatement1P, JudgeStatement2P, JudgeStatement3P, ReasonP

__comment_p = CommentP()
__explanation_p = ExplanationP()
__bookmark_p = BookmarkP()
__move_statement_p = MoveStatementP()
__move_p = MoveP()
__elapsed_time_p = ElapsedTimeP()
__total_elapsed_time_p = TotalElapsedTimeP()
__judge_statement1_p = JudgeStatement1P()
__judge_statement2_p = JudgeStatement2P()
__judge_statement3_p = JudgeStatement3P()
__reason_p = ReasonP()


def convert_kifu_to_pivot(file, output_folder='pivot', done_folder='kifu-done'):
    """KIFUファイルを読込んで、JSONファイルを出力します
    """
    piece_type_p = PieceTypeP()
    zenkaku_number_p = ZenkakuNumberP()
    kanji_number_p = KanjiNumberP()

    data = {}

    # basename
    basename = os.path.basename(file)
    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kifu':
        return

    # insert new extention
    outPath = os.path.join(output_folder, f"{stem}.json")

    # とりあえず KIFU を読んでみます
    row_number = 1
    with open(file, encoding='utf-8') as f:

        s = f.read()
        text = s.rstrip()

        lines = text.split('\n')
        for line in lines:

            # 指し手の解析
            result = __move_statement_p.match(line)
            if result:
                moves = result.group(1)
                move = result.group(2)
                elapsedTime = result.group(3)
                totalElapsedTime = result.group(4)

                data[f'{row_number}'] = {
                    "Type": "Move",
                    "Moves": f"{moves}"
                }

                # 消費時間の解析
                if elapsedTime:
                    result2 = __elapsed_time_p.match(elapsedTime)
                    if result2:
                        minute = int(result2.group(1))
                        second = int(result2.group(2))
                        data[f'{row_number}']['ElapsedTime'] = {}
                        data[f'{row_number}']['ElapsedTime']['Minute'] = minute
                        data[f'{row_number}']['ElapsedTime']['Second'] = second

                # 累計の消費時間の解析
                if totalElapsedTime:
                    result2 = __total_elapsed_time_p.match(totalElapsedTime)
                    if result2:
                        hour = int(result2.group(1))
                        minute = int(result2.group(2))
                        second = int(result2.group(3))
                        data[f'{row_number}']['TotalElapsedTime'] = {}
                        data[f'{row_number}']['TotalElapsedTime']['Hour'] = hour
                        data[f'{row_number}']['TotalElapsedTime']['Minute'] = minute
                        data[f'{row_number}']['TotalElapsedTime']['Second'] = second

                # 指し手の詳細の解析
                if sign_p.contains(move):
                    data[f'{row_number}']['Move'] = {
                        "Sign": sign_p.to_pivot(move)}
                else:

                    result2 = __move_p.match(move)
                    if result2:
                        data[f'{row_number}']['Move'] = {}

                        destinationFile = result2.group(1)
                        if destinationFile:
                            dstFile = zenkaku_number_p.to_pivot(
                                destinationFile)
                            data[f'{row_number}']['Move']['DestinationFile'] = dstFile

                        destinationRank = result2.group(2)
                        if destinationRank:
                            dstRank = kanji_number_p.to_pivot(destinationRank)
                            data[f'{row_number}']['Move']['DestinationRank'] = dstRank

                        destination = result2.group(3)
                        if destination:
                            if destination == '同　':
                                data[f'{row_number}']['Move']['Destination'] = 'Same'
                            else:
                                # Error
                                print(f"Error: destination={destination}")
                                return None, None

                        pieceType = result2.group(4)
                        if pieceType:
                            pct = piece_type_p.to_pivot(pieceType)
                            data[f'{row_number}']['Move']['PieceType'] = pct

                        dropOrPromotion = result2.group(5)
                        if dropOrPromotion:
                            if dropOrPromotion == '打':
                                data[f'{row_number}']['Move']['Drop'] = True
                            elif dropOrPromotion == '成':
                                data[f'{row_number}']['Move']['Promotion'] = True
                            else:
                                # Error
                                print(
                                    f"Error: dropOrPromotion={dropOrPromotion}")
                                return None, None

                        source = result2.group(6)
                        if source:
                            # Example `(77)`
                            square = int(source[1:-1])
                            srcFile = square//10
                            srcRank = square % 10
                            data[f'{row_number}']['Move']['SourceFile'] = srcFile
                            data[f'{row_number}']['Move']['SourceRank'] = srcRank

                        unknown = result2.group(7)
                        if unknown:
                            data[f'{row_number}']['Move']['Unknown'] = unknown

                    else:
                        data[f'{row_number}']['Move'] = {"Unknown": move}

                row_number += 1
                continue

            # コメントの解析
            result = __comment_p.match(line)
            if result:
                comment = result.group(1)
                __comment_p.to_pibot(data, row_number, comment)

                row_number += 1
                continue

            # 指し手等の解説の解析
            result = __explanation_p.match(line)
            if result:
                explanation = result.group(1)
                __explanation_p.to_pibot(data, row_number, explanation)

                row_number += 1
                continue

            # しおりの解析
            result = __bookmark_p.match(line)
            if result:
                bookmark = result.group(1)
                __bookmark_p.to_pibot(data, row_number, bookmark)

                row_number += 1
                continue

            # プレイヤー名の解析
            result = player_statement_p.match(line)
            if result:
                player_phase = player_phase_p.to_pivot(result.group(1))
                player_name = result.group(2)
                data[f'{row_number}'] = {
                    "Type": "Player",
                    "PlayerPhase": f"{player_phase}",
                    "PlayerName": f"{player_name}",
                }

                row_number += 1
                continue

            # 指し手のテーブルの先頭行
            if line == '手数----指手---------消費時間--':
                # Ignored
                row_number += 1
                continue

            result = handicap_p.match(line)
            if result:
                handicap = handicap_p.to_pivot(result.group(1))
                data[f'{row_number}'] = {
                    "Type": "Handicap",
                    "Handicap": handicap,
                }

                row_number += 1
                continue

            # Example: `まで64手で後手の勝ち`
            result = __judge_statement1_p.match(line)
            if result:
                moves = result.group(1)
                playerPhase = player_phase_p.to_pivot(result.group(2))
                judge = sign_p.to_pivot(result.group(3))
                data[f'{row_number}'] = {
                    "Type": "Result",
                    "Moves": f"{moves}",
                    "Winner": f"{playerPhase}",
                    "Judge": f"{judge}",
                }

                row_number += 1
                continue

            # Example: `まで63手で中断`
            result = __judge_statement2_p.match(line)
            if result:
                moves = result.group(1)
                judge = sign_p.to_pivot(result.group(2))
                data[f'{row_number}'] = {
                    "Type": "Result",
                    "Moves": f"{moves}",
                    "Judge": f"{judge}",
                }

                row_number += 1
                continue

            # Example: `まで52手で時間切れにより後手の勝ち`
            result = __judge_statement3_p.match(line)
            if result:
                moves = result.group(1)
                reason = __reason_p.to_pivot(result.group(2))
                playerPhase = player_phase_p.to_pivot(result.group(3))
                judge = sign_p.to_pivot(result.group(4))
                data[f'{row_number}'] = {
                    "Type": "Result",
                    "Moves": f"{moves}",
                    "Reason": f"{reason}",
                    "Winner": f"{playerPhase}",
                    "Judge": f"{judge}",
                }

                row_number += 1
                continue

            # 解析漏れ
            print(f"Error: row_number={row_number} line={line}")
            return None, None

    with open(outPath, 'w', encoding='utf-8') as fOut:
        fOut.write(json.dumps(data, indent=4, ensure_ascii=False))

    # ファイルの移動
    donePath = shutil.move(file, os.path.join(done_folder, basename))
    return outPath, donePath


def main():

    # KIFUファイル一覧
    kifu_files = glob.glob("./kifu/*.kifu")
    for kifu_file in kifu_files:
        _outPath, _donePath = convert_kifu_to_pivot(kifu_file)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    main()
