import os
import json
from scripts.kifu_specification import comment_p, explanation_p, bookmark_p, \
    sign_p, \
    move_statement_p, move_p, elapsed_time_p, total_elapsed_time_p, judge_statement1_p, \
    judge_statement2_p, judge_statement3_p, reason_p, variation_label_statement_p, \
    moves_header_statement_p, \
    any_game_info_key_value_pair_statement_p
from scripts.generator_identification import generator_identification
import sys


def convert_kifu_to_pivot(kifu_file, output_folder):
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
        return None

    # insert new extention
    output_pivot = os.path.join(output_folder, f"{stem}[data].json")

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
                # [投了]とか [中断]とか [詰み]とか
                data[f'{row_number}']["move"] = {"sign": move}
            else:

                result2 = move_p.match(move)
                if result2:
                    data[f'{row_number}']["move"] = {}

                    destinationFile = result2.group(1)
                    if destinationFile:
                        data[f'{row_number}']["move"]["destinationFile"] = destinationFile

                    destinationRank = result2.group(2)
                    if destinationRank:
                        data[f'{row_number}']["move"]["destinationRank"] = destinationRank

                    destination = result2.group(3)
                    if destination:
                        if destination == '同　':
                            data[f'{row_number}']["move"]["destination"] = 'Same'
                        else:
                            # Error
                            print(f"Error: destination={destination}")
                            return None

                    pieceType = result2.group(4)
                    if pieceType:
                        data[f'{row_number}']["move"]["pieceType"] = pieceType

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
                            return None

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
            comment_p.to_pivot(
                data,
                row_number,
                indent=result.group(1),
                comment=result.group(2))
            row_number += 1
            continue

        # 指し手等の解説の解析
        result = explanation_p.match(line)
        if result:
            explanation_p.to_pivot(
                data,
                row_number,
                indent=result.group(1),
                explanation=result.group(2),
                comment=result.group(3))
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

        # 指し手リストの先頭行
        # Example: `手数----指手---------消費時間-- # この行は、なくてもいい`
        result = moves_header_statement_p.match(line)
        if result:
            moves_header = result.group(1)
            comment = result.group(2)
            moves_header_statement_p.to_pivot(
                data, row_number, moves_header, comment)
            row_number += 1
            continue

        # ユーザー定義の対局情報の行の解析
        result = any_game_info_key_value_pair_statement_p.match(line)
        if result:
            key = result.group(1)
            value = result.group(2)
            comment = result.group(3)
            any_game_info_key_value_pair_statement_p.to_pivot(
                data, row_number, key, value, comment)
            row_number += 1
            continue

        # Example: `まで64手で後手の勝ち`
        result = judge_statement1_p.match(line)
        if result:
            moves = result.group(1)
            player_phase = result.group(2)
            judge = result.group(3)
            judge_statement1_p.to_pivot(
                data, row_number, moves, player_phase, judge)
            row_number += 1
            continue

        # Example: `まで63手で中断`
        result = judge_statement2_p.match(line)
        if result:
            moves = result.group(1)
            judge = result.group(2)
            judge_statement2_p.to_pivot(data, row_number, moves, judge)
            row_number += 1
            continue

        # Example: `まで52手で時間切れにより後手の勝ち`
        result = judge_statement3_p.match(line)
        if result:
            moves = result.group(1)
            reason = reason_p.to_pivot(result.group(2))
            player_phase = result.group(3)
            judge = result.group(4)
            judge_statement3_p.to_pivot(
                data, row_number, moves, reason, player_phase, judge)
            row_number += 1
            continue

        # 解析漏れ
        print(
            f"Error: kifu_to_pivot.py unimplemented row_number={row_number} line=[{line}] kifu_file=[{kifu_file}]")
        return None

    # 最終行まで解析終わり

    with open(output_pivot, 'w', encoding='utf-8') as fOut:
        fOut.write(json.dumps(data, indent=4, ensure_ascii=False))

    return output_pivot
