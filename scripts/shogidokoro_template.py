from scripts.base_template import BaseTemplate
from scripts.kifu_specification import sign_p, piece_type_p


class ShogidokoroTemplate(BaseTemplate):
    """将棋所テンプレート"""

    @property
    def name(self):
        return "shogidokoro"

    def move_row(self, row_data):
        kifu_text = ""

        # Move num（n手目）
        if "num" in row_data:
            num = row_data["num"]
            kifu_text += f"{num:>4} "

        # Move（指し手）
        if "m" in row_data:
            m = row_data["m"]

            move_text = ""
            # 半角スペース幅
            spaces = 14

            if "sign" in m:
                sign = m["sign"]
                move_text += f"{sign}"
                spaces -= sign_p.half_width(sign)

            # Destination file（行き先の筋）
            if "x" in m:
                dst_file = m["x"]
                dst_rank = m["y"]
                move_text += f"{dst_file}{dst_rank}"
                spaces -= 4

            if "dst" in m:
                dst = m["dst"]
                if dst == '同　':
                    move_text += dst
                    spaces -= 4
                else:
                    move_text += f"{dst}"
                    spaces -= 2

            # Piece type（移動した駒、先後の無い駒種類）
            if "pt" in m:
                piece_type = m["pt"]
                move_text += f"{piece_type}"
                spaces -= piece_type_p.half_width(piece_type)

            if "drop" in m:
                drop = m["drop"]
                if drop:
                    move_text += drop
                    spaces -= 2

            # Promote（成り）
            if "pro" in m:
                pro = m["pro"]
                if pro:
                    move_text += pro
                    spaces -= 2

            # Source（移動元の升）
            if "src" in m:
                src = m["src"]  # 11 とか 99 とか
                move_text += f"({src})"
                spaces -= 4

            # 左にスペースを詰めます
            move_text += ''.ljust(spaces, ' ')

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
            kifu_text += f"({timeMin:02}:{timeSec:02} / {totalExpendedTimeHr:02}:{totalMin:02}:{totalSec:02})"

        # Comment（コメント）
        if "comment" in row_data:
            comment = row_data["comment"]
            kifu_text += f"#{comment}"

        return f"{kifu_text}\n"
