# Translation - 翻訳案

.kifファイルの国際化に向けた翻訳について、主な日本語の一覧。  
**英語さっぱりわからん**  

翻訳の参考: 📖　[Marken-Foo/shogi-translations](https://github.com/Marken-Foo/shogi-translations/blob/main/KIF-standard.md)  

| .kif        | 訳者         | 対訳案                                                      | 説明                               |
| ----------- | ---------- | -------------------------------------------------------- | -------------------------------- |
| 付加情報        | むずでょ       | Appendix (?)                                             | 元の.kifファイルには無いが、加えておきたい情報ぐらいの意味  |
|             | Marken-Foo | Other information                                        |                                  |
| 棋譜          | むずでょ       | Record (?)                                               | 頻繁に出てくるのに知らない英語                  |
|             | Marken-Foo |                                                          | 英語で kifu か game record でもいい      |
| 対局情報        | むずでょ       | Game info (?)                                            | .kifファイルに出てこなくても新規格で使うかもしれない単語   |
|             | Marken-Foo | Game information                                         |                                  |
| 開始日時        | むずでょ       | Start datetime (?)                                       | 対局情報。対局開始日付時刻                    |
| 対局日         | Marken-Foo | Start date                                               | 「開始日時」の別表記                       |
| 終了日時        | むずでょ       | End datetime (?)                                         | 対局情報。対局終了日付時刻                    |
|             | Marken-Foo | End date                                                 |                                  |
| 棋戦          | むずでょ       | Tournament (?)                                           | 対局情報。                            |
|             | Marken-Foo | Tournament / Event                                       | Event はチェスのPGN形式由来               |
| 戦型          | むずでょ       | Form (?)                                                 | 対局情報。                            |
|             | Marken-Foo | Opening                                                  | 戦型は序盤から決まるので                     |
| 表題          | む          | Thema (?)                                                | 対局情報。なんだこりゃ                      |
|             |            | Heading                                                  | なんだこりゃ                           |
| 持ち時間        | む          | Time (?)                                                 | 対局情報。                            |
|             |            | Time control (initial starting time on clock)            | Time control はチェスの用語だ            |
| 消費時間        | む          | Total elapsed (?)                                        | 対局情報として。                         |
|             |            | Time expended                                            |                                  |
| 場所          | む          | Place (?)                                                | 対局情報。対局場所                        |
|             |            | Location                                                 | Location はチェスのPGN形式由来            |
| 掲載          | む          | Media (?)                                                | 対局情報。この棋譜が載ってた雑誌か                |
|             |            | Published                                                |                                  |
| 備考          | む          | Remark (?)                                               | 対局情報。詰将棋情報でも使われる                 |
|             |            | Reference                                                | わからん                             |
| 先手省略名       | む          | (?)                                                      | 対局情報。 `局面図の印刷等に使用する。` とのこと       |
|             |            | Sente's name                                             |                                  |
| 後手省略名       | む          | (?)                                                      | 対局情報。 `局面図の印刷等に使用する。` とのこと       |
|             |            | Gote's name                                              |                                  |
| 作品番号        | む          | Article number (?)                                       | 詰将棋情報                            |
|             |            | Problem ID                                               |                                  |
| 作品名         | む          | Title (?)                                                | 詰将棋情報                            |
|             |            | Problem name                                             |                                  |
| 作者          | む          | Author (?)                                               | 詰将棋情報                            |
|             |            | Composer                                                 |                                  |
| 発表誌         | む          | (?)                                                      | 詰将棋情報                            |
|             |            | Publication (the magazine/book/etc. it was published in) |                                  |
| 発表年月        | む          | (?)                                                      | 詰将棋情報                            |
|             |            | Date of publication                                      |                                  |
| 出典          | む          | (?)                                                      | 詰将棋情報                            |
|             |            | Collection                                               |                                  |
| 手数          | む          | (?)                                                      | 詰将棋情報                            |
|             |            | Length (number of halfmoves)                             |                                  |
| 完全性         | む          | (?)                                                      | 詰将棋情報                            |
|             |            | Status (whether it is cooked or sound)                   |                                  |
| 分類          | む          | Kind (?)                                                 | 詰将棋情報                            |
|             |            | Type                                                     |                                  |
| 受賞          | む          | Award (?)                                                | 詰将棋情報                            |
|             |            | Prize (if it won a prize or award)                       |                                  |
| 備考          | む          |                                                          | 対局情報の方にも同じのがある                   |
|             |            | Reference (can be used like the same field for games)    |                                  |
| 対局者         | む          | Player (?)                                               |                                  |
|             |            | player                                                   |                                  |
| 対局者名        | む          | Player name (?)                                          |                                  |
|             |            | player name                                              |                                  |
| 手番 (?)      | む          | Color (?)                                                | 色でいいのか？ 先手、後手、下手、上手を指す           |
|             |            | side, symbol                                             |                                  |
| 先手          | む          | Black (?)                                                | 色でいいのか？                          |
|             |            | sente                                                    |                                  |
| 後手          | む          | White (?)                                                |                                  |
|             |            | gote                                                     |                                  |
| 下手          | む          | Trainee (?)                                              | 駒落ち将棋。下手は次に指すが先手の扱いのはず           |
|             |            | shitate (handicap receiver)                              |                                  |
| 上手          | む          | Trainer (?)                                              | 駒落ち将棋。上手は最初に指すが後手の扱いのはず          |
|             |            | uwate (handicap giver) respectively                      |                                  |
| 手合割         | む          | Handicap (?)                                             | 平手～10枚落ちなどの駒落ち将棋を指す              |
|             |            | Handicap                                                 |                                  |
| 平手          | む          | Even (?)                                                 | 手割合                              |
|             |            | even                                                     |                                  |
| 香落ち         | む          | Without left lance (?)                                   | 手割合。左の香が落ちる                      |
|             |            | lance                                                    |                                  |
| 右香落ち        | む          | Without right lance (?)                                  | 手割合                              |
|             |            | right lance                                              |                                  |
| 角落ち         | む          | Without a bishop (?)                                     | 手割合                              |
|             |            | bishop                                                   |                                  |
| 飛車落ち        | む          | Without a rook (?)                                       | 手割合                              |
|             |            | rook                                                     |                                  |
| 飛香落ち        | む          | Without a rook, a lance (?)                              | 手割合。左の香が落ちる                      |
|             |            | rook-lance                                               |                                  |
| 二枚落ち        | む          | Without 2 pieces (?)                                     | 手割合。飛角が落ちる                       |
|             |            | two piece                                                |                                  |
| 三枚落ち        | む          | Without 3 pieces (?)                                     | 手割合。飛、角、左香落ち                     |
|             |            | three piece                                              |                                  |
| 四枚落ち        | む          | Without 4 pieces (?)                                     | 手割合。飛、角、両香落ち                     |
|             |            | four piece                                               |                                  |
| 五枚落ち        | む          | Without 5 pieces  (?)                                    | 手割合。飛、角、右桂、両香落ち                  |
|             |            | five piece                                               |                                  |
| 左五枚落ち       | む          | Without left 5 pieces  (?)                               | 手割合。飛、角、左桂、両香落ち                  |
|             |            | left [knight] five piece                                 |                                  |
| 六枚落ち        | む          | Without 6 pieces  (?)                                    | 手割合。飛、角、両桂、両香落ち                  |
|             |            | six piece                                                |                                  |
| 左七枚落ち       | む          | Without left 7 pieces  (?)                               | 手割合。飛、角、左銀、両桂、両香落ち               |
|             |            |                                                          |                                  |
| 右七枚落ち       | む          | Without right 7 pieces  (?)                              | 手割合。飛、角、右銀、両桂、両香落ち               |
|             |            |                                                          |                                  |
| 八枚落ち        | む          | Without 8 pieces  (?)                                    | 手割合。飛、角、両銀、両桂、両香落ち               |
|             |            | eight piece                                              |                                  |
| 十枚落ち        | む          | Without 10 pieces  (?)                                   | 手割合。飛、角、両金、両銀、両桂、両香落ち            |
|             |            | ten piece                                                |                                  |
| その他         | む          | Others (?)                                               | 手割合。                             |
|             |            | other                                                    |                                  |
| 手数          | む          | Moves (?)                                                | 1手目、2手目... の数を指す。 Ply はちょっと違うか？  |
|             |            |                                                          |                                  |
| n手で         | む          | n th (?)                                                 | 「まで26手で後手の勝ち」のように文の中で出てくる        |
|             |            |                                                          |                                  |
| 指し手         | む          | Move (?)                                                 | ７六歩、２四歩... とかの指し手を指す             |
|             |            |                                                          |                                  |
| 変化          | む          | Variation (?)                                            | 指し手の変化手順を指す                      |
|             |            |                                                          |                                  |
| 移動元座標       | む          | Source square (?)                                        |                                  |
|             |            | origin coordinates                                       |                                  |
| 移動先座標       | む          | Destination square (?)                                   |                                  |
|             |            | destination coordinates                                  |                                  |
| 筋           | む          | File (?)                                                 | Fileはチェス由来                       |
|             |            | x                                                        |                                  |
| 段           | む          | Rank (?)                                                 | Rankはチェス由来                       |
|             |            | y                                                        |                                  |
| 駒（先後を区別する）  | む          | Piece (?)                                                | コンピューター チェス由来                    |
|             |            |                                                          |                                  |
| 駒（先後を区別しない） | む          | Piece type (?)                                           | PieceTypeはコンピューター チェス由来          |
|             |            | piece                                                    |                                  |
| 一           | む          | 1                                                        | 盤の段。指し手に出てくる                     |
| 二           | む          | 2                                                        | 盤の段                              |
| 三           | む          | 3                                                        | 盤の段                              |
| 四           | む          | 4                                                        | 盤の段                              |
| 五           | む          | 5                                                        | 盤の段                              |
| 六           | む          | 6                                                        | 盤の段                              |
| 七           | む          | 7                                                        | 盤の段                              |
| 八           | む          | 8                                                        | 盤の段                              |
| 九           | む          | 9                                                        | 盤の段                              |
| 同           | む          | Same (?)                                                 | 同歩... とかの同。無くていい気もする。チェスには無いし    |
|             |            | the destination coordinate is the same                   |                                  |
| 玉           | む          | King                                                     | 駒の名前。チェスに寄せる場合。将棋の駒は財宝から来てるとも聞くが |
|             |            | King                                                     |                                  |
| 飛           | む          | Rook                                                     |                                  |
|             |            |                                                          |                                  |
| 龍           | む          | Promoted rook (?)                                        |                                  |
|             |            | promoted rook                                            |                                  |
| 竜           | む          | Promoted rook (?)                                        |                                  |
|             |            | promoted rook (not a typo)                               |                                  |
| 角           | む          | Bishop                                                   |                                  |
|             |            | bishop                                                   |                                  |
| 馬           | む          | Promoted bishop (?)                                      |                                  |
|             |            | promoted bishop                                          |                                  |
| 金           | む          | Gold                                                     |                                  |
|             |            | gold                                                     |                                  |
| 銀           | む          | Silver                                                   |                                  |
|             |            | silver                                                   |                                  |
| 成銀          | む          | Promoted silver (?)                                      |                                  |
|             |            | promoted silver                                          |                                  |
| 全           | む          | Promoted silver (?)                                      |                                  |
|             |            | promoted silver                                          |                                  |
| 桂           | む          | Knight                                                   |                                  |
|             |            | knight                                                   |                                  |
| 成桂          | む          | Promoted knight (?)                                      |                                  |
|             |            | promoted knight                                          |                                  |
| 圭           | む          | Promoted knight (?)                                      |                                  |
|             |            | promoted knight                                          |                                  |
| 香           | む          | Lance                                                    |                                  |
|             |            | lance                                                    |                                  |
| 成香          | む          | Promoted lance (?)                                       |                                  |
|             |            | promoted lance                                           |                                  |
| 杏           | む          | Promoted lance (?)                                       |                                  |
|             |            | promoted lance                                           |                                  |
| 歩           | む          | Pawn                                                     |                                  |
|             |            | pawn                                                     |                                  |
| と           | む          | Promoted pawn (?)                                        |                                  |
|             |            | promoted pawn                                            |                                  |
| 打           | む          | Drop (?)                                                 |                                  |
|             |            | drop                                                     |                                  |
| 成           | む          | Promotion (?)                                            |                                  |
|             |            | promote                                                  |                                  |
| 中断          | む          | Stop (?)                                                 | 対局の終わり方。詰将棋も混ざってるかも              |
|             |            | Game aborted                                             |                                  |
| 投了          | む          | Resign (?)                                               |                                  |
|             |            | Resignation                                              |                                  |
| 持将棋         | む          | Ji-shogi (?)                                             | すぐ再対戦するので引き分けではない                |
|             |            | Jishogi (one of the draw conditions)                     |                                  |
| 千日手         | む          | Fourfold repeatation (?)                                 |                                  |
|             |            | Sennichite (repetition)                                  |                                  |
| 詰み          | む          | Checkmate (?)                                            |                                  |
|             |            | Mate                                                     |                                  |
| 切れ負け        | む          | Tome up (?)                                              | 「切れ負けにより」のように文の中で出てくる            |
|             |            | Loss by time (time out/flag drop)                        |                                  |
| 反則勝ち        | む          | Illegal win (?)                                          | 「後手の反則勝ち」のように文の中で出てくる            |
|             |            | Illegal move win                                         |                                  |
| 反則負け        | む          | Illegal lose (?)                                         |                                  |
|             |            | Illegal move loss                                        |                                  |
| 入玉勝ち        | む          | Entering king win (?)                                    | 入玉宣言勝ちのこと                        |
|             |            | Entering king win                                        |                                  |
| 不戦勝         | む          | Unearned win (?)                                         |                                  |
|             |            |                                                          |                                  |
| 不戦敗         | む          | Unearned lose (?)                                        |                                  |
|             |            |                                                          |                                  |
| 勝ち          | む          | Win (?)                                                  | 「後手の勝ち」のように文の中で出てくる              |
|             |            |                                                          |                                  |
| 負け          | む          | Lose (?)                                                 | 単体では見かけないが、出てくるかも                |
|             |            |                                                          |                                  |
| １手の消費時間     | む          | Elapsed (?)                                              | 指し手の情報として。                       |
|             |            | Time expended                                            |                                  |
| 現在の累積の消費時間  | む          | Total elapsed (?)                                        | 指し手の情報として。                       |
|             |            | player's total time expended                             |                                  |
| 時           | む          | Hour (?)                                                 |                                  |
|             |            | hours                                                    |                                  |
| 分           | む          | Minute (?)                                               |                                  |
|             |            | minute, minutes                                          |                                  |
| 秒           | む          | Seconds (?)                                              |                                  |
|             |            | seconds                                                  |                                  |
| しおり         | む          | Bookmark (?)                                             | 変化手順のジャンプ先ラベルのようなもの              |
|             |            | Bookmark                                                 |                                  |
|             |            |                                                          |                                  |
|             |            |                                                          |                                  |
|             |            |                                                          |                                  |
