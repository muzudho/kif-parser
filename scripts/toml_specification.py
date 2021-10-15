from os import error
import re


class CommentP():
    def __init__(self):
        self._comment_statement = re.compile(r"^#(.+)$")

    def match(self, line):
        return self._comment_statement.match(line)


class ExplanationP():
    def __init__(self):
        self._explanation_statement = re.compile(r"^\*(.+)$")

    def match(self, line):
        return self._explanation_statement.match(line)


explanation_p = ExplanationP()


class PlayerPhaseP():
    def __init__(self):
        # 逆引き対応
        # このディクショナリーのキーは、 JSON のキーにもなる
        self._player_phase = {
            'first-player': 'FirstPlayer',
            'second-player': 'SecondPlayer',
            'trainee': 'Trainee',
            'trainer': 'Trainer',
        }

    def to_pivot(self, player_phase):
        if player_phase in self._player_phase:
            return self._player_phase[player_phase]

        return player_phase

    def from_pivot(self, player_phase):
        items = [k for k, v in self._player_phase.items() if v == player_phase]
        return items[0]

    def choices(self):
        items = [k for k, v in self._player_phase.items()]
        return "|".join(items)


player_phase_p = PlayerPhaseP()


class KeyValuePairStatementP():
    """TODO 対局情報は　`ユーザが任意のものを追加できる`　と `棋譜ファイル KIF 形式` にある"""

    def __init__(self):
        pass

    def from_pivot(self, rowNumber, key, value, comment):
        if comment:
            return f"kvPair-{rowNumber} = {{ key = '''{key}''', value = '''{value}''', comment = '''{comment}''' }}\n"

        return f"kvPair-{rowNumber} = {{ key = '''{key}''', value = '''{value}''' }}\n"


key_value_pair_statement_p = KeyValuePairStatementP()


class MoveStatementP():
    def __init__(self):
        # Example: `   1 ７六歩(77)    (00:01 / 00:00:01)`
        # Example: `  22 同　角(88)    (00:01 / 00:00:11)`
        self._move_statement = re.compile(
            r"^\s*(\d+)\s+([^ ]+)\s+\(([0-9:]+) / ([0-9:]+)\)(.*)$")

    def match(self, line):
        return self._move_statement.match(line)

    def from_pivot(self, moveNum, time, total, move):
        """
        Parameters
        ----------
        time : int
            Expended time（消費時間）
        total : int
            Total expended time（消費時間合計）
        """
        toml_text = ''

        timeHr = 0
        timeMin = time["min"]
        if 60 < timeMin:
            timeHr = timeMin // 60
            timeMin = timeMin % 60
        timeSec = time["sec"]

        totalHr = total["hr"]
        totalMin = total["min"]
        totalSec = total["sec"]

        key_value_pairs = []

        # 移動した駒
        if "pieceType" in move:
            piece_type = piece_type_p.from_pivot(move["pieceType"])
            key_value_pairs.append(f"piece-type='{piece_type}'")

        # TODO 「x」pivotに駒を取ったという情報が欲しい

        if "srcFile" in move:
            # 移動元（打のときは、 SourceFile, SourceRank ともにありません）
            src_square = int(move["srcFile"]) * \
                10 + int(move["srcRank"])
            key_value_pairs.append(f"from = {src_square}")
        elif "drop" in move:
            # 打
            drop = move["drop"]
            if drop:
                key_value_pairs.append(f"drop = true")

        # 行き先
        if "dstFile" in move:
            dst_square = int(
                move["dstFile"]) * 10 + int(move["dstRank"])
            key_value_pairs.append(
                f"to = {dst_square}")

        elif "dst" in move:
            dst = move["dst"]
            if dst == 'Same':
                # TODO チェスに「同」は無さそう？
                key_value_pairs.append(f"to-same = true")
            else:
                # Error
                raise error(f'unknown dst={dst}')

        # 成り
        if "promotion" in move:
            pro = move["promotion"]
            if pro:
                key_value_pairs.append(f"promotion = true")

        # 投了なども行き先欄に書く
        if "sign" in move:
            sign = sign_p.from_pivot(move["sign"])
            key_value_pairs.append(f"sign = '{sign}'")

        # 経過時間
        key_value_pairs.append(
            f"""expended = {timeHr:02}:{timeMin:02}:{timeSec:02}""")

        key_value_pairs.append(
            f"""sum = {totalHr:02}:{totalMin:02}:{totalSec:02}""")

        table_items = ', '.join(key_value_pairs)

        # 指し手
        toml_text += f"""{moveNum} = {{ {table_items} }}
"""

        return toml_text


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


class PieceTypeP():
    """先後を区別しない駒の種類"""

    def __init__(self):
        # 逆引き対応（複数あるものは先にくるものが選ばれるものとします）
        # SFEN を参考にします
        self._piece_type = {
            'K': "king",
            'R': "rook",
            '+R': "dragon",
            'B': "bishop",
            '+B': "horse",
            'G': "gold",
            'S': "silver",
            '+S': "promotionSilver",
            'N': "knight",
            '+N': "promotionKnight",
            'L': "lance",
            '+L': "promotionLance",
            'P': "pawn",
            '+P': "promotionPawn",
        }

    def to_pivot(self, piece_type):
        if piece_type in self._piece_type:
            return self._piece_type[piece_type]

        return piece_type

    def from_pivot(self, piece_type):
        items = [k for k, v in self._piece_type.items() if v == piece_type]
        return items[0]


piece_type_p = PieceTypeP()


class SignP():
    def __init__(self):
        # 逆引き対応
        self._sign = {
            'stop': 'Stop',
            'resign': 'Resign',
            'ji-shogi': 'JiShogi',
            'repeatation': 'Repeatation',
            'checkmate': 'Checkmate',
            'time-up-lose': 'TimeUpLose',
            'illegal-win': 'IllegalWin',
            'illegal-lose': 'IllegalLose',
            'entering-king-win': 'EnteringKingWin',
            'unearned-win': 'UnearnedWin',
            'unearned-lose': 'UnearnedLose',
            'win': 'Win',  # 追加
        }

    def contains(self, key):
        return key in self._sign.keys()

    def to_pivot(self, sign):
        if sign in self._sign:
            return self._sign[sign]

        return sign

    def from_pivot(self, sign):
        items = [k for k, v in self._sign.items() if v == sign]
        return items[0]


sign_p = SignP()


class ExpendedTimeP():
    def __init__(self):
        # Example: `00:01`
        self._expended_time = re.compile(r"^(\d+):(\d+)$")

    def match(self, line):
        return self._expended_time.match(line)


class TotalExpendedTimeP():
    def __init__(self):
        # Example: `00:00:16`
        self._total_expended_time = re.compile(r"^(\d+):(\d+):(\d+)$")

    def match(self, line):
        return self._total_expended_time.match(line)


class JudgeStatement1P():
    def __init__(self):
        # Example: `まで64手で後手の勝ち`
        self._judge_statement1 = re.compile(
            r"^まで(\d+)手で(先手|後手|下手|上手)の(反則負け|勝ち)$")

    def match(self, line):
        return self._judge_statement1.match(line)

    def from_pivot(self, moveNum, winner, judge):
        # Example: `まで64手で後手の勝ち`
        return f"""last-move-num={moveNum}
winner='{player_phase_p.from_pivot(winner)}'
judge='{sign_p.from_pivot(judge)}'
"""


judge_statement1_p = JudgeStatement1P()


class JudgeStatement2P():
    def __init__(self):
        # Example: `まで63手で中断`
        self._judge_statement2 = re.compile(r"^まで(\d+)手で(中断|持将棋|千日手)$")

    def match(self, line):
        return self._judge_statement2.match(line)

    def from_pivot(self, moveNum, judge):
        # Example: `まで63手で中断`
        return f"""last-move-num={moveNum}
judge='{sign_p.from_pivot(judge)}'
"""


judge_statement2_p = JudgeStatement2P()


class JudgeStatement3P():
    def __init__(self):
        # Example: `まで52手で時間切れにより後手の勝ち`
        self._judge_statement3 = re.compile(
            r"^まで(\d+)手で(時間切れ)により(先手|後手|下手|上手)の(勝ち)$")

    def match(self, line):
        return self._judge_statement3.match(line)

    def from_pivot(self, moveNum, reason, winner, judge):
        # Example: `まで52手で時間切れにより後手の勝ち`
        return f"""last-move-num={moveNum}
reason='{reason_p.from_pivot(reason)}'
winner='{player_phase_p.from_pivot(winner)}'
judge='{sign_p.from_pivot(judge)}'
"""


judge_statement3_p = JudgeStatement3P()


class ReasonP():
    def __init__(self):
        # 逆引き対応
        self._reason = {
            'time-up': 'TimeUp',
        }

    def to_pivot(self, reason):
        if reason in self._reason:
            return self._reason[reason]

        return reason

    def from_pivot(self, reason):
        items = [k for k, v in self._reason.items() if v == reason]
        return items[0]


reason_p = ReasonP()


"""
class ZenkakuNumberP():
    def __init__(self):
        # 逆引き対応
        self._zenkaku_number = {
            '１': 1,
            '２': 2,
            '３': 3,
            '４': 4,
            '５': 5,
            '６': 6,
            '７': 7,
            '８': 8,
            '９': 9,
        }

    def to_pivot(self, zenkaku_number):
        if zenkaku_number in self._zenkaku_number:
            return self._zenkaku_number[zenkaku_number]

        return zenkaku_number

    def from_pivot(self, zenkaku_number):
        items = [k for k, v in self._zenkaku_number.items() if v ==
                 zenkaku_number]
        return items[0]


zenkaku_number_p = ZenkakuNumberP()
"""


"""
class KanjiNumberP():
    def __init__(self):
        # 逆引き対応
        self._kanji_number = {
            '一': 1,
            '二': 2,
            '三': 3,
            '四': 4,
            '五': 5,
            '六': 6,
            '七': 7,
            '八': 8,
            '九': 9,
        }

    def to_pivot(self, kanji_number):
        if kanji_number in self._kanji_number:
            return self._kanji_number[kanji_number]

        return kanji_number

    def from_pivot(self, kanji_number):
        items = [k for k, v in self._kanji_number.items() if v == kanji_number]
        return items[0]


kanji_number_p = KanjiNumberP()
"""


class AlphabetNumberP():
    def __init__(self):
        # 逆引き対応
        self._alphabet_number = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 7,
            'h': 8,
            'i': 9,
        }

    def to_pivot(self, alphabet):
        if alphabet in self._alphabet_number:
            return self._alphabet_number[alphabet]

        return alphabet

    def from_pivot(self, number):
        items = [k for k, v in self._alphabet_number.items() if v == number]
        return items[0]


alphabet_number_p = AlphabetNumberP()
