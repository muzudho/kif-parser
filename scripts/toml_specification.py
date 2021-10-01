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


class PlayerStatementP():
    def __init__(self):
        self._player_name_statement = re.compile(
            r"^(" + player_phase_p.choices() + r")：(.+)$")

    def match(self, line):
        return self._player_name_statement.match(line)


player_statement_p = PlayerStatementP()


class HandicapP():
    def __init__(self):
        # 逆引き対応
        self._handicap = {
            'even': 'Hirate',
            'without left lance': 'LostLance',  # 香落ち（左の香が落ちる）
            'without right lance': 'LostRightLance',  # 右香落ち
            'without the bishop': 'LostBishop',  # 角落ち
            'without the rook': 'LostRook',  # 飛車落ち
            'without a rook, left lance': 'LostRookLance',  # 飛香落ち（飛車と左の香）
            'without a rook, a bishop': 'Lost2Pieces',  # ２枚落ち
            'without a rook, a bishop, left lance': 'Lost3Pieces',  # ３枚落ち（飛、角、左香）
            'without a rook, a bishop, 2 lances': 'Lost4Pieces',  # ４枚落ち（飛、角、両香）
            'without a rook, a bishop, left knight, 2 lances': 'Lost5Pieces',  # ５枚落ち（飛、角、左桂、両香）
            'without left 5 pieces': 'LostLeft5Pieces',  # 左５枚落ち
            'without a hisha, a kaku, 2 kyoushas, 2 keimas': 'Lost6Pieces',  # ６枚落ち
            'without left 7 pieces': 'LostLeft7Pieces',  # 左七枚落ち
            'without right 7 pieces': 'LostRight7Pieces',  # 右七枚落ち
            # ８枚落ち（飛、角、両銀、両桂、両香）
            'without a rook, a bishop, 2 silvers, 2 knights, 2 lances': 'Lost8Pieces',
            # １０枚落ち（飛、角、両金、両銀、両桂、両香）
            'without a rook, a bishop, 2 golds, 2 silvers, 2knight, 2 lances': 'Lost10Pieces',
            'other': 'Other',
        }

        self._handicap_statement = re.compile(r"^手合割：(.+)$")

    def to_pivot(self, handicap):
        if handicap in self._handicap:
            return self._handicap[handicap]

        return handicap

    def from_pivot(self, handicap):
        items = [k for k, v in self._handicap.items() if v == handicap]
        return items[0]

    def match(self, line):
        return self._handicap_statement.match(line)


handicap_p = HandicapP()


class MoveStatementP():
    def __init__(self):
        # Example: `   1 ７六歩(77)    (00:01 / 00:00:01)`
        # Example: `  22 同　角(88)    (00:01 / 00:00:11)`
        self._move_statement = re.compile(
            r"^\s*(\d+)\s+([^ ]+)\s+\(([0-9:]+) / ([0-9:]+)\)(.*)$")

    def match(self, line):
        return self._move_statement.match(line)

    def from_pivot(self, moves, elapsedTime, totalElapsedTime, move):
        toml_text = ''

        elapsedTimeHour = 0
        elapsedTimeMinute = elapsedTime["minute"]
        if 60 < elapsedTimeMinute:
            elapsedTimeHour = elapsedTimeMinute // 60
            elapsedTimeMinute = elapsedTimeMinute % 60
        elapsedTimeSecond = elapsedTime["second"]

        totalElapsedTimeHour = totalElapsedTime["hour"]
        totalElapsedTimeMinute = totalElapsedTime["minute"]
        totalElapsedTimeSecond = totalElapsedTime["second"]

        key_value_pairs = []

        # 移動した駒
        if "pieceType" in move:
            piece_type = piece_type_p.from_pivot(move["pieceType"])
            key_value_pairs.append(f"piece-type='{piece_type}'")

        # TODO 「x」pivotに駒を取ったという情報が欲しい

        if "sourceFile" in move:
            # 移動元（打のときは、 SourceFile, SourceRank ともにありません）
            source_square = int(move["sourceFile"]) * \
                10 + int(move["sourceRank"])
            key_value_pairs.append(f"from = {source_square}")
        elif "drop" in move:
            # 打
            drop = move["drop"]
            if drop:
                key_value_pairs.append(f"drop = true")

        # 行き先
        if "destinationFile" in move:
            destination_square = int(
                move["destinationFile"]) * 10 + int(move["destinationRank"])
            key_value_pairs.append(
                f"to = {destination_square}")

        elif "destination" in move:
            destination = move["destination"]
            if destination == 'Same':
                # TODO チェスに「同」は無さそう？
                key_value_pairs.append(f"to-same = true")
            else:
                # Error
                raise error(f'unknown destination={destination}')

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
            f"""elapsed = {elapsedTimeHour:02}:{elapsedTimeMinute:02}:{elapsedTimeSecond:02}""")

        key_value_pairs.append(
            f"""sum = {totalElapsedTimeHour:02}:{totalElapsedTimeMinute:02}:{totalElapsedTimeSecond:02}""")

        table_items = ', '.join(key_value_pairs)

        # 指し手
        toml_text += f"""{moves} = {{ {table_items} }}
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
            'K': 'King',
            'R': 'Rook',
            '+R': 'Dragon',
            'B': 'Bishop',
            '+B': 'Horse',
            'G': 'Gold',
            'S': 'Silver',
            '+S': 'PromotionSilver',
            'N': 'Knight',
            '+N': 'PromotionKnight',
            'L': 'Lance',
            '+L': 'PromotionLance',
            'P': 'Pawn',
            '+P': 'PromotionPawn',
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


class ElapsedTimeP():
    def __init__(self):
        # Example: `00:01`
        self._elapsed_time = re.compile(r"^(\d+):(\d+)$")

    def match(self, line):
        return self._elapsed_time.match(line)


class TotalElapsedTimeP():
    def __init__(self):
        # Example: `00:00:16`
        self._total_elapsed_time = re.compile(r"^(\d+):(\d+):(\d+)$")

    def match(self, line):
        return self._total_elapsed_time.match(line)


class JudgeStatement1P():
    def __init__(self):
        # Example: `まで64手で後手の勝ち`
        self._judge_statement1 = re.compile(
            r"^まで(\d+)手で(先手|後手|下手|上手)の(反則負け|勝ち)$")

    def match(self, line):
        return self._judge_statement1.match(line)

    def from_pivot(self, moves, winner, judge):
        # Example: `まで64手で後手の勝ち`
        return f"""[result]
last-moves={moves}
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

    def from_pivot(self, moves, judge):
        # Example: `まで63手で中断`
        return f"""[result]
last-moves={moves}
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

    def from_pivot(self, moves, reason, winner, judge):
        # Example: `まで52手で時間切れにより後手の勝ち`
        return f"""[result]
last-moves={moves}
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
