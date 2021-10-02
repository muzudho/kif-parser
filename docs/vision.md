# Vision - 展望

## Overview - 全体図

![20211001shogi2.png](../docs/img/20211001shogi2.png)  

* どの形式のファイルも、 PIVOT （中間）ファイルに変換できるものとし、また、 PIVOT から元の形式に戻せるものとします
  * ただし `.kif` ファイルは PIVOT に直接変換せず、 `.kifu` 変換を経由するものとします


## Research - 調査

### .kif

![20210929shogi7-kif.png](../docs/img/20210929shogi7-kif-50per.png)  
👆 `.kif` ファイル。 文字エンコーディングが Shift-JIS なので国際化に向きません。国産の既存のGUIで普及しています。  
**このファイルをテキストエディターで直接編集している利用者はほぼ居らず、ShogiGUIなどのソフトへ入力、出力するだけと聞きます**  

また、桁ぞろえや 前ゼロなど 表記は、 **ソフトによって異なります**  

`.kif` 形式を使っているソフトの例:  

* [柿木将棋](http://kakinoki.o.oo7.jp/) - .kif 形式のオリジナル。 しかし「変化」手順は仕様にありません
* [将棋所](http://shogidokoro.starfree.jp/)
* [Shogi GUI](http://shogigui.siganus.com/)
* [将棋ウォーズ](https://shogiwars.heroz.jp/?locale=ja)

`.kif` 形式のファイルを配布しているサイトの例:  

* [floodgate](http://wdoor.c.u-tokyo.ac.jp/shogi/floodgate.html)
* [世界コンピュータ将棋選手権](http://www2.computer-shogi.org/)
* [将棋電王トーナメント](https://denou.jp/tournament2017/)
* [世界将棋AI 電竜戦](https://denryu-sen.jp/)

### .kifu

![20210929shogi8-kifu.png](../docs/img/20210929shogi8-kifu-50per.png)  
👆 `.kifu` ファイル。 `.kif` を UTF-8 に変換したファイルです。国産の既存のGUIで普及していません。  
将棋は日本が最大のユーザー数ですから、自然、まだ普及していません  

## Proposal - 提案

一番困っているのは、これから新しく GUI や、関連ソフトを作ろうとしている新規の GUI 開発者側の人です。  
もうGUIを作った人、将棋を指す人、観る人、思考エンジンを作る人は困っていません。  

そこで 2021年現在、人気の高いプログラム言語の Python, Java Script で標準で実装されている JSON ファイル形式を  
中心に据え直し、 `.kif` へエクスポートできるアルゴリズムを Work in progress (作業中)です。  

### .json

![20211002shogi3-50per.png](../docs/img/20211002shogi3-50per.png)  
👆 `.json` ファイル。 仕様は未定

意味解析せず、 `.kif` の１行１行を **直訳** したもの。  
単一行コメントを どの行、どの文末にも置けることから、  
このコメントが上に係っているのか　下に係っているのか　機械的に判断できないため。  

また、 どのソフトから読み取った `.kif` ファイルなのか類推して情報として付加しておくと  
開発時のテストで役に立つかもしれません。  

### .toml

また、もっと ハードコアな開発者向けに、 `.toml` 形式も先行して準備します。  
コメント、文字列型、ヒアドキュメント、整数型、浮動小数点型、時刻型やリスト、連想配列など プログラマー寄りの設定ファイル形式です  

![20211002shogi4-per.png](../docs/img/20211002shogi4-per.png)  
👆 `.toml` ファイル。 仕様は未定。  
