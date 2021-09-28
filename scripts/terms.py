def player_phase_to_en(playerPhase):
    if playerPhase=='先手':
        return 'FirstPlayer'
    elif playerPhase=='|後手':
        return 'SecondPlayer'
    elif playerPhase=='|下手':
        return 'Trainee'
    elif playerPhase=='|上手':
        return 'Trainer'
    return playerPhase

def handicap_to_en(handicap):
    if handicap == '平手':
        return "Hirate"
    elif handicap == '香落ち':
        return "LostLance"
    elif handicap == '右香落ち':
        return "LostRightLance"
    elif handicap == '角落ち':
        return "LostBishop"
    elif handicap == '飛車落ち':
        return "LostRook"
    elif handicap == '飛香落ち':
        return "LostRookLance"
    elif handicap == '二枚落ち':
        return "Lost2Pieces"
    elif handicap == '三枚落ち':
        return "Lost3Pieces"
    elif handicap == '四枚落ち':
        return "Lost4Pieces"
    elif handicap == '五枚落ち':
        return "Lost5Pieces"
    elif handicap == '左五枚落ち':
        return "LostLeft5Pieces"
    elif handicap == '六枚落ち':
        return "Lost6Pieces"
    elif handicap == '左七枚落ち':
        return "LostLeft7Pieces"
    elif handicap == '右七枚落ち':
        return "LostRight7Pieces"
    elif handicap == '八枚落ち':
        return "Lost8Pieces"
    elif handicap == '十枚落ち':
        return "Lost10Pieces"
    elif handicap == 'その他':
        return "Other"

    return handicap
