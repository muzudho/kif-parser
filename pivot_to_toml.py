import os
import glob
import json
import sys
import shutil
from collections import OrderedDict
from scripts.toml_specification import player_phase_p, handicap_p, \
    judge_statement1_p, judge_statement2_p, judge_statement3_p, move_statement_p, \
    variation_label_statement_p
import argparse
from remove_all_temporary import remove_all_temporary
from remove_all_output import remove_all_output


def convert_pivot_to_toml(pivot_file, output_folder='temporary/toml', done_folder='temporary/pivot-done'):

    # basename
    try:
        basename = os.path.basename(pivot_file)
    except:
        print(f"Error: pivot_file={pivot_file} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None, None

    toml_file = ""

    with open(pivot_file, encoding='utf-8') as f:
        data = json.loads(f.read(), object_pairs_hook=OrderedDict)

        toml_text = ""
        buffer = ""
        comment_buffer = []
        explanation_buffer = []

        # 棋譜は 文書構造であり 意味でまとまってないので（コメントはどこにでもある）
        # それでは不便なので ある程度の区画にまとめます
        # また、コメントが何に係っているのか分からないので、順序を変えることが正しく行えません
        #
        # * "<COMMENT>" section
        # * "<EXPLANATION>" section
        # * "<BOOKMARK>" section
        # * "<GAMEINFO>" section
        # * "<MOVES>" section
        #   * Move
        #   * VariationLabel
        # * "<RESULT>" section
        pre_section_type = ""  # 分かりやすい目印

        # JSON to TOML
        for row_number, row_data in data.items():

            row_type = row_data["type"]

            if pre_section_type == "<COMMENT>" and row_type != "comment":
                # 連続するコメント行の切り替わり時
                items = "''',\n    '''".join(comment_buffer)
                comment_buffer = []

                # コメントをバッファーへ出力
                #
                # Example:
                #
                # comment = [
                #     '''aaaa''',
                #     '''bbbb''',
                #     '''cccc'''
                # ]
                buffer += f"""comment = [\n    '''{items}'''\n]\n"""

            elif pre_section_type == "<EXPLANATION>" and row_type != "explanation":
                # 連続する解説の切り替わり時
                items = "''',\n    '''".join(explanation_buffer)
                explanation_buffer = []

                # Example:
                #
                # explanation = [
                #     '''aaaa''',
                #     '''bbbb''',
                #     '''cccc'''
                # ]
                buffer += f"""explanation = [\n    '''{items}'''\n]\n"""

            #

            #

            if row_type == "comment":
                # 1. コメントに キーが無いことによる重複を避けてください
                # 2. コメント行は連続することを考慮し、常に配列にします

                if pre_section_type != "<COMMENT>":
                    # セクション切り替わり時
                    toml_text += buffer  # flush
                    buffer = f"""\n[[section]]\n"""

                # コメント１行ごとに配列の１要素とします
                toml_text += buffer  # flush
                buffer = ""

                comment = row_data["comment"]

                # TOMLのコメントにすると、パーサーがコメントを読み込んでくれないので、
                # コメントにはしません
                # TODO 文字列エスケープどうする？
                comment_buffer.append(comment)

                pre_section_type = "<COMMENT>"

            elif row_type == "explanation":
                # 1. 指し手等へのコメントに キーが無いことによる重複を避けてください
                # 2. 指し手等へのコメント行は連続することを考慮し、常に配列にします

                if pre_section_type != "<EXPLANATION>":
                    # セクション切り替わり時
                    toml_text += buffer  # flush
                    buffer = f"""\n[[section]]\n"""

                # 指し手等へのコメント１行ごとに配列の１要素とします
                toml_text += buffer  # flush
                buffer = ""

                explanation = row_data["explanation"]

                # TODO 文字列エスケープどうする？
                explanation_buffer.append(explanation)

                pre_section_type = "<EXPLANATION>"

            elif row_type == "bookmark":
                # 1. しおりに キーが無いことによる重複を避けてください
                # 2. しおりは連続する用途ではありません（だから連続しても別のセクションとして扱います）

                if pre_section_type != "<BOOKMARK>":
                    # セクション切り替わり時
                    toml_text += buffer  # flush
                    buffer = f"""\n[[section]]\n"""

                # しおり１行ごとに配列の１要素とします
                toml_text += buffer  # flush
                buffer = ""

                bookmark = row_data["bookmark"]

                # TODO 文字列エスケープどうする？
                buffer += f"""bookmark='''{bookmark}'''\n"""

                pre_section_type = "<BOOKMARK>"

            elif row_type == "Move":
                # 指し手

                if pre_section_type != "<MOVES>":
                    # セクション切り替わり時
                    toml_text += buffer  # Flush
                    # Sub table
                    buffer = f"""\n[[section]]
[section.moves]
"""

                buffer += move_statement_p.from_pivot(
                    moves=row_data["moves"],
                    elapsedTime=row_data["elapsedTime"],
                    totalElapsedTime=row_data["totalElapsedTime"],
                    move=row_data["move"])

                pre_section_type = "<MOVES>"

            elif row_type == "variationLabel":
                # 変化手順（棋譜の分岐）のジャンプ先ラベル

                # セクションを切り替えます
                toml_text += buffer  # Flush
                buffer = f"""\n[[section]]
[section.moves]
"""

                buffer += variation_label_statement_p.from_pivot(
                    moves=row_data["moves"])

                pre_section_type = "<MOVES>"

            elif row_type == "Handicap":

                if pre_section_type != "<GAMEINFO>":
                    # セクション切り替わり時
                    toml_text += buffer  # Flush
                    buffer = f"""\n[[section]]
[section.gameinfo]
"""

                handicap = handicap_p.from_pivot(row_data["handicap"])
                buffer += f"handicap='{handicap}'\n"

                pre_section_type = "<GAMEINFO>"

            elif row_type == "player":

                if pre_section_type != "<GAMEINFO>":
                    # セクション切り替わり時
                    toml_text += buffer
                    buffer = f"""\n[[section]]
[section.gameinfo]
"""

                player_phase = player_phase_p.from_pivot(
                    row_data["playerPhase"])

                player_name = row_data["playerName"]

                buffer += f"""{player_phase}='''{player_name}'''
"""

                pre_section_type = "<GAMEINFO>"

            elif row_type == "result":

                if pre_section_type != "<RESULT>":
                    # セクション切り替わり時
                    toml_text += buffer
                    buffer = f"""\n[[section]]
[section.result]
"""

                if "reason" in row_data:
                    # Example: `まで52手で時間切れにより後手の勝ち`
                    moves = row_data["moves"]
                    reason = row_data['reason']
                    winner = row_data["winner"]
                    judge = row_data["judge"]
                    buffer += judge_statement3_p.from_pivot(
                        moves, reason, winner, judge)
                elif "winner" in row_data:
                    # Example: `まで64手で後手の勝ち`
                    moves = row_data["moves"]
                    winner = row_data["winner"]
                    judge = row_data["judge"]
                    buffer += judge_statement1_p.from_pivot(
                        moves, winner, judge)
                else:
                    # Example: `まで63手で中断`
                    moves = row_data["moves"]
                    judge = row_data["judge"]
                    buffer += judge_statement2_p.from_pivot(
                        moves, judge)

                pre_section_type = "<RESULT>"

            elif row_data["type"] == "appendix":
                # 元の `.kifu` には無い、このアプリケーションが付けた情報なので、無視します
                pass
            else:
                # Error
                print(
                    f"Error: pivot_to_toml.py unimplemented row_number={row_number} row_data={row_data}")
                return None, None

        if buffer != "":
            toml_text += buffer
            buffer = ""

        # New .kifu ファイル出力
        toml_file = os.path.join(output_folder, f"{stem}.toml")
        with open(toml_file, mode='w', encoding='utf-8') as fOut:
            fOut.write(toml_text)

    # with句を抜けて、ファイルを閉じたあと
    # ファイルの移動
    done_pivot_file = shutil.move(
        pivot_file, os.path.join(done_folder, basename))

    return toml_file, done_pivot_file


def __main(debug=False):
    if not debug:
        # 出力フォルダーを空っぽにします
        remove_all_output(echo=False)

    # PIVOTファイル一覧
    pivot_files = glob.glob("./temporary/pivot/*.json")
    for pivot_file in pivot_files:
        toml_file, done_pivot_file = convert_pivot_to_toml(pivot_file)
        if toml_file is None:
            print(f"Parse fail. pivot_file={pivot_file}")

    if not debug:
        # 変換の途中で作ったファイルは削除します
        remove_all_temporary(echo=False)


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":
    # Description
    parser = argparse.ArgumentParser(
        description='Convert from .json (PIVOT) file to .toml file.')
    # `--` - Option arg
    # `action='store_true'` - Flag
    parser.add_argument(
        '--debug', action='store_true', help='Leave temporary files created during the conversion process without deleting them.')
    args = parser.parse_args()

    __main(debug=args.debug)
