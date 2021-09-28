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