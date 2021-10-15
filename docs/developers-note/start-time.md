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
