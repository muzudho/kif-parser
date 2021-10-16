import os
import json
from scripts.kifu_specification import comment_row_p, explain_row_p, bookmark_row_p, \
    sign_p, \
    move_statement_p, move_p, expended_time_p, total_expended_time_p, judge_statement1_p, \
    judge_statement2_p, judge_statement3_p, reason_p, \
    moves_header_row_p, \
    key_value_pair_row_p
from scripts.generator_identification import generator_identification
from scripts.data_json_format import format_data_json
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
    output_pivot = os.path.join(output_folder, f"{stem}[kifu-pivot].json")

    # とりあえず KIFU を読んでみます
    row_number = 1
    with open(kifu_file, encoding='utf-8') as f:
        text = f.read().rstrip()

    # この棋譜を生成したソフトが何か当てに行きます
    shogi_dokoro, shogi_gui = generator_identification.read_all_text(text)
    # 0行目に情報を追加するものとします
    data[0] = {
        "type": "metadata",
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

        # Move（指し手）
        result = move_statement_p.match(line)
        if result:
            num = result.group(1)  # Move num
            m = result.group(2)  # Move
            time = result.group(3)  # Expended time（消費時間）
            total = result.group(4)  # Total expended time（消費時間合計）

            data[f'{row_number}'] = {
                "type": "move",
                "num": f"{num}"
            }

            # 指し手の詳細の解析
            if sign_p.contains(m):
                # [投了]とか [中断]とか [詰み]とか
                data[f'{row_number}']["m"] = {"sign": m}
            else:

                result2 = move_p.match(m)
                if result2:
                    data[f'{row_number}']["m"] = {}

                    # Destination file（行き先の筋）
                    x = result2.group(1)
                    if x:
                        data[f'{row_number}']["m"]["x"] = x

                    # Destination rank（行き先の行）
                    y = result2.group(2)
                    if y:
                        data[f'{row_number}']["m"]["y"] = y

                    # 筋と段に分かれていない表記の場合
                    dst = result2.group(3)
                    if dst:
                        if dst == '同　':
                            data[f'{row_number}']["m"]["dst"] = dst
                        else:
                            # Error
                            print(f"Error: dst={dst}")
                            return None

                    pt = result2.group(4)  # Piece type（先後の無い駒種類）
                    if pt:
                        data[f'{row_number}']["m"]["pt"] = pt

                    dropOrPromotion = result2.group(5)
                    if dropOrPromotion:
                        # Drop（打つ）
                        if dropOrPromotion == '打':
                            data[f'{row_number}']["m"]["drop"] = dropOrPromotion
                        # Promote（成り）
                        elif dropOrPromotion == '成':
                            data[f'{row_number}']["m"]["pro"] = dropOrPromotion
                        else:
                            # Error
                            print(
                                f"Error: dropOrPromotion={dropOrPromotion}")
                            return None

                    src = result2.group(6)
                    if src:
                        # Example `(77)`
                        square = int(src[1:-1])
                        data[f'{row_number}']["m"]["src"] = square

                    # 後ろにコメントが書けるはず
                    unimplemented = result2.group(7)
                    if unimplemented:
                        data[f'{row_number}']["m"]["unimplemented"] = unimplemented

                else:
                    data[f'{row_number}']["m"] = {"Unknown": m}

            # Expended time（消費時間）
            if time:
                result2 = expended_time_p.match(time)
                if result2:
                    min = int(result2.group(1))  # minute
                    sec = int(result2.group(2))  # second
                    expended_time_p.to_pivot(
                        data, row_number, min, sec)

            # Total expended time（消費時間合計）
            if total:
                result2 = total_expended_time_p.match(total)
                if result2:
                    hr = int(result2.group(1))  # hour
                    min = int(result2.group(2))  # minute
                    sec = int(result2.group(3))  # second
                    total_expended_time_p.to_pivot(
                        data, row_number, hr, min, sec)

            row_number += 1
            continue

        # Comment row（コメント行）
        result = comment_row_p.match(line)
        if result:
            comment_row_p.to_pivot(
                data,
                row_number,
                indent=result.group(1),
                comment=result.group(2))
            row_number += 1
            continue

        # Explain row（指し手等の解説行）
        result = explain_row_p.match(line)
        if result:
            explain_row_p.to_pivot(
                data,
                row_number,
                indent=result.group(1),
                explain=result.group(2),
                comment=result.group(3))
            row_number += 1
            continue

        # Bookmark row （しおり行）
        result = bookmark_row_p.match(line)
        if result:
            indent = result.group(1)
            bookmark = result.group(2)
            comment = result.group(3)
            bookmark_row_p.to_pivot(
                data, row_number, indent, bookmark, comment)
            row_number += 1
            continue

        # 指し手リストの先頭行
        # Example: `手数----指手---------消費時間-- # この行は、なくてもいい`
        result = moves_header_row_p.match(line)
        if result:
            moves_header = result.group(1)
            comment = result.group(2)
            moves_header_row_p.to_pivot(
                data, row_number, moves_header, comment)
            row_number += 1
            continue

        # Key-value pair row（キー値ペア行）
        result = key_value_pair_row_p.match(line)
        if result:
            key = result.group(1)
            value = result.group(2)
            comment = result.group(3)
            key_value_pair_row_p.to_pivot(
                data, row_number, key, value, comment)
            row_number += 1
            continue

        # Example: `まで64手で後手の勝ち`
        result = judge_statement1_p.match(line)
        if result:
            num = result.group(1)
            player_phase = result.group(2)
            judge = result.group(3)
            judge_statement1_p.to_pivot(
                data, row_number, num, player_phase, judge)
            row_number += 1
            continue

        # Example: `まで63手で中断`
        result = judge_statement2_p.match(line)
        if result:
            num = result.group(1)
            judge = result.group(2)
            judge_statement2_p.to_pivot(data, row_number, num, judge)
            row_number += 1
            continue

        # Example: `まで52手で時間切れにより後手の勝ち`
        result = judge_statement3_p.match(line)
        if result:
            num = result.group(1)
            reason = reason_p.to_pivot(result.group(2))
            player_phase = result.group(3)
            judge = result.group(4)
            judge_statement3_p.to_pivot(
                data, row_number, num, reason, player_phase, judge)
            row_number += 1
            continue

        # 解析漏れ
        print(
            f"Error: kifu_to_pivot.py unimplemented row_number={row_number} line=[{line}] kifu_file=[{kifu_file}]")
        return None

    # 最終行まで解析終わり

    with open(output_pivot, 'w', encoding='utf-8') as fOut:
        # JSON出力
        # dumps そのままでは、配列の要素が複数行に改行されるのが気になる
        text = json.dumps(data, indent=4, ensure_ascii=False)

        # そこで再整形
        text = format_data_json(text)

        fOut.write(text)

    return output_pivot
