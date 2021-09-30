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
            '先手': 'FirstPlayer',
            '後手': 'SecondPlayer',
            '下手': 'Trainee',
            '上手': 'Trainer',
        }

    def to_pibot(self, player_phase):
        if player_phase in self._player_phase:
            return self._player_phase[player_phase]

        return player_phase

    def from_pibot(self, player_phase):
        items = [k for k, v in self._player_phase.items() if v == player_phase]
        return items[0]


player_phase_p = PlayerPhaseP()


class PlayerNameP():
    def __init__(self):
        self._player_name_statement = re.compile(r"^(先手|後手|下手|上手)：(.+)$")

    def match(self, line):
        return self._player_name_statement.match(line)


class HandicapP():
    def __init__(self):
        # 逆引き対応
        self._handicap = {
            '平手': 'Hirate',
            '香落ち': 'LostLance',
            '右香落ち': 'LostRightLance',
            '角落ち': 'LostBishop',
            '飛車落ち': 'LostRook',
            '飛香落ち': 'LostRookLance',
            '二枚落ち': 'Lost2Pieces',
            '三枚落ち': 'Lost3Pieces',
            '四枚落ち': 'Lost4Pieces',
            '五枚落ち': 'Lost5Pieces',
            '左五枚落ち': 'LostLeft5Pieces',
            '六枚落ち': 'Lost6Pieces',
            '左七枚落ち': 'LostLeft7Pieces',
            '右七枚落ち': 'LostRight7Pieces',
            '八枚落ち': 'Lost8Pieces',
            '十枚落ち': 'Lost10Pieces',
            'その他': 'Other',
        }

        self._handicap_statement = re.compile(r"^手合割：(.+)$")

    def to_pibot(self, handicap):
        if handicap in self._handicap:
            return self._handicap[handicap]

        return handicap

    def from_pibot(self, handicap):
        items = [k for k, v in self._handicap.items() if v == handicap]
        return items[0]

    def match(self, line):
        return self._handicap_statement.match(line)


class MoveStatementP():
    def __init__(self):
        # Example: `   1 ７六歩(77)    (00:01 / 00:00:01)`
        # Example: `  22 同　角(88)    (00:01 / 00:00:11)`
        self._move_statement = re.compile(
            r"^\s*(\d+)\s+([^ ]+)\s+\(([0-9:]+) / ([0-9:]+)\)(.*)$")

    def match(self, line):
        return self._move_statement.match(line)


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
    def __init__(self):
        # 逆引き対応（複数あるものは先にくるものが選ばれるものとします）
        self._piece_type = {
            '玉': 'King',
            '飛': 'Rook',
            '龍': 'Dragon',
            '竜': 'Dragon',
            '角': 'Bishop',
            '馬': 'Horse',
            '金': 'Gold',
            '銀': 'Silver',
            '成銀': 'PromotionSilver',
            '全': 'PromotionSilver',
            '桂': 'Knight',
            '成桂': 'PromotionKnight',
            '圭': 'PromotionKnight',
            '香': 'Lance',
            '成香': 'PromotionLance',
            '杏': 'PromotionLance',
            '歩': 'Pawn',
            'と': 'PromotionPawn',
        }

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

    def to_pibot(self, piece_type):
        if piece_type in self._piece_type:
            return self._piece_type[piece_type]

        return piece_type

    def from_pibot(self, piece_type):
        items = [k for k, v in self._piece_type.items() if v == piece_type]
        return items[0]

    def half_width(self, piece_type):
        if piece_type in self._piece_type_half_width.keys():
            return self._piece_type_half_width[piece_type]

        return piece_type


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

    def to_pibot(self, zenkaku_number):
        if zenkaku_number in self._zenkaku_number:
            return self._zenkaku_number[zenkaku_number]

        return zenkaku_number

    def from_pibot(self, zenkaku_number):
        items = [k for k, v in self._zenkaku_number.items() if v ==
                 zenkaku_number]
        return items[0]


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

    def to_pibot(self, kanji_number):
        if kanji_number in self._kanji_number:
            return self._kanji_number[kanji_number]

        return kanji_number

    def from_pibot(self, kanji_number):
        items = [k for k, v in self._kanji_number.items() if v == kanji_number]
        return items[0]


class SignP():
    def __init__(self):
        # 逆引き対応
        self._sign = {
            '中断': 'Stop',
            '投了': 'Resign',
            '持将棋': 'JiShogi',
            '千日手': 'Repeatation',
            '詰み': 'Checkmate',
            '切れ負け': 'TimeUpLose',
            '反則勝ち': 'IllegalWin',
            '反則負け': 'IllegalLose',
            '入玉勝ち': 'EnteringKingWin',
            '不戦勝': 'UnearnedWin',
            '不戦敗': 'UnearnedLose',
            '勝ち': 'Win',  # 追加
        }

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
        return key in self._sign.keys()

    def to_pibot(self, sign):
        if sign in self._sign:
            return self._sign[sign]

        return sign

    def from_pibot(self, sign):
        items = [k for k, v in self._sign.items() if v == sign]
        return items[0]

    def half_width(self, sign):
        if sign in self._sign_half_width.keys():
            return self._sign_half_width[sign]

        return sign


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

    def from_pibot(self, moves, winner, judge):
        # Example: `まで64手で後手の勝ち`
        return f"まで{moves}手で{player_phase_p.from_pibot(winner)}の{sign_p.from_pibot(judge)}\n"


class JudgeStatement2P():
    def __init__(self):
        # Example: `まで63手で中断`
        self._judge_statement2 = re.compile(r"^まで(\d+)手で(中断|持将棋)$")

    def match(self, line):
        return self._judge_statement2.match(line)

    def from_pibot(self, moves, judge):
        # Example: `まで63手で中断`
        return f"まで{moves}手で{sign_p.from_pibot(judge)}\n"


class JudgeStatement3P():
    def __init__(self):
        # Example: `まで52手で時間切れにより後手の勝ち`
        self._judge_statement2 = re.compile(
            r"^まで(\d+)手で(時間切れ)により(先手|後手|下手|上手)の(勝ち)$")

    def match(self, line):
        return self._judge_statement2.match(line)

    def from_pibot(self, moves, reason, winner, judge):
        # Example: `まで52手で時間切れにより後手の勝ち`
        return f"まで{moves}手で{reason}により{player_phase_p.from_pibot(winner)}の{sign_p.from_pibot(judge)}\n"


class ReasonP():
    def __init__(self):
        # 逆引き対応
        self._reason = {
            '時間切れ': 'TimeUp',
        }

    def to_pibot(self, reason):
        if reason in self._reason:
            return self._reason[reason]

        return reason

    def from_pibot(self, reason):
        items = [k for k, v in self._reason.items() if v == reason]
        return items[0]
