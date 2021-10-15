# 開始日時パーサー

難しいので一旦廃止  

```plain
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
```

```plain
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
```

```plain
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
```

```plain
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
```

```plain
class HandicapStatementP():
    def __init__(self):
        # 逆引き対応
        self._handicap = {
            'even': 'even',
            'without left lance': 'withoutLeftLance',  # 香落ち（左の香が落ちる）
            'without right lance': 'withoutRightLance',  # 右香落ち
            'without the bishop': 'withoutBishop',  # 角落ち
            'without the rook': 'withoutRook',  # 飛車落ち
            'without a rook, left lance': 'withoutRookLance',  # 飛香落ち（飛車と左の香）
            'without a rook, a bishop': 'without2Pieces',  # ２枚落ち
            'without a rook, a bishop, left lance': 'without3Pieces',  # ３枚落ち（飛、角、左香）
            'without a rook, a bishop, 2 lances': 'without4Pieces',  # ４枚落ち（飛、角、両香）
            'without a rook, a bishop, right knight, 2 lances': 'without5Pieces',  # ５枚落ち（飛、角、右桂、両香）
            'without a rook, a bishop, left knight, 2 lances': 'withoutLeft5Pieces',  # 左５枚落ち（飛、角、左桂、両香）
            'without a hisha, a kaku, 2 kyoushas, 2 keimas': 'without6Pieces',  # ６枚落ち
            'without left 7 pieces': 'withoutLeft7Pieces',  # 左七枚落ち
            'without right 7 pieces': 'withoutRight7Pieces',  # 右七枚落ち
            # ８枚落ち（飛、角、両銀、両桂、両香）
            'without a rook, a bishop, 2 silvers, 2 knights, 2 lances': 'without8Pieces',
            # １０枚落ち（飛、角、両金、両銀、両桂、両香）
            'without a rook, a bishop, 2 golds, 2 silvers, 2knight, 2 lances': 'lost10Pieces',
            'others': 'others',
        }

        self._handicap_statement = re.compile(r"^手合割：(.+)$")

    def to_pivot(self, handicap):
        if handicap in self._handicap:
            return self._handicap[handicap]

        return handicap

    def from_pivot(self, handicap):
        items = [k for k, v in self._handicap.items() if v == handicap]
        return f"handicap='{items[0]}'\n"

    def match(self, line):
        return self._handicap_statement.match(line)


handicap_statement_p = HandicapStatementP()
```
