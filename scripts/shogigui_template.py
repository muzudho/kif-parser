from scripts.base_template import BaseTemplate
from scripts.kifu_specification import sign_p, piece_type_p


class ShogiguiTemplate(BaseTemplate):
    """ShogiGUIテンプレート"""

    @property
    def name(self):
        return "shogigui"

    def move_row(self, row_data):
        kifu_text = ""

        # Move num（n手目）
        if "num" in row_data:
            num = row_data["num"]
            kifu_text += f"{num:>4} "

        if "m" in row_data:
            """Move（指し手）
            全角半角に関わらず15文字幅
            """
            m = row_data["m"]

            move_text = ""
            # 半角スペース幅
            space_num = 15

            if "sign" in m:
                sign = m["sign"]
                move_text += f"{sign}"
                space_num -= len(sign)

            # Destination file（行き先の筋）
            if "x" in m:
                dst_file = m["x"]
                dst_rank = m["y"]
                move_text += f"{dst_file}{dst_rank}"
                space_num -= 2

            # Example: `同　`
            if "dst" in m:
                dst = m["dst"]
                move_text += dst
                space_num -= len(dst)

            # Piece type（移動した駒、先後の無い駒種類）
            if "pt" in m:
                piece_type = m["pt"]
                move_text += f"{piece_type}"
                space_num -= len(piece_type)

            # Example: `打`
            if "drop" in m:
                drop = m["drop"]
                move_text += drop
                space_num -= len(drop)

            # Promote（成り）
            if "pro" in m:
                pro = m["pro"]
                move_text += pro
                space_num -= len(pro)

            # Source（移動元の升）
            if "src" in m:
                src = m["src"]  # 11 とか 99 とか
                s = f"({src})"
                move_text += s
                space_num -= len(s)

            # 左にスペースを詰めます
            move_text += ''.ljust(space_num, ' ')

            kifu_text += f"{move_text}"

        # Expended time（消費時間）
        if "time" in row_data:
            time = row_data["time"]
            # time[0] # hour（時）
            timeMin = time[1]  # minute（分）
            timeSec = time[2]  # second（秒）
        else:
            time = None

        # Total expended time（消費時間合計）
        if "total" in row_data:
            total = row_data["total"]
            totalExpendedTimeHr = total[0]  # hour（時）
            totalMin = total[1]  # minute（分）
            totalSec = total[2]  # second（秒）
        else:
            total = None

        if time and total:
            kifu_text += f"({timeMin:>2}:{timeSec:02}/{totalExpendedTimeHr:02}:{totalMin:02}:{totalSec:02})"

        # Comment（コメント）
        if "comment" in row_data:
            comment = row_data["comment"]
            kifu_text += f"#{comment}"

        return f"{kifu_text}\n"

    def end_of_file(self):
        """ファイルの最後
        ShogiGUIのファイルの最後は空行が２つです"""
        return "\n"
