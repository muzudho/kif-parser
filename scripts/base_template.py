from scripts.kifu_specification import sign_p, piece_type_p, judge_statement1_p, judge_statement2_p, judge_statement3_p


class BaseTemplate():
    """将棋所、ShogiGUIに共通するテンプレート"""

    def __init__(self):
        pass

    def comment_row(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        return f'{s}#{row_data["comment"]}\n'

    def explain_row(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        s += f'*{row_data["explain"]}'

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f'{s}\n'

    def bookmark_row(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        s += f'&{row_data["bookmark"]}'

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f'{s}\n'

    def moves_header_row(self, row_data):
        s = row_data["movesHeader"]

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f"{s}\n"

    def key_value_pair_row(self, row_data):
        key = row_data["key"]

        if "value" in row_data:
            value = row_data["value"]
        else:
            value = None

        if "comment" in row_data:
            comment = row_data["comment"]
        else:
            comment = None

        text = ""

        if key:
            text += key

        text += "："

        if value:
            text += value

        if comment:
            text += f"#{comment}"

        return f"{text}\n"

    def result_row(self, row_data):
        if "reason" in row_data:
            # Example: `まで52手で時間切れにより後手の勝ち`
            num = row_data["num"]  # Move num
            reason = row_data['reason']
            winner = row_data["winner"]
            judge = row_data["judge"]
            return judge_statement3_p.from_pivot(
                num, reason, winner, judge)
        elif "winner" in row_data:
            # Example: `まで64手で後手の勝ち`
            num = row_data["num"]
            winner = row_data["winner"]
            judge = row_data["judge"]
            return judge_statement1_p.from_pivot(
                num, winner, judge)
        else:
            # Example: `まで63手で中断`
            num = row_data["num"]
            judge = row_data["judge"]
            return judge_statement2_p.from_pivot(
                num, judge)
