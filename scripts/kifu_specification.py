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

    def to_pibot(self, handicap):
        if handicap in self._handicap:
            return self._handicap[handicap]

        return handicap

    def from_pibot(self, handicap):
        items = [k for k, v in self._handicap.items() if v == handicap]
        return items[0]


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
            '切れ負け': 'TimeUp',
            '反則勝ち': 'IllegalWin',
            '反則負け': 'IllegalLose',
            '入玉勝ち': 'EnteringKingWin',
            '不戦勝': 'UnearnedWin',
            '不戦敗': 'UnearnedLose',
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


class JudgeP():
    def __init__(self):
        # 逆引き対応
        self._judge = {
            '中断': 'Stop',
            '反則負け': 'IllegalLose',
            '勝ち': 'Win',
        }

    def to_pibot(self, judge):
        if judge in self._judge:
            return self._judge[judge]

        return judge

    def from_pibot(self, judge):
        items = [k for k, v in self._judge.items() if v == judge]
        return items[0]
