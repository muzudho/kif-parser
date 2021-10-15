from os import error
import re


class CommentP():
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

    def from_pivot(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        return f'{s}#{row_data["comment"]}\n'


comment_p = CommentP()


class ExplanationP():
    def __init__(self):
        self._explanation_statement = re.compile(r"^(\s)*\*([^#]*)#?(.+)?$")

    def match(self, line):
        return self._explanation_statement.match(line)

    def to_pivot(self, data, row_number, indent, explanation, comment):
        data[f'{row_number}'] = {
            "type": "explanation",
        }

        if indent:
            data[f'{row_number}']["indent"] = indent

        if explanation:
            data[f'{row_number}']["explanation"] = explanation

        if comment:
            data[f'{row_number}']["comment"] = comment

    def from_pivot(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        s += f'*{row_data["explanation"]}'

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f'{s}\n'


explanation_p = ExplanationP()


class BookmarkP():
    def __init__(self):
        self._bookmark_statement = re.compile(r"^(\s)*\&([^#]*)#?(.*)?$")

    def match(self, line):
        return self._bookmark_statement.match(line)

    def to_pivot(self, data, row_number, bookmark):
        data[f'{row_number}'] = {
            "type": "bookmark",
            "bookmark": f"{bookmark}",
        }

    def from_pivot(self, row_data):
        s = ""

        if "indent" in row_data:
            s += row_data["indent"]

        s += f'&{row_data["bookmark"]}'

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f'{s}\n'


bookmark_p = BookmarkP()


class KeyValuePairStatementP():
    """TODO 対局情報は　`ユーザが任意のものを追加できる`　と `棋譜ファイル KIF 形式` にある"""

    def __init__(self):
        # Example: `キーワード：オプション # コメント`
        # トリムしていません
        self._pattern = re.compile(
            r"^([^：]*)：([^#]*)#?(.*)?$")

    def match(self, line):
        return self._pattern.match(line)

    def to_pivot(self, data, row_number, key, value, comment):
        dict = {
            "type": "keyValuePair",
            "key": f"{key}",
        }

        if value:
            dict["value"] = value

        if comment:
            dict["comment"] = comment

        data[f'{row_number}'] = dict

    def from_pivot(self, key, value, comment):
        s = ""

        if key:
            s += key

        s += "："

        if value:
            s += value

        if comment:
            s += f"#{comment}"

        return f"{s}\n"


key_value_pair_statement_p = KeyValuePairStatementP()


class PlayerPhaseP():
    def __init__(self):
        self._player_phase_list = ['先手', '後手', '下手', '上手']

    def choices(self):
        return "|".join(self._player_phase_list)


player_phase_p = PlayerPhaseP()


class MovesHeaderStatementP():
    """指し手リストのヘッダー パーサー

    Examples
    --------
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

    def from_pivot(self, row_data):
        s = row_data["movesHeader"]

        if "comment" in row_data:
            s += f'#{row_data["comment"]}'

        return f"{s}\n"


moves_header_statement_p = MovesHeaderStatementP()


class MoveStatementP():
    def __init__(self):
        # 棋譜ファイル KIF 形式
        # -------------------
        # Example: `1 ７六歩(77) ( 0:16/00:00:16)`
        # Example: `2 ３四歩(33) ( 0:00/00:00:00)`
        # Example: `3 中断 ( 0:03/ 0:00:19)`
        #
        # 将棋所
        # -----
        # Example: `   1 ７六歩(77)    (00:01 / 00:00:01)`
        # Example: `  22 同　角(88)    (00:01 / 00:00:11)`
        #
        # Shogi GUI
        # ---------
        # Example: `   1 ７六歩(77)        ( 0:00/00:00:00)`
        self._move_statement = re.compile(
            r"^\s*(\d+)\s+([^ ]+)\s*\(?\s*([0-9:]+)?\s*/?\s*([0-9:]+)?\s*\)?(.*)$")

    def match(self, line):
        return self._move_statement.match(line)

    def from_pivot(self, row_data):
        kifu_text = ""

        if "moves" in row_data:
            # 数
            moves = row_data["moves"]
            kifu_text += f"{moves:>4} "

        if "move" in row_data:
            move = row_data["move"]

            move_text = ""
            # 半角スペース幅
            spaces = 14

            if "sign" in move:
                sign = move["sign"]
                move_text += f"{sign}"
                spaces -= sign_p.half_width(sign)

            if "dstFile" in move:
                dst_file = move["dstFile"]
                dst_rank = move["dstRank"]
                move_text += f"{dst_file}{dst_rank}"
                spaces -= 4

            if "dst" in move:
                dst = move["dst"]
                if dst == 'Same':
                    move_text += "同　"
                    spaces -= 4
                else:
                    move_text += f"{dst}"
                    spaces -= 2

            if "pieceType" in move:
                piece_type = move["pieceType"]
                move_text += f"{piece_type}"
                spaces -= piece_type_p.half_width(piece_type)

            if "drop" in move:
                drop = move["drop"]
                if drop:
                    move_text += "打"
                    spaces -= 2

            if "promotion" in move:
                pro = move["promotion"]
                if pro:
                    move_text += "成"
                    spaces -= 2

            if "srcFile" in move:
                srcFile = move["srcFile"]
                srcRank = move["srcRank"]
                move_text += f"({srcFile}{srcRank})"
                spaces -= 4

            # 左にスペースを詰めます
            move_text += ''.ljust(spaces, ' ')

            kifu_text += f"{move_text}"

        # Expended time（消費時間）
        if "time" in row_data:
            time = row_data["time"]
            timeMin = time["min"]  # minute（分）
            timeSec = time["sec"]  # second（秒）
        else:
            time = None

        # Total expended time（消費時間合計）
        if "total" in row_data:
            total = row_data["total"]
            totalExpendedTimeHr = total["hr"]  # hour（時）
            totalMin = total["min"]  # minute（分）
            totalSec = total["sec"]  # second（秒）
        else:
            total = None

        if time and total:
            kifu_text += f"({timeMin:02}:{timeSec:02} / {totalExpendedTimeHr:02}:{totalMin:02}:{totalSec:02})"

        return f"{kifu_text}\n"


move_statement_p = MoveStatementP()


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
        data[f'{row_number}']["time"] = {}
        data[f'{row_number}']["time"]["min"] = min
        data[f'{row_number}']["time"]["sec"] = sec


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
        data[f'{row_number}']["total"] = {}
        data[f'{row_number}']["total"]["hr"] = hr
        data[f'{row_number}']["total"]["min"] = min
        data[f'{row_number}']["total"]["sec"] = sec


total_expended_time_p = TotalExpendedTimeP()


class JudgeStatement1P():
    def __init__(self):
        # Example: `まで64手で後手の勝ち`
        self._judge_statement1 = re.compile(
            r"^まで(\d+)手で(先手|後手|下手|上手)の(反則勝ち|反則負け|勝ち)$")

    def match(self, line):
        return self._judge_statement1.match(line)

    def from_pivot(self, moves, winner, judge):
        # Example: `まで64手で後手の勝ち`
        return f"まで{moves}手で{winner}の{judge}\n"

    def to_pivot(self, data, row_number, moves, playerPhase, judge):
        data[f'{row_number}'] = {
            "type": "result",
            "moves": f"{moves}",
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

    def from_pivot(self, moves, judge):
        # Example: `まで63手で中断`
        return f"まで{moves}手で{judge}\n"

    def to_pivot(self, data, row_number, moves, judge):
        data[f'{row_number}'] = {
            "type": "result",
            "moves": f"{moves}",
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

    def from_pivot(self, moves, reason, winner, judge):
        # Example: `まで52手で時間切れにより後手の勝ち`
        return f"まで{moves}手で{reason_p.from_pivot(reason)}により{winner}の{judge}\n"

    def to_pivot(self, data, row_number, moves, reason, playerPhase, judge):
        data[f'{row_number}'] = {
            "type": "result",
            "moves": f"{moves}",
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
