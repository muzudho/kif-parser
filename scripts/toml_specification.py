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
            'hirate': 'Hirate',
            'lost-lance': 'LostLance',
            'lost-right-lance': 'LostRightLance',
            'lost-bishop': 'LostBishop',
            'lost-rook': 'LostRook',
            'lost-rook-lance': 'LostRookLance',
            'lost-2-pieces': 'Lost2Pieces',
            'lost-3-pieces': 'Lost3Pieces',
            'lost-4-pieces': 'Lost4Pieces',
            'lost-5-pieces': 'Lost5Pieces',
            'lost-left-5-pieces': 'LostLeft5Pieces',
            'lost-6-pieces': 'Lost6Pieces',
            'lost-left-7-pieces': 'LostLeft7Pieces',
            'lost-right-7-pieces': 'LostRight7Pieces',
            'lost-8-pieces': 'Lost8Pieces',
            'lost-10-pieces': 'Lost10Pieces',
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
        elapsedTimeMinute = elapsedTime['Minute']
        if 60 < elapsedTimeMinute:
            elapsedTimeHour = elapsedTimeMinute // 60
            elapsedTimeMinute = elapsedTimeMinute % 60
        elapsedTimeSecond = elapsedTime['Second']

        totalElapsedTimeHour = totalElapsedTime['Hour']
        totalElapsedTimeMinute = totalElapsedTime['Minute']
        totalElapsedTimeSecond = totalElapsedTime['Second']

        move_to_text = ""

        # 移動した駒（チェスでは歩は省く）
        if 'PieceType' in move:
            pieceType = piece_type_p.from_pivot(move['PieceType'])
            if pieceType != 'P':
                move_to_text += pieceType

        # TODO 「x」pivotに駒を取ったという情報が欲しい

        # 行き先
        if 'DestinationFile' in move:
            destinationFile = move['DestinationFile']
            destinationRank = alphabet_number_p.from_pivot(
                move['DestinationRank'])
            move_to_text += f'{destinationFile}{destinationRank}'

        if 'Destination' in move:
            destination = move['Destination']
            if destination == 'same':
                # TODO チェスに「同」は無さそう？
                move_to_text += 'same'
            else:
                # TODO エラーにしたい
                move_to_text += destination

        # 成り
        if 'Promotion' in move:
            pro = move['Promotion']
            if pro:
                move_to_text += '+'

        # 投了なども行き先欄に書く
        if 'Sign' in move:
            sign = sign_p.from_pivot(move['Sign'])
            move_to_text += f"{sign}"

        move_from_text = ""

        # 移動元
        if 'SourceFile' in move:
            sourceFile = move['SourceFile']
            sourceRank = alphabet_number_p.from_pivot(move['SourceRank'])
            move_from_text += f'{sourceFile}{sourceRank}'

        # 打
        if 'Drop' in move:
            drop = move['Drop']
            if drop:
                move_from_text += 'drop'

        if move_from_text != '':
            move_from_text = f""", from = '{move_from_text}'"""
            pass

        move_text = f"""to = '{move_to_text}'{move_from_text}"""

        # 経過時間
        elapsed_text = f"""elapsed = {elapsedTimeHour:02}:{elapsedTimeMinute:02}:{elapsedTimeSecond:02}, sum = {totalElapsedTimeHour:02}:{totalElapsedTimeMinute:02}:{totalElapsedTimeSecond:02}"""

        # 指し手
        toml_text += f"""{moves} = {{ {move_text}, {elapsed_text} }}
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
last-moves='{moves}'
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
last-moves='{moves}'
judge='{sign_p.from_pivot(judge)}'
"""


judge_statement2_p = JudgeStatement2P()


class JudgeStatement3P():
    def __init__(self):
        # Example: `まで52手で時間切れにより後手の勝ち`
        self._judge_statement2 = re.compile(
            r"^まで(\d+)手で(時間切れ)により(先手|後手|下手|上手)の(勝ち)$")

    def match(self, line):
        return self._judge_statement2.match(line)

    def from_pivot(self, moves, reason, winner, judge):
        # Example: `まで52手で時間切れにより後手の勝ち`
        return f"""[result]
last-moves='{moves}'
reason='{reason}'
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
