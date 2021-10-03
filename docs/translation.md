# Translation - 翻訳案

.kifファイルの国際化に向けた翻訳について、主な日本語の一覧。  
**英語さっぱりわからん**  

翻訳の参考: 📖　[Marken-Foo/shogi-translations](https://github.com/Marken-Foo/shogi-translations/blob/main/KIF-standard.md)  

| .kif        | むずでょ対訳案                     | Marken-Foo案                                              | 説明                               |
| ----------- | --------------------------- | -------------------------------------------------------- | -------------------------------- |
| 付加情報        | Appendix (?)                |                                                          | 元の.kifファイルには無いが、加えておきたい情報ぐらいの意味  |
| 棋譜          | Record (?)                  |                                                          | 頻繁に出てくるのに知らない英語                  |
| 対局情報        | Game info (?)               | Game information                                         | .kifファイルに出てこなくても新規格で使うかもしれない単語   |
| 開始日時        | Start datetime (?)          | Start date                                               | 対局情報。対局開始日付時刻                    |
| 対局日         |                             |                                                          | 「開始日時」の別表記                       |
| 終了日時        | End datetime (?)            | End date                                                 | 対局情報。対局終了日付時刻                    |
| 棋戦          | Tournament (?)              | Tournament                                               | 対局情報。                            |
| 戦型          | Form (?)                    | Opening                                                  | 対局情報。                            |
| 表題          | Thema (?)                   | Heading                                                  | 対局情報。なんだこりゃ                      |
| 持ち時間        | Time (?)                    | Time control (initial starting time on clock)            | 対局情報。                            |
| 消費時間        | Total elapsed (?)           | Time expended                                            | 対局情報として。                         |
| 場所          | Place (?)                   | Location                                                 | 対局情報。対局場所                        |
| 掲載          | Media (?)                   | Published                                                | 対局情報。この棋譜が載ってた雑誌か                |
| 備考          | Remark (?)                  | Reference                                                | 対局情報。詰将棋情報でも使われる                 |
| 先手省略名       | (?)                         | Sente's name                                             | 対局情報。 `局面図の印刷等に使用する。` とのこと       |
| 後手省略名       | (?)                         | Gote's name                                              | 対局情報。 `局面図の印刷等に使用する。` とのこと       |
| 作品番号        | Article number (?)          | Problem ID                                               | 詰将棋情報                            |
| 作品名         | Title (?)                   | Problem name                                             | 詰将棋情報                            |
| 作者          | Author (?)                  | Composer                                                 | 詰将棋情報                            |
| 発表誌         | (?)                         | Publication (the magazine/book/etc. it was published in) | 詰将棋情報                            |
| 発表年月        | (?)                         | Date of publication                                      | 詰将棋情報                            |
| 出典          | (?)                         | Collection                                               | 詰将棋情報                            |
| 手数          | (?)                         | Length (number of halfmoves)                             | 詰将棋情報                            |
| 完全性         | (?)                         | Status (whether it is cooked or sound)                   | 詰将棋情報                            |
| 分類          | Kind (?)                    | Type                                                     | 詰将棋情報                            |
| 受賞          | Award (?)                   | Prize (if it won a prize or award)                       | 詰将棋情報                            |
| 備考          |                             | Reference (can be used like the same field for games)    | 対局情報の方にも同じのがある                   |
| 対局者         | Player (?)                  | player                                                   |                                  |
| 対局者名        | Player name (?)             | player name                                              |                                  |
| 手番 (?)      | Color (?)                   | side, symbol                                             | 色でいいのか？ 先手、後手、下手、上手を指す           |
| 先手          | Black (?)                   | sente                                                    | 色でいいのか？                          |
| 後手          | White (?)                   | gote                                                     |                                  |
| 下手          | Trainee (?)                 | shitate (handicap receiver)                              | 駒落ち将棋。下手は次に指すが先手の扱いのはず           |
| 上手          | Trainer (?)                 | uwate (handicap giver) respectively                      | 駒落ち将棋。上手は最初に指すが後手の扱いのはず          |
| 手合割         | Handicap (?)                | Handicap                                                 | 平手～10枚落ちなどの駒落ち将棋を指す              |
| 平手          | Even (?)                    | even                                                     | 手割合                              |
| 香落ち         | Without left lance (?)      | lance                                                    | 手割合。左の香が落ちる                      |
| 右香落ち        | Without right lance (?)     | right lance                                              | 手割合                              |
| 角落ち         | Without a bishop (?)        | bishop                                                   | 手割合                              |
| 飛車落ち        | Without a rook (?)          | rook                                                     | 手割合                              |
| 飛香落ち        | Without a rook, a lance (?) | rook-lance                                               | 手割合。左の香が落ちる                      |
| 二枚落ち        | Without 2 pieces (?)        | two piece                                                | 手割合。飛角が落ちる                       |
| 三枚落ち        | Without 3 pieces (?)        | three piece                                              | 手割合。飛、角、左香落ち                     |
| 四枚落ち        | Without 4 pieces (?)        | four piece                                               | 手割合。飛、角、両香落ち                     |
| 五枚落ち        | Without 5 pieces  (?)       | five piece                                               | 手割合。飛、角、右桂、両香落ち                  |
| 左五枚落ち       | Without left 5 pieces  (?)  | left [knight] five piece                                 | 手割合。飛、角、左桂、両香落ち                  |
| 六枚落ち        | Without 6 pieces  (?)       | six piece                                                | 手割合。飛、角、両桂、両香落ち                  |
| 左七枚落ち       | Without left 7 pieces  (?)  |                                                          | 手割合。飛、角、左銀、両桂、両香落ち               |
| 右七枚落ち       | Without right 7 pieces  (?) |                                                          | 手割合。飛、角、右銀、両桂、両香落ち               |
| 八枚落ち        | Without 8 pieces  (?)       | eight piece                                              | 手割合。飛、角、両銀、両桂、両香落ち               |
| 十枚落ち        | Without 10 pieces  (?)      | ten piece                                                | 手割合。飛、角、両金、両銀、両桂、両香落ち            |
| その他         | Others (?)                  | other                                                    | 手割合。                             |
| 手数          | Moves (?)                   |                                                          | 1手目、2手目... の数を指す。 Ply はちょっと違うか？  |
| n手で         | n th (?)                    |                                                          | 「まで26手で後手の勝ち」のように文の中で出てくる        |
| 指し手         | Move (?)                    |                                                          | ７六歩、２四歩... とかの指し手を指す             |
| 変化          | Variation (?)               |                                                          | 指し手の変化手順を指す                      |
| 移動元座標       | Source square (?)           | origin coordinates                                       |                                  |
| 移動先座標       | Destination square (?)      | destination coordinates                                  |                                  |
| 筋           | File (?)                    | x                                                        | Fileはチェス由来                       |
| 段           | Rank (?)                    | y                                                        | Rankはチェス由来                       |
| 駒（先後を区別する）  | Piece (?)                   |                                                          | コンピューター チェス由来                    |
| 駒（先後を区別しない） | Piece type (?)              | piece                                                    | PieceTypeはコンピューター チェス由来          |
| 一           | 1                           |                                                          | 盤の段。指し手に出てくる                     |
| 二           | 2                           |                                                          | 盤の段                              |
| 三           | 3                           |                                                          | 盤の段                              |
| 四           | 4                           |                                                          | 盤の段                              |
| 五           | 5                           |                                                          | 盤の段                              |
| 六           | 6                           |                                                          | 盤の段                              |
| 七           | 7                           |                                                          | 盤の段                              |
| 八           | 8                           |                                                          | 盤の段                              |
| 九           | 9                           |                                                          | 盤の段                              |
| 同           | Same (?)                    | the destination coordinate is the same                   | 同歩... とかの同。無くていい気もする。チェスには無いし    |
| 玉           | King                        | King                                                     | 駒の名前。チェスに寄せる場合。将棋の駒は財宝から来てるとも聞くが |
| 飛           | Rook                        |                                                          |                                  |
| 龍           | Promoted rook (?)           | promoted rook                                            |                                  |
| 竜           | Promoted rook (?)           | promoted rook (not a typo)                               |                                  |
| 角           | Bishop                      | bishop                                                   |                                  |
| 馬           | Promoted bishop (?)         | promoted bishop                                          |                                  |
| 金           | Gold                        | gold                                                     |                                  |
| 銀           | Silver                      | silver                                                   |                                  |
| 成銀          | Promoted silver (?)         | promoted silver                                          |                                  |
| 全           | Promoted silver (?)         | promoted silver                                          |                                  |
| 桂           | Knight                      | knight                                                   |                                  |
| 成桂          | Promoted knight (?)         | promoted knight                                          |                                  |
| 圭           | Promoted knight (?)         | promoted knight                                          |                                  |
| 香           | Lance                       | lance                                                    |                                  |
| 成香          | Promoted lance (?)          | promoted lance                                           |                                  |
| 杏           | Promoted lance (?)          | promoted lance                                           |                                  |
| 歩           | Pawn                        | pawn                                                     |                                  |
| と           | Promoted pawn (?)           | promoted pawn                                            |                                  |
| 打           | Drop (?)                    | drop                                                     |                                  |
| 成           | Promotion (?)               | promote                                                  |                                  |
| 中断          | Stop (?)                    | Game aborted                                             | 対局の終わり方。詰将棋も混ざってるかも              |
| 投了          | Resign (?)                  | Resignation                                              |                                  |
| 持将棋         | Ji-shogi (?)                | Jishogi (one of the draw conditions)                     | すぐ再対戦するので引き分けではない                |
| 千日手         | Fourfold repeatation (?)    | Sennichite (repetition)                                  |                                  |
| 詰み          | Checkmate (?)               | Mate                                                     |                                  |
| 切れ負け        | Tome up (?)                 | Loss by time (time out/flag drop)                        | 「切れ負けにより」のように文の中で出てくる            |
| 反則勝ち        | Illegal win (?)             | Illegal move win                                         | 「後手の反則勝ち」のように文の中で出てくる            |
| 反則負け        | Illegal lose (?)            | Illegal move loss                                        |                                  |
| 入玉勝ち        | Entering king win (?)       | Entering king win                                        | 入玉宣言勝ちのこと                        |
| 不戦勝         | Unearned win (?)            |                                                          |                                  |
| 不戦敗         | Unearned lose (?)           |                                                          |                                  |
| 勝ち          | Win (?)                     |                                                          | 「後手の勝ち」のように文の中で出てくる              |
| 負け          | Lose (?)                    |                                                          | 単体では見かけないが、出てくるかも                |
| １手の消費時間     | Elapsed (?)                 | Time expended                                            | 指し手の情報として。                       |
| 現在の累積の消費時間  | Total elapsed (?)           | player's total time expended                             | 指し手の情報として。                       |
| 時           | Hour (?)                    | hours                                                    |                                  |
| 分           | Minute (?)                  | minute, minutes                                          |                                  |
| 秒           | Seconds (?)                 | seconds                                                  |                                  |
| しおり         | Bookmark (?)                | Bookmark                                                 | 変化手順のジャンプ先ラベルのようなもの              |
|             |                             |                                                          |                                  |
