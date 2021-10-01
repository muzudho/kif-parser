import glob
import os
import json
import shutil

"""
from scripts.toml_specification import comment_p, explanation_p, bookmark_p, player_phase_p, \
    player_statement_p, handicap_p, piece_type_p, zenkaku_number_p, kanji_number_p, sign_p, \
    move_statement_p, move_p, elapsed_time_p, total_elapsed_time_p, judge_statement1_p, \
    judge_statement2_p, judge_statement3_p, reason_p
"""

import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output
import sys
import tomli


def copy_toml_from_input(output_folder='temporary/toml'):
    """inputフォルダーにある `*.toml` ファイルを output_folder へコピーします"""

    input_files = glob.glob("./input/*.toml")
    for input_file in input_files:
        # basename
        try:
            basename = os.path.basename(input_file)
        except:
            print(f"Error: input_file={input_file} except={sys.exc_info()[0]}")
            raise

        copy_file = os.path.join(output_folder, basename)
        shutil.copyfile(input_file, copy_file)


def convert_toml_to_pivot(toml_file, output_folder='temporary/pivot', done_folder='temporary/toml-done'):
    """.tomlファイルを読込んで、JSON (PIVOT) ファイルを出力します"""

    data = {}

    # basename
    try:
        basename = os.path.basename(toml_file)
    except:
        print(f"Error: toml_file={toml_file} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.toml':
        return

    # insert new extention
    out_path = os.path.join(output_folder, f"{stem}.json")

    # とりあえず KIFU を読んでみます
    row_number = 1
    with open(toml_file, encoding='utf-8') as f:

        s = f.read()
        text = s.rstrip()

        try:
            toml_dict = tomli.loads(text)
            print(f"toml_dict={toml_dict}")
        except tomli.TOMLDecodeError:
            # 構文エラーなど
            print(f"Yep, definitely not valid. toml_file={toml_file}")
            raise

        """
        lines = text.split('\n')
        for line in lines:

            # 指し手の解析
            result = move_statement_p.match(line)
            if result:
                moves = result.group(1)
                move = result.group(2)
                elapsedTime = result.group(3)
                totalElapsedTime = result.group(4)

                data[f'{row_number}'] = {
                    "type": "Move",
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

                        unknown = result2.group(7)
                        if unknown:
                            data[f'{row_number}']["move"]['Unknown'] = unknown

                    else:
                        data[f'{row_number}']["move"] = {"Unknown": move}

                row_number += 1
                continue

            # コメントの解析
            result = comment_p.match(line)
            if result:
                comment = result.group(1)
                comment_p.to_pibot(data, row_number, comment)

                row_number += 1
                continue

            # 指し手等の解説の解析
            result = explanation_p.match(line)
            if result:
                explanation = result.group(1)
                explanation_p.to_pibot(data, row_number, explanation)

                row_number += 1
                continue

            # しおりの解析
            result = bookmark_p.match(line)
            if result:
                bookmark = result.group(1)
                bookmark_p.to_pibot(data, row_number, bookmark)

                row_number += 1
                continue

            # プレイヤー名の解析
            result = player_statement_p.match(line)
            if result:
                player_phase = player_phase_p.to_pivot(result.group(1))
                player_name = result.group(2)
                player_statement_p.to_pivot(
                    data, row_number, player_phase, player_name)

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
                    "type": "Handicap",
                    "handicap": handicap,
                }

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
            print(f"Error: row_number={row_number} line={line}")
            return None, None

    with open(out_path, 'w', encoding='utf-8') as fOut:
        fOut.write(json.dumps(data, indent=4, ensure_ascii=False))

    # ファイルの移動
    done_path = shutil.move(toml_file, os.path.join(done_folder, basename))
    return out_path, done_path
        """
        return None, None


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output(echo=False)

    copy_toml_from_input()

    # TOMLファイル一覧
    toml_files = glob.glob("./temporary/toml/*.toml")
    for toml_file in toml_files:
        out_path, _done_path = convert_toml_to_pivot(
            toml_file, output_folder='output')

        if out_path is None:
            print(f"Parse fail. toml_file={toml_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .toml file to .json (PIVOT) file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)