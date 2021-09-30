class PlayerPhaseP():
    def __init__(self):
        # 逆引き対応
        self._player_phase = {
            '先手': 'FirstPlayer',
            '後手': 'SecondPlayer',
            '下手': 'Trainee',
            '上手': 'Trainer',
        }

    def to_en(self, playerPhase):
        if playerPhase in self._player_phase:
            return self._player_phase[playerPhase]

        return playerPhase

    def from_en(self, en):
        items = [k for k, v in self._player_phase.items() if v == en]
        return items[0]


# 逆引き対応
__handicap = {
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


def handicap_to_en(handicap):
    if handicap in __handicap:
        return __handicap[handicap]

    return handicap


def en_to_handicap(en):
    items = [k for k, v in __handicap.items() if v == en]
    return items[0]


# 逆引き対応（複数あるものは先にくるものが選ばれるものとします）
__piece_type = {
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
__piece_type_half_width = {
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


def piece_type_to_en(pieceType):
    if pieceType in __piece_type:
        return __piece_type[pieceType]

    return pieceType


def en_to_piece_type(en):
    items = [k for k, v in __piece_type.items() if v == en]
    return items[0]


def piece_type_half_width(piece_type):
    if piece_type in __piece_type_half_width.keys():
        return __piece_type_half_width[piece_type]

    return piece_type


# 逆引き対応
__zenkaku_number = {
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


def zenkaku_to_number(zenkaku):
    if zenkaku in __zenkaku_number:
        return __zenkaku_number[zenkaku]

    return zenkaku


def number_to_zenkaku(en):
    items = [k for k, v in __zenkaku_number.items() if v == en]
    return items[0]


# 逆引き対応
__kanji_number = {
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


def kanji_to_number(kanji):
    if kanji in __kanji_number:
        return __kanji_number[kanji]

    return kanji


def number_to_kanji(en):
    items = [k for k, v in __kanji_number.items() if v == en]
    return items[0]


# 逆引き対応
__sign = {
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
__sign_half_width = {
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


def contains_sign(key):
    return key in __sign.keys()


def sign_to_en(sign):
    if sign in __sign:
        return __sign[sign]

    return sign


def en_to_sign(en):
    items = [k for k, v in __sign.items() if v == en]
    return items[0]


def sign_half_width(sign):
    if sign in __sign_half_width.keys():
        return __sign_half_width[sign]

    return sign


# 逆引き対応
__judge = {
    '中断': 'Stop',
    '反則負け': 'IllegalLose',
    '勝ち': 'Win',
}


def judge_to_en(judge):
    if judge in __judge:
        return __judge[judge]

    return judge


def en_to_judge(en):
    items = [k for k, v in __judge.items() if v == en]
    return items[0]
