import os
import json
import sys
from collections import OrderedDict
from scripts.toml_specification import player_phase_p, \
    judge_statement1_p, judge_statement2_p, judge_statement3_p, move_statement_p, \
    key_value_pair_statement_p


def convert_pivot_to_toml(pivot_file, output_folder):

    # basename
    try:
        basename = os.path.basename(pivot_file)
    except:
        print(f"Error: pivot_file={pivot_file} except={sys.exc_info()[0]}")
        raise

    stem, extention = os.path.splitext(basename)
    if extention.lower() != '.json':
        return None

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

        elif row_type == "move":
            # 指し手

            if pre_section_type != "<MOVES>":
                # セクション切り替わり時
                toml_text += buffer  # Flush
                # Sub table
                buffer = f"""\n[[section]]
[section.moves]
"""

            buffer += move_statement_p.from_pivot(
                moveNum=row_data["moveNum"],  # Move num（n手目）
                time=row_data["time"],  # Expended time（消費時間）
                total=row_data["total"],  # Total expended time（消費時間合計）
                move=row_data["move"])

            pre_section_type = "<MOVES>"

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

        elif row_type == "keyValuePair":

            if pre_section_type != "<GAMEINFO>":
                # セクション切り替わり時
                toml_text += buffer  # Flush
                buffer = f"""\n[[section]]
[section.gameinfo]
"""

            key = row_data["key"]

            if "value" in row_data:
                value = row_data["value"]
            else:
                value = None

            if "comment" in row_data:
                comment = row_data["comment"]
            else:
                comment = None

            buffer += key_value_pair_statement_p.from_pivot(
                row_number, key, value, comment)

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
                moveNum = row_data["moveNum"]
                reason = row_data['reason']
                winner = row_data["winner"]
                judge = row_data["judge"]
                buffer += judge_statement3_p.from_pivot(
                    moveNum, reason, winner, judge)
            elif "winner" in row_data:
                # Example: `まで64手で後手の勝ち`
                moveNum = row_data["moveNum"]
                winner = row_data["winner"]
                judge = row_data["judge"]
                buffer += judge_statement1_p.from_pivot(
                    moveNum, winner, judge)
            else:
                # Example: `まで63手で中断`
                moveNum = row_data["moveNum"]
                judge = row_data["judge"]
                buffer += judge_statement2_p.from_pivot(
                    moveNum, judge)

            pre_section_type = "<RESULT>"

        elif row_data["type"] == "appendix":
            # 元の `.kifu` には無い、このアプリケーションが付けた情報なので、無視します
            pass
        else:
            # Error
            print(
                f"Error: pivot_to_toml.py unimplemented row_number={row_number} row_data={row_data} pivot_file=[{pivot_file}]")
            return None

    if buffer != "":
        toml_text += buffer
        buffer = ""

    # .toml ファイル出力
    toml_file = os.path.join(output_folder, f"{stem}.toml")
    with open(toml_file, mode='w', encoding='utf-8') as fOut:
        fOut.write(toml_text)

    return toml_file
