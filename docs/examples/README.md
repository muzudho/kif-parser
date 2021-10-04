# Examples - .kifファイルの利用実態の調査

`.kif` ファイル（Shift-JIS）は文字化けして不便なので、 `.kifu` ファイル（UTF-8）に変換して説明します  

## [handmade]any-game-info.kifu

```plain
足合割：平足
説明しよう：任意の対局情報を作れるそう
キーワード１：
キーワード２：値２
キーワード３： # コメント３
キーワード４：値４ # コメント４
```

👆 対局情報を、ユーザーが任意で追加することができるとのことから、  
その解析をテストするために テキスト編集して作ったファイルです  

## [shogidokoro]20210503_191257 AI_AN_shogi_ver1 vs Kifuwarabe.kifu

第31回世界コンピュータ将棋選手権（WCSC31）に出場したした きふわらべ が用いたGUIである 将棋所 から出力した棋譜です。  

## [shogiextend-shogiwars]surokiti0510-muzudho-20211004_204159.kifu  

📖　[将棋ウォーズ棋譜検索](https://www.shogi-extend.com/swars/search)  

👆 SHOGI-EXTEND の 将棋ウォーズ棋譜検索 の `[コピー]` ボタンは `.kifu` (UTF-8) 形式のファイルをクリップボードにコピーしてくれます。  

## [shogigui]20211002_223506_KifuwarabeW31B22vsKifuwarabeW31B22.kif

ShogiGUI で WCSC31の きふわらべ を自己対局させた `.kif` ファイルを `.kifu` へ変換したものです。  

## [shogigui]bookmark.kifu

ShogiGUI で 「変化」の機能が見たくて しおり を試しに使ってみたもの。  
指し手へのコメントも複数行付けた。  

# (参考) .kif 以外の形式

📖　[CSA形式](./csa)  
