from os import error
import re


class CommentRowP():
    """コメント行パーサー"""

    def __init__(self):
        self._comment_statement = re.compile(r"^([^#]*)#(.+)$")

    def match(self, line):
        return self._comment_statement.match(line)

    def to_pivot(self, data, row_number, indent, comment):
        data[f'{row_number}'] = {
            "type": "comment",
        }

        if indent:
            data[f'{row_number}']["indent"] = indent

        if comment:
            data[f'{row_number}']["comment"] = comment


comment_row_p = CommentRowP()


class ExplainRowP():
    """指し手の解説行パーサー"""

    def __init__(self):
        self._explain_statement = re.compile(r"^(\s)*\*([^#]*)#?(.+)?$")

    def match(self, line):
        return self._explain_statement.match(line)

    def to_pivot(self, data, row_number, indent, explain, comment):
        data[f'{row_number}'] = {
            "type": "explain",
        }

        if indent:
            data[f'{row_number}']["indent"] = indent

        if explain:
            data[f'{row_number}']["explain"] = explain

        if comment:
            data[f'{row_number}']["comment"] = comment


explain_row_p = ExplainRowP()


class BookmarkRowP():
    """しおり行パーサー"""

    def __init__(self):
        # indent, bookmark, comment
        self._bookmark_statement = re.compile(r"^(\s*)\&([^#]*)#?(.*)?$")

    def match(self, line):
        return self._bookmark_statement.match(line)

    def to_pivot(self, data, row_number, indent, bookmark, comment):
        data[f'{row_number}'] = {
            "type": "bookmark",
        }

        if indent:
            data[f'{row_number}']["indent"] = indent

        if bookmark:
            data[f'{row_number}']["bookmark"] = bookmark

        if comment:
            data[f'{row_number}']["comment"] = comment


bookmark_row_p = BookmarkRowP()


class KeyValuePairRowP():
    """キー値ペア行
    対局情報は　`ユーザが任意のものを追加できる`　と `棋譜ファイル KIF 形式` にあります"""

    def __init__(self):
        # Example: `キーワード：オプション # コメント`
        # トリムしていません
        self._pattern = re.compile(
            r"^([^：]*)：([^#]*)#?(.*)?$")

    def match(self, line):
        return self._pattern.match(line)

    def to_pivot(self, data, row_number, key, value, comment):
        dict = {
            "type": "kvPair",  # Key-value pair
            "key": f"{key}",
        }

        if value:
            dict["value"] = value

        if comment:
            dict["comment"] = comment

        data[f'{row_number}'] = dict


key_value_pair_row_p = KeyValuePairRowP()


class PlayerPhaseP():
    def __init__(self):
        self._player_phase_list = ['先手', '後手', '下手', '上手']

    def choices(self):
        return "|".join(self._player_phase_list)


player_phase_p = PlayerPhaseP()


class MovesHeaderRowP():
    """指し手リストのヘッダー行パーサー

    Example
    -------
    棋譜ファイル KIF 形式
    `手数----指手---------消費時間-- # この行は、なくてもいい`
    """

    def __init__(self):
        self._moves_header_statement = re.compile(
            r"^([-]*手数[-]+指手[-]+消費時間[-]+[^#]*)#?(.*)?$")

    def match(self, line):
        return self._moves_header_statement.match(line)

    def to_pivot(self, data, row_number, moves_header, comment):
        data[f'{row_number}'] = {
            "type": "movesHeader",
            "movesHeader": moves_header,
        }

        if comment:
            data[f'{row_number}']["comment"] = comment


moves_header_row_p = MovesHeaderRowP()


class MoveRowP():
    def __init__(self):
        """
        Example
        -------
        棋譜ファイル KIF 形式
        `1 ７六歩(77) ( 0:16/00:00:16)`
        `2 ３四歩(33) ( 0:00/00:00:00)`
        `3 中断 ( 0:03/ 0:00:19)`

        将棋所
        `   1 ７六歩(77)    (00:01 / 00:00:01)`
        `  22 同　角(88)    (00:01 / 00:00:11)`

        Shogi GUI
        `   1 ７六歩(77)        ( 0:00/00:00:00)`

        末尾にコメントが打てる
        """
        self._move_row = re.compile(
            r"^\s*(\d+)\s+([^ ]+)\s*\(?\s*([0-9:]+)?\s*/?\s*([0-9:]+)?\s*\)?\s*#?(.*)?$")
        #         -----   -------    --------------         ---------            ----
        #         1       2          3                      4                    5
        #         num     move       time                   total                comment

    def match(self, line):
        return self._move_row.match(line)


move_row_p = MoveRowP()


class MoveP():
    def __init__(self):
        # Example: `７六歩(77)`
        # Example: `同　角(88)`
        # Example: `４九角打`
        self._move = re.compile(
            r"^(１|２|３|４|５|６|７|８|９)?(一|二|三|四|五|六|七|八|九)?(同　)?(玉|飛|龍|竜|角|馬|金|銀|成銀|全|桂|成桂|圭|香|成香|杏|歩|と)(打|成)?(\(\d+\))?(.*)$")

    def match(self, line):
        return self._move.match(line)


move_p = MoveP()


