import os
import json
from scripts.kifu_specification import comment_p, explanation_p, bookmark_p, player_phase_p, \
    player_statement_p, handicap_statement_p, piece_type_p, zenkaku_number_p, kanji_number_p, sign_p, \
    move_statement_p, move_p, elapsed_time_p, total_elapsed_time_p, judge_statement1_p, \
    judge_statement2_p, judge_statement3_p, reason_p, variation_label_statement_p, \
    start_time_statement_p, end_time_statement_p, moves_header_statement_p
from scripts.generator_identification import generator_identification
import sys


def convert_kifu_to_pivot(kifu_file, output_folder='temporary/pivot'):
    """KIFUファイルを読込んで、JSONファイルを出力します
    Parameters
    ----------
    output_folder : str
        'temporary/pivot' か `output`
    """

    data = {}

    # basename
    try:
        basename = os.path.basename(kifu_file)
    except:
        print(f"Error: kifu_file={kifu_file} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.kifu':
        return

    # insert new extention
    output_pivot = os.path.join(output_folder, f"{stem}.json")

    # とりあえず KIFU を読んでみます
    row_number = 1
    with open(kifu_file, encoding='utf-8') as f:
        text = f.read().rstrip()

    # この棋譜を生成したソフトが何か当てに行きます
    shogi_dokoro, shogi_gui = generator_identification.read_all_text(text)
    # 0行目に情報を追加するものとします
    data[0] = {
        "type": "appendix",
        "generatingSoftwareIsProbably": {
            "shogidokoro": shogi_dokoro,
            "shogi-gui": shogi_gui,
        }
    }

    lines = text.split('\n')
    for line in lines:

        # 空行は読み飛ばします。「変化」の直前に有ったりします
        if line.strip() == '':
            continue

        # 指し手の解析
        result = move_statement_p.match(line)
        if result:
            moves = result.group(1)
            move = result.group(2)
            elapsedTime = result.group(3)
            totalElapsedTime = result.group(4)

            data[f'{row_number}'] = {
                "type": "move",
                "moves": f"{moves}"
            }

            # 消費時間の解析
            if elapsedTime:
                result2 = elapsed_time_p.match(elapsedTime)
                if result2:
                    minute = int(result2.group(1))
                    second = int(result2.group(2))
                    elapsed_time_p.to_pivot(
                        data, row_number, minute, second)

            # 累計の消費時間の解析
            if totalElapsedTime:
                result2 = total_elapsed_time_p.match(totalElapsedTime)
                if result2:
                    hour = int(result2.group(1))
                    minute = int(result2.group(2))
                    second = int(result2.group(3))
                    total_elapsed_time_p.to_pivot(
                        data, row_number, hour, minute, second)

            # 指し手の詳細の解析
            if sign_p.contains(move):
                move = sign_p.to_pivot(move)
                data[f'{row_number}']["move"] = {"sign": move}
            else:

                result2 = move_p.match(move)
                if result2:
                    data[f'{row_number}']["move"] = {}

                    destinationFile = result2.group(1)
                    if destinationFile:
                        dstFile = zenkaku_number_p.to_pivot(
                            destinationFile)
                        data[f'{row_number}']["move"]["destinationFile"] = dstFile

                    destinationRank = result2.group(2)
                    if destinationRank:
                        dstRank = kanji_number_p.to_pivot(destinationRank)
                        data[f'{row_number}']["move"]["destinationRank"] = dstRank

                    destination = result2.group(3)
                    if destination:
                        if destination == '同　':
                            data[f'{row_number}']["move"]["destination"] = 'Same'
                        else:
                            # Error
                            print(f"Error: destination={destination}")
                            return None, None

                    pieceType = result2.group(4)
                    if pieceType:
                        pct = piece_type_p.to_pivot(pieceType)
                        data[f'{row_number}']["move"]["pieceType"] = pct

                    dropOrPromotion = result2.group(5)
                    if dropOrPromotion:
                        if dropOrPromotion == '打':
                            data[f'{row_number}']["move"]["drop"] = True
                        elif dropOrPromotion == '成':
                            data[f'{row_number}']["move"]["promotion"] = True
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
                        data[f'{row_number}']["move"]["sourceFile"] = srcFile
                        data[f'{row_number}']["move"]["sourceRank"] = srcRank

                    # 後ろにコメントが書けるはず
                    unimplemented = result2.group(7)
                    if unimplemented:
                        data[f'{row_number}']["move"]["unimplemented"] = unimplemented

                else:
                    data[f'{row_number}']["move"] = {"Unknown": move}

            row_number += 1
            continue

        # コメントの解析
        result = comment_p.match(line)
        if result:
            comment = result.group(1)
            comment_p.to_pivot(data, row_number, comment)
            row_number += 1
            continue

        # 指し手等の解説の解析
        result = explanation_p.match(line)
        if result:
            explanation = result.group(1)
            explanation_p.to_pivot(data, row_number, explanation)
            row_number += 1
            continue

        # しおりの解析
        result = bookmark_p.match(line)
        if result:
            bookmark = result.group(1)
            bookmark_p.to_pivot(data, row_number, bookmark)
            row_number += 1
            continue

        # 変化のジャンプ先ラベルの解析
        result = variation_label_statement_p.match(line)
        if result:
            moves = result.group(1)
            variation_label_statement_p.to_pivot(
                data, row_number, moves)
            row_number += 1
            continue

        # プレイヤー名の行の解析
        result = player_statement_p.match(line)
        if result:
            player_phase = player_phase_p.to_pivot(result.group(1))
            player_name = result.group(2)
            player_statement_p.to_pivot(
                data, row_number, player_phase, player_name)
            row_number += 1
            continue

        # 指し手リストの先頭行
        result = moves_header_statement_p.match(line)
        if result:
            moves_header_statement_p.to_pivot(data, row_number)
            row_number += 1
            continue

        if line == '手数----指手---------消費時間--':
            # Ignored
            row_number += 1
            continue

        # 開始日時の行の解析
        result = start_time_statement_p.match(line)
        if result:
            startTime = result.group(1)
            start_time_statement_p.to_pivot(data, row_number, startTime)
            row_number += 1
            continue

        # 終了日時の行の解析
        result = end_time_statement_p.match(line)
        if result:
            endTime = result.group(1)
            end_time_statement_p.to_pivot(data, row_number, endTime)
            row_number += 1
            continue

        # 手割合の行の解析
        result = handicap_statement_p.match(line)
        if result:
            handicap = result.group(1)
            handicap_statement_p.to_pivot(data, row_number, handicap)
            row_number += 1
            continue

        # Example: `まで64手で後手の勝ち`
        result = judge_statement1_p.match(line)
        if result:
            moves = result.group(1)
            playerPhase = player_phase_p.to_pivot(result.group(2))
            judge = sign_p.to_pivot(result.group(3))
            judge_statement1_p.to_pivot(
                data, row_number, moves, playerPhase, judge)
            row_number += 1
            continue

        # Example: `まで63手で中断`
        result = judge_statement2_p.match(line)
        if result:
            moves = result.group(1)
            judge = sign_p.to_pivot(result.group(2))
            judge_statement2_p.to_pivot(data, row_number, moves, judge)
            row_number += 1
            continue

        # Example: `まで52手で時間切れにより後手の勝ち`
        result = judge_statement3_p.match(line)
        if result:
            moves = result.group(1)
            reason = reason_p.to_pivot(result.group(2))
            playerPhase = player_phase_p.to_pivot(result.group(3))
            judge = sign_p.to_pivot(result.group(4))
            judge_statement3_p.to_pivot(
                data, row_number, moves, reason, playerPhase, judge)
            row_number += 1
            continue

        # 解析漏れ
        print(
            f"Error: kifu_to_pivot.py unimplemented row_number={row_number} line=[{line}]")
        return None, None

    # 最終行まで解析終わり

    with open(output_pivot, 'w', encoding='utf-8') as fOut:
        fOut.write(json.dumps(data, indent=4, ensure_ascii=False))

    return output_pivot