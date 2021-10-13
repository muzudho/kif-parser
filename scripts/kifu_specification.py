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
            "comment": comment,
        }

        if indent:
            data[f'{row_number}']["indent"]=indent

comment_p = CommentP()


class ExplanationP():
    def __init__(self):
        self._explanation_statement = re.compile(r"^\*(.+)$")

    def match(self, line):
        return self._explanation_statement.match(line)

    def to_pivot(self, data, row_number, explanation):
        data[f'{row_number}'] = {
            "type": "explanation",
            "explanation": f"{explanation}",
        }


explanation_p = ExplanationP()


class BookmarkP():
    def __init__(self):
        self._bookmark_statement = re.compile(r"^\&(.+)$")

    def match(self, line):
        return self._bookmark_statement.match(line)

    def to_pivot(self, data, row_number, bookmark):
        data[f'{row_number}'] = {
            "type": "bookmark",
            "bookmark": f"{bookmark}",
        }


bookmark_p = BookmarkP()


class AnyGameInfoKeyValuePairStatementP():
    """TODO 対局情報は　`ユーザが任意のものを追加できる`　と `棋譜ファイル KIF 形式` にある"""

    def __init__(self):
        # Example: `キーワード：オプション # コメント`
        self._pattern = re.compile(
            r"^\s*([^：]+)\s*：\s*([^#]*)\s*#?(.*)?$")

    def match(self, line):
        return self._pattern.match(line)

    def to_pivot(self, data, row_number, key, value, comment):
        dict = {
            "type": "anyGameInfo",
            "key": f"{key}",
        }

        if value:
            dict["value"] = value

        if comment:
            dict["comment"] = comment

        data[f'{row_number}'] = dict

    def from_pivot(self, key, value, comment):
        if comment:
            return f"{key}：{value} # {comment}\n"

        return f"{key}：{value}\n"


any_game_info_key_value_pair_statement_p = AnyGameInfoKeyValuePairStatementP()


class StartTimeStatementP():
    """開始日時文パーサー"""

    def __init__(self):
        # Example: `開始日時：1999/07/15(木) 19:07:12` - 棋譜ファイル KIF 形式
        # Example: `開始日時：2021/10/02 22:35:06` - ShogiGUI
        self._start_time_statement = re.compile(
            r"^開始日時：(\d{4}/\d{2}/\d{2}[^\s]* \d{2}:\d{2}:\d{2})$")

    def match(self, line):
        return self._start_time_statement.match(line)

    def to_pivot(self, data, row_number, start_time):
        data[f'{row_number}'] = {
            "type": "startTime",
            # TODO 書式を よくある書式に整形したい
            "startTime": f"{start_time}"
        }

    def from_pivot(self, startTime):
        return f"開始日時：{startTime}\n"


start_time_statement_p = StartTimeStatementP()


class EndTimeStatementP():
    """終了日時文パーサー"""

    def __init__(self):
        # Example: `終了日時：1999/07/15(木) 19:07:17` - 棋譜ファイル KIF 形式
        self._end_time_statement = re.compile(
            r"^終了日時：(\d{4}/\d{2}/\d{2}[^\s]* \d{2}:\d{2}:\d{2})$")

    def match(self, line):
        return self._end_time_statement.match(line)

    def to_pivot(self, data, row_number, end_time):
        data[f'{row_number}'] = {
            "type": "endTime",
            # TODO 書式を よくある書式に整形したい
            "endTime": f"{end_time}"
        }

    def from_pivot(self, endTime):
        return f"終了日時：{endTime}\n"


end_time_statement_p = EndTimeStatementP()


class PlayerPhaseP():
    def __init__(self):
        self._player_phase_list = ['先手', '後手', '下手', '上手']

    def choices(self):
        return "|".join(self._player_phase_list)


player_phase_p = PlayerPhaseP()


class PlayerStatementP():
    def __init__(self):
        self._player_name_statement = re.compile(
            # Player name may be blank
            r"^(" + player_phase_p.choices() + r")：(.*)$")

    def match(self, line):
        return self._player_name_statement.match(line)

    def to_pivot(self, data, row_number, player_phase, player_name):
        data[f'{row_number}'] = {
            "type": "player",
            "playerPhase": f"{player_phase}",
            "playerName": f"{player_name}",
        }


player_statement_p = PlayerStatementP()


class HandicapStatementP():
    def __init__(self):
        self._handicap_statement = re.compile(r"^手合割：(.+)$")

    def to_pivot(self, data, row_number, handicap):
        data[f'{row_number}'] = {
            "type": "handicap",
            "handicap": handicap,
        }

    def from_pivot(self, handicap):
        return f"手合割：{handicap}\n"

    def match(self, line):
        return self._handicap_statement.match(line)


handicap_statement_p = HandicapStatementP()


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
            "comment": comment
        }

    def from_pivot(self, moves_header, comment):
        return f"{moves_header}#{comment}\n"


moves_header_statement_p = MovesHeaderStatementP()


class VariationLabelStatementP():
    """変化手順（棋譜の分岐）のジャンプ先ラベル パーサー"""

    def __init__(self):
        self._variation_label_statement = re.compile(r"^変化：(\d+)手$")

    def match(self, line):
        return self._variation_label_statement.match(line)

    def to_pivot(self, data, row_number, moves):
        data[f'{row_number}'] = {
            "type": "variationLabel",
            "moves": f"{moves}",
        }

    def from_pivot(self, moves):
        return f"変化：{moves}手\n"


variation_label_statement_p = VariationLabelStatementP()


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
            r"^\s*(\d+)\s+([^ ]+)\s*\(\s*([0-9:]+)\s*/\s*([0-9:]+)\s*\)(.*)$")

    def match(self, line):
        return self._move_statement.match(line)

    def from_pivot(self, moves, elapsedTime, totalElapsedTime, move):
        kifu_text = ""

        elapsedTimeMinute = elapsedTime["minute"]
        elapsedTimeSecond = elapsedTime["second"]

        totalElapsedTimeHour = totalElapsedTime["hour"]
        totalElapsedTimeMinute = totalElapsedTime["minute"]
        totalElapsedTimeSecond = totalElapsedTime["second"]

        move_text = ""
        # 半角スペース幅
        spaces = 14

        if "sign" in move:
            sign = move["sign"]
            move_text += f"{sign}"
            spaces -= sign_p.half_width(sign)

        if "destinationFile" in move:
            destination_file = move["destinationFile"]
            destination_rank = move["destinationRank"]
            move_text += f"{destination_file}{destination_rank}"
            spaces -= 4

        if "destination" in move:
            destination = move["destination"]
            if destination == 'Same':
                move_text += "同　"
                spaces -= 4
            else:
                move_text += f"{destination}"
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

        if "sourceFile" in move:
            sourceFile = move["sourceFile"]
            sourceRank = move["sourceRank"]
            move_text += f"({sourceFile}{sourceRank})"
            spaces -= 4

        # 左にスペースを詰めます
        move_text += ''.ljust(spaces, ' ')

        kifu_text += f"{moves:>4} {move_text}({elapsedTimeMinute:02}:{elapsedTimeSecond:02} / {totalElapsedTimeHour:02}:{totalElapsedTimeMinute:02}:{totalElapsedTimeSecond:02})\n"

        return kifu_text


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
        self._sign = ['中断', '投了', '持将棋', '千日手', '詰み', '切れ負け', '反則勝ち', '反則負け', '入玉勝ち', '不戦勝', '不戦敗', # KIFの仕様にあるもの
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


class ElapsedTimeP():
    def __init__(self):
        # ↓ どっちもある
        # Example: `0:01`
        # Example: `00:01`
        self._elapsed_time = re.compile(r"^(\d+):(\d+)$")

    def match(self, line):
        return self._elapsed_time.match(line)

    def to_pivot(self, data, row_number, minute, second):
        data[f'{row_number}']["elapsedTime"] = {}
        data[f'{row_number}']["elapsedTime"]["minute"] = minute
        data[f'{row_number}']["elapsedTime"]["second"] = second


elapsed_time_p = ElapsedTimeP()


class TotalElapsedTimeP():
    def __init__(self):
        # Example: `00:00:16`
        self._total_elapsed_time = re.compile(r"^(\d+):(\d+):(\d+)$")

    def match(self, line):
        return self._total_elapsed_time.match(line)

    def to_pivot(self, data, row_number, hour, minute, second):
        data[f'{row_number}']["totalElapsedTime"] = {}
        data[f'{row_number}']["totalElapsedTime"]["hour"] = hour
        data[f'{row_number}']["totalElapsedTime"]["minute"] = minute
        data[f'{row_number}']["totalElapsedTime"]["second"] = second


total_elapsed_time_p = TotalElapsedTimeP()


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
