# Translation - 翻訳案

.kifファイルの国際化に向けた翻訳について、主な日本語の一覧。  
**英語さっぱりわからん**  

翻訳の参考: 📖　[Marken-Foo/shogi-translations](https://github.com/Marken-Foo/shogi-translations/blob/main/KIF-standard.md)  

| .kif        | 訳者                  | 対訳案                                                      | 説明                               |
| ----------- | ------------------- | -------------------------------------------------------- | -------------------------------- |
| 付加情報        | むずでょ                | Appendix (?)                                             | 元の.kifファイルには無いが、加えておきたい情報ぐらいの意味  |
|             | Marken-Foo          | Other information                                        |                                  |
| 棋譜          | むずでょ                | Record (?)                                               | 頻繁に出てくるのに知らない英語                  |
|             | Marken-Foo          |                                                          | 英語で kifu か game record でもいい      |
| 対局情報        | むずでょ                | Game info (?)                                            | .kifファイルに出てこなくても新規格で使うかもしれない単語   |
|             | Marken-Foo          | Game information                                         |                                  |
| 開始日時        | むずでょ                | Start datetime (?)                                       | 対局情報。対局開始日付時刻                    |
| 対局日         | Marken-Foo          | Start date                                               | 「開始日時」の別表記                       |
| 終了日時        | むずでょ                | End datetime (?)                                         | 対局情報。対局終了日付時刻                    |
|             | Marken-Foo          | End date                                                 |                                  |
| 棋戦          | むずでょ                | Tournament (?)                                           | 対局情報。                            |
|             | Marken-Foo          | Tournament / Event                                       | Event はチェスのPGN形式由来               |
| 戦型          | むずでょ                | Form (?)                                                 | 対局情報。                            |
|             | Marken-Foo          | Opening                                                  |                                  |
| 表題          |                     | Thema (?)                                                | 対局情報。なんだこりゃ                      |
|             |                     | Heading                                                  |                                  |
| 持ち時間        |                     | Time (?)                                                 | 対局情報。                            |
|             |                     | Time control (initial starting time on clock)            |                                  |
| 消費時間        |                     | Total elapsed (?)                                        | 対局情報として。                         |
|             |                     | Time expended                                            |                                  |
| 場所          |                     | Place (?)                                                | 対局情報。対局場所                        |
|             |                     | Location                                                 |                                  |
| 掲載          |                     | Media (?)                                                | 対局情報。この棋譜が載ってた雑誌か                |
|             |                     | Published                                                |                                  |
| 備考          |                     | Remark (?)                                               | 対局情報。詰将棋情報でも使われる                 |
|             |                     | Reference                                                |                                  |
| 先手省略名       |                     | (?)                                                      | 対局情報。 `局面図の印刷等に使用する。` とのこと       |
|             |                     | Sente's name                                             |                                  |
| 後手省略名       |                     | (?)                                                      | 対局情報。 `局面図の印刷等に使用する。` とのこと       |
|             |                     | Gote's name                                              |                                  |
| 作品番号        |                     | Article number (?)                                       | 詰将棋情報                            |
|             |                     | Problem ID                                               |                                  |
| 作品名         |                     | Title (?)                                                | 詰将棋情報                            |
|             |                     | Problem name                                             |                                  |
| 作者          |                     | Author (?)                                               | 詰将棋情報                            |
|             |                     | Composer                                                 |                                  |
| 発表誌         |                     | (?)                                                      | 詰将棋情報                            |
|             |                     | Publication (the magazine/book/etc. it was published in) |                                  |
| 発表年月        |                     | (?)                                                      | 詰将棋情報                            |
|             |                     | Date of publication                                      |                                  |
| 出典          |                     | (?)                                                      | 詰将棋情報                            |
|             |                     | Collection                                               |                                  |
| 手数          |                     | (?)                                                      | 詰将棋情報                            |
|             |                     | Length (number of halfmoves)                             |                                  |
| 完全性         |                     | (?)                                                      | 詰将棋情報                            |
|             |                     | Status (whether it is cooked or sound)                   |                                  |
| 分類          |                     | Kind (?)                                                 | 詰将棋情報                            |
|             |                     | Type                                                     |                                  |
| 受賞          |                     | Award (?)                                                | 詰将棋情報                            |
|             |                     | Prize (if it won a prize or award)                       |                                  |
| 備考          |                     |                                                          | 対局情報の方にも同じのがある                   |
|             |                     | Reference (can be used like the same field for games)    |                                  |
| 対局者         |                     | Player (?)                                               |                                  |
|             |                     | player                                                   |                                  |
| 対局者名        |                     | Player name (?)                                          |                                  |
|             |                     | player name                                              |                                  |
| 手番 (?)      |                     | Color (?)                                                | 色でいいのか？ 先手、後手、下手、上手を指す           |
|             |                     | side, symbol                                             |                                  |
| 先手          |                     | Black (?)                                                | 色でいいのか？                          |
|             |                     | sente                                                    |                                  |
| 後手          |                     | White (?)                                                |                                  |
|             |                     | gote                                                     |                                  |
| 下手          |                     | Trainee (?)                                              | 駒落ち将棋。下手は次に指すが先手の扱いのはず           |
|             |                     | shitate (handicap receiver)                              |                                  |
| 上手          |                     | Trainer (?)                                              | 駒落ち将棋。上手は最初に指すが後手の扱いのはず          |
|             |                     | uwate (handicap giver) respectively                      |                                  |
| 手合割         |                     | Handicap (?)                                             | 平手～10枚落ちなどの駒落ち将棋を指す              |
|             |                     | Handicap                                                 |                                  |
| 平手          |                     | Even (?)                                                 | 手割合                              |
|             |                     | even                                                     |                                  |
| 香落ち         |                     | Without left lance (?)                                   | 手割合。左の香が落ちる                      |
|             |                     | lance                                                    |                                  |
| 右香落ち        |                     | Without right lance (?)                                  | 手割合                              |
|             |                     | right lance                                              |                                  |
| 角落ち         |                     | Without a bishop (?)                                     | 手割合                              |
|             |                     | bishop                                                   |                                  |
| 飛車落ち        |                     | Without a rook (?)                                       | 手割合                              |
|             |                     | rook                                                     |                                  |
| 飛香落ち        |                     | Without a rook, a lance (?)                              | 手割合。左の香が落ちる                      |
|             |                     | rook-lance                                               |                                  |
| 二枚落ち        |                     | Without 2 pieces (?)                                     | 手割合。飛角が落ちる                       |
|             |                     | two piece                                                |                                  |
| 三枚落ち        |                     | Without 3 pieces (?)                                     | 手割合。飛、角、左香落ち                     |
|             |                     | three piece                                              |                                  |
| 四枚落ち        |                     | Without 4 pieces (?)                                     | 手割合。飛、角、両香落ち                     |
|             |                     | four piece                                               |                                  |
| 五枚落ち        |                     | Without 5 pieces  (?)                                    | 手割合。飛、角、右桂、両香落ち                  |
|             |                     | five piece                                               |                                  |
| 左五枚落ち       |                     | Without left 5 pieces  (?)                               | 手割合。飛、角、左桂、両香落ち                  |
|             |                     | left [knight] five piece                                 |                                  |
| 六枚落ち        |                     | Without 6 pieces  (?)                                    | 手割合。飛、角、両桂、両香落ち                  |
|             |                     | six piece                                                |                                  |
| 左七枚落ち       |                     | Without left 7 pieces  (?)                               | 手割合。飛、角、左銀、両桂、両香落ち               |
|             |                     |                                                          |                                  |
| 右七枚落ち       |                     | Without right 7 pieces  (?)                              | 手割合。飛、角、右銀、両桂、両香落ち               |
|             |                     |                                                          |                                  |
| 八枚落ち        |                     | Without 8 pieces  (?)                                    | 手割合。飛、角、両銀、両桂、両香落ち               |
|             |                     | eight piece                                              |                                  |
| 十枚落ち        |                     | Without 10 pieces  (?)                                   | 手割合。飛、角、両金、両銀、両桂、両香落ち            |
|             |                     | ten piece                                                |                                  |
| その他         |                     | Others (?)                                               | 手割合。                             |
|             |                     | other                                                    |                                  |
| 手数          |                     | Moves (?)                                                | 1手目、2手目... の数を指す。 Ply はちょっと違うか？  |
|             |                     |                                                          |                                  |
| n手で         |                     | n th (?)                                                 | 「まで26手で後手の勝ち」のように文の中で出てくる        |
|             |                     |                                                          |                                  |
| 指し手         |                     | Move (?)                                                 | ７六歩、２四歩... とかの指し手を指す             |
|             |                     |                                                          |                                  |
| 変化          |                     | Variation (?)                                            | 指し手の変化手順を指す                      |
|             |                     |                                                          |                                  |
| 移動元座標       |                     | Source square (?)                                        |                                  |
|             |                     | origin coordinates                                       |                                  |
| 移動先座標       |                     | Destination square (?)                                   |                                  |
|             |                     | destination coordinates                                  |                                  |
| 筋           |                     | File (?)                                                 | Fileはチェス由来                       |
|             |                     | x                                                        |                                  |
| 段           |                     | Rank (?)                                                 | Rankはチェス由来                       |
|             |                     | y                                                        |                                  |
| 駒（先後を区別する）  |                     | Piece (?)                                                | コンピューター チェス由来                    |
|             |                     |                                                          |                                  |
| 駒（先後を区別しない） |                     | Piece type (?)                                           | PieceTypeはコンピューター チェス由来          |
|             |                     | piece                                                    |                                  |
| 一           |                     | 1                                                        | 盤の段。指し手に出てくる                     |
| 二           |                     | 2                                                        | 盤の段                              |
| 三           |                     | 3                                                        | 盤の段                              |
| 四           |                     | 4                                                        | 盤の段                              |
| 五           |                     | 5                                                        | 盤の段                              |
| 六           |                     | 6                                                        | 盤の段                              |
| 七           |                     | 7                                                        | 盤の段                              |
| 八           |                     | 8                                                        | 盤の段                              |
| 九           |                     | 9                                                        | 盤の段                              |
| 同           |                     | Same (?)                                                 | 同歩... とかの同。無くていい気もする。チェスには無いし    |
|             |                     | the destination coordinate is the same                   |                                  |
| 玉           |                     | King                                                     | 駒の名前。チェスに寄せる場合。将棋の駒は財宝から来てるとも聞くが |
|             |                     | King                                                     |                                  |
| 飛           |                     | Rook                                                     |                                  |
|             |                     |                                                          |                                  |
| 龍           |                     | Promoted rook (?)                                        |                                  |
|             |                     | promoted rook                                            |                                  |
| 竜           |                     | Promoted rook (?)                                        |                                  |
|             |                     | promoted rook (not a typo)                               |                                  |
| 角           |                     | Bishop                                                   |                                  |
|             |                     | bishop                                                   |                                  |
| 馬           |                     | Promoted bishop (?)                                      |                                  |
|             |                     | promoted bishop                                          |                                  |
| 金           |                     | Gold                                                     |                                  |
|             |                     | gold                                                     |                                  |
| 銀           |                     | Silver                                                   |                                  |
|             |                     | silver                                                   |                                  |
| 成銀          |                     | Promoted silver (?)                                      |                                  |
|             |                     | promoted silver                                          |                                  |
| 全           |                     | Promoted silver (?)                                      |                                  |
|             |                     | promoted silver                                          |                                  |
| 桂           | Knight              |                                                          |                                  |
|             |                     | knight                                                   |                                  |
| 成桂          | Promoted knight (?) |                                                          |                                  |
|             |                     | promoted knight                                          |                                  |
| 圭           | Promoted knight (?) |                                                          |                                  |
|             |                     | promoted knight                                          |                                  |
| 香           | Lance               |                                                          |                                  |
|             |                     | lance                                                    |                                  |
| 成香          | Promoted lance (?)  |                                                          |                                  |
|             |                     | promoted lance                                           |                                  |
| 杏           | Promoted lance (?)  |                                                          |                                  |
|             |                     | promoted lance                                           |                                  |
| 歩           | Pawn                |                                                          |                                  |
|             |                     | pawn                                                     |                                  |
| と           | Promoted pawn (?)   |                                                          |                                  |
|             |                     | promoted pawn                                            |                                  |
| 打           | Drop (?)            |                                                          |                                  |
|             |                     | drop                                                     |                                  |
| 成           | Promotion (?)       |                                                          |                                  |
|             |                     | promote                                                  |                                  |
| 中断          | Stop (?)            |                                                          | 対局の終わり方。詰将棋も混ざってるかも              |
|             |                     | Game aborted                                             |                                  |
| 投了          |                     | Resign (?)                                               |                                  |
|             |                     | Resignation                                              |                                  |
| 持将棋         |                     | Ji-shogi (?)                                             | すぐ再対戦するので引き分けではない                |
|             |                     | Jishogi (one of the draw conditions)                     |                                  |
| 千日手         |                     | Fourfold repeatation (?)                                 |                                  |
|             |                     | Sennichite (repetition)                                  |                                  |
| 詰み          |                     | Checkmate (?)                                            |                                  |
|             |                     | Mate                                                     |                                  |
| 切れ負け        |                     | Tome up (?)                                              | 「切れ負けにより」のように文の中で出てくる            |
|             |                     | Loss by time (time out/flag drop)                        |                                  |
| 反則勝ち        |                     | Illegal win (?)                                          | 「後手の反則勝ち」のように文の中で出てくる            |
|             |                     | Illegal move win                                         |                                  |
| 反則負け        |                     | Illegal lose (?)                                         |                                  |
|             |                     | Illegal move loss                                        |                                  |
| 入玉勝ち        |                     | Entering king win (?)                                    | 入玉宣言勝ちのこと                        |
|             |                     | Entering king win                                        |                                  |
| 不戦勝         |                     | Unearned win (?)                                         |                                  |
|             |                     |                                                          |                                  |
| 不戦敗         |                     | Unearned lose (?)                                        |                                  |
|             |                     |                                                          |                                  |
| 勝ち          |                     | Win (?)                                                  | 「後手の勝ち」のように文の中で出てくる              |
|             |                     |                                                          |                                  |
| 負け          |                     | Lose (?)                                                 | 単体では見かけないが、出てくるかも                |
|             |                     |                                                          |                                  |
| １手の消費時間     |                     | Elapsed (?)                                              | 指し手の情報として。                       |
|             |                     | Time expended                                            |                                  |
| 現在の累積の消費時間  |                     | Total elapsed (?)                                        | 指し手の情報として。                       |
|             |                     | player's total time expended                             |                                  |
| 時           |                     | Hour (?)                                                 |                                  |
|             |                     | hours                                                    |                                  |
| 分           |                     | Minute (?)                                               |                                  |
|             |                     | minute, minutes                                          |                                  |
| 秒           |                     | Seconds (?)                                              |                                  |
|             |                     | seconds                                                  |                                  |
| しおり         |                     | Bookmark (?)                                             | 変化手順のジャンプ先ラベルのようなもの              |
|             |                     | Bookmark                                                 |                                  |
|             |                     |                                                          |                                  |
|             |                     |                                                          |                                  |
|             |                     |                                                          |                                  |
