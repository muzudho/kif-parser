__player_phase = {
    '先手':'FirstPlayer',
    '後手':'SecondPlayer',
    '下手':'Trainee',
    '上手':'Trainer',
}

def player_phase_to_en(playerPhase):
    if playerPhase in __player_phase:
        return __player_phase[playerPhase]

    return playerPhase

__handicap = {
    '平手':'Hirate',
    '香落ち':'LostLance',
    '右香落ち':'LostRightLance',
    '角落ち':'LostBishop',
    '飛車落ち':'LostRook',
    '飛香落ち':'LostRookLance',
    '二枚落ち':'Lost2Pieces',
    '三枚落ち':'Lost3Pieces',
    '四枚落ち':'Lost4Pieces',
    '五枚落ち':'Lost5Pieces',
    '左五枚落ち':'LostLeft5Pieces',
    '六枚落ち':'Lost6Pieces',
    '左七枚落ち':'LostLeft7Pieces',
    '右七枚落ち':'LostRight7Pieces',
    '八枚落ち':'Lost8Pieces',
    '十枚落ち':'Lost10Pieces',
    'その他':'Other',
}

def handicap_to_en(handicap):
    if handicap in __handicap:
        return __handicap[handicap]

    return handicap

__pieceType = {
    '玉':'King',
    '飛':'Rook',
    '龍':'Dragon',
    '竜':'Dragon',
    '角':'Bishop',
    '馬':'Horse',
    '金':'Gold',
    '銀':'Silver',
    '成銀':'PromotionSilver',
    '全':'PromotionSilver',
    '桂':'Knight',
    '成桂':'PromotionKnight',
    '圭':'PromotionKnight',
    '香':'Lance',
    '成香':'PromotionLance',
    '杏':'PromotionLance',
    '歩':'Pawn',
    'と':'PromotionPawn',
}

def piece_type_to_en(pieceType):
    if pieceType in __pieceType:
        return __pieceType[pieceType]

    return pieceType