class PieceTypeP():
    def __init__(self):
        # 逆引き対応（複数あるものは先にくるものが選ばれるものとします）
        self._piece_type = ['玉', '飛', '龍', '竜', '角', '馬', '金', '銀', '成銀', '全',
                            '桂', '成桂', '圭', '香', '成香', '杏', '歩', 'と']

        # 半角スペース幅
        self._piece_type_half_width = {
            '玉': 2,
            '飛': 2,
            '龍': 2,
            '竜': 2,
            '角': 2,
            '馬': 2,
            '金': 2,
            '銀': 2,
            '成銀': 4,
            '全': 2,
            '桂': 2,
            '成桂': 4,
            '圭': 2,
            '香': 2,
            '成香': 4,
            '杏': 2,
            '歩': 2,
            'と': 2,
        }

    def half_width(self, piece_type):
        if piece_type in self._piece_type_half_width.keys():
            return self._piece_type_half_width[piece_type]

        return piece_type


piece_type_p = PieceTypeP()


class SignP():
    def __init__(self):
        # 逆引き対応
        self._sign = ['中断', '投了', '持将棋', '千日手', '詰み', '切れ負け', '反則勝ち', '反則負け', '入玉勝ち', '不戦勝', '不戦敗',  # KIFの仕様にあるもの
                      '勝ち',  # 追加
                      ]

        # 半角スペースサイズ
        self._sign_half_width = {
            '中断': 4,
            '投了': 4,
            '持将棋': 6,
            '千日手': 6,
            '詰み': 4,
            '切れ負け': 8,
            '反則勝ち': 8,
            '反則負け': 8,
            '入玉勝ち': 8,
            '不戦勝': 6,
            '不戦敗': 6,
            '勝ち': 4,
        }

    def contains(self, key):
        return key in self._sign

    def half_width(self, sign):
        if sign in self._sign_half_width.keys():
            return self._sign_half_width[sign]

        return sign


sign_p = SignP()


class ExpendedTimeP():
    def __init__(self):
        # ↓ どっちもある
        # Example: `0:01`
        # Example: `00:01`
        self._expended_time = re.compile(r"^(\d+):(\d+)$")

    def match(self, line):
        return self._expended_time.match(line)

    def to_pivot(self, data, row_number, min, sec):
        """
        Parameters
        ----------
        min : int
            Minute
        sec : int
            Second
        """

        # とりあえず [時, 分, 秒] で持てる形にします
        # [時, 分, 秒, ミリ秒] も見据えます
        data[f'{row_number}']["time"] = [0, min, sec]


expended_time_p = ExpendedTimeP()


class TotalExpendedTimeP():
    def __init__(self):
        # Example: `00:00:16`
        self._total_expended_time = re.compile(r"^(\d+):(\d+):(\d+)$")

    def match(self, line):
        return self._total_expended_time.match(line)

    def to_pivot(self, data, row_number, hr, min, sec):
        """
        Parameters
        ----------
        hr : int
            Hour
        min : int
            Minute
        sec : int
            Second
        """

        # とりあえず [時, 分, 秒] で持てる形にします
        # [時, 分, 秒, ミリ秒] も見据えます
        data[f'{row_number}']["total"] = [hr, min, sec]


total_expended_time_p = TotalExpendedTimeP()


class ResultRowP():

    def from_pivot(self, row_data):
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


result_row_p = ResultRowP()


class JudgeStatement1P():
    def __init__(self):
        # Example: `まで64手で後手の勝ち`
        self._judge_statement1 = re.compile(
            r"^まで(\d+)手で(先手|後手|下手|上手)の(反則勝ち|反則負け|勝ち)$")

    def match(self, line):
        return self._judge_statement1.match(line)

    def from_pivot(self, num, winner, judge):
        # Example: `まで64手で後手の勝ち`
        return f"まで{num}手で{winner}の{judge}\n"

    def to_pivot(self, data, row_number, num, playerPhase, judge):
        data[f'{row_number}'] = {
            "type": "result",
            "num": f"{num}",
            "winner": f"{playerPhase}",
            "judge": f"{judge}",
        }


judge_statement1_p = JudgeStatement1P()


class JudgeStatement2P():
    def __init__(self):
        # Example: `まで63手で中断`
        self._judge_statement2 = re.compile(r"^まで(\d+)手で(中断|持将棋|千日手)$")

    def match(self, line):
        return self._judge_statement2.match(line)

    def from_pivot(self, num, judge):
        # Example: `まで63手で中断`
        return f"まで{num}手で{judge}\n"

    def to_pivot(self, data, row_number, num, judge):
        data[f'{row_number}'] = {
            "type": "result",
            "num": f"{num}",
            "judge": f"{judge}",
        }


judge_statement2_p = JudgeStatement2P()


class JudgeStatement3P():
    def __init__(self):
        # Example: `まで52手で時間切れにより後手の勝ち`
        self._judge_statement3 = re.compile(
            r"^まで(\d+)手で(時間切れ)により(先手|後手|下手|上手)の(勝ち)$")

    def match(self, line):
        return self._judge_statement3.match(line)

    def from_pivot(self, num, reason, winner, judge):
        # Example: `まで52手で時間切れにより後手の勝ち`
        return f"まで{num}手で{reason_p.from_pivot(reason)}により{winner}の{judge}\n"

    def to_pivot(self, data, row_number, num, reason, playerPhase, judge):
        data[f'{row_number}'] = {
            "type": "result",
            "num": f"{num}",
            "reason": f"{reason}",
            "winner": f"{playerPhase}",
            "judge": f"{judge}",
        }


judge_statement3_p = JudgeStatement3P()


class ReasonP():
    def __init__(self):
        # 逆引き対応
        self._reason = {
            '時間切れ': 'TimeUp',
        }

    def to_pivot(self, reason):
        if reason in self._reason:
            return self._reason[reason]

        return reason

    def from_pivot(self, reason):
        items = [k for k, v in self._reason.items() if v == reason]
        return items[0]


reason_p = ReasonP()
