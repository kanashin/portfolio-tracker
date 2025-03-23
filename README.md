# 株式ポートフォリオ自動管理ツール（python × google Sheets）

## 概要

本ツールは、保有している日本、米国株の銘柄リストをもとに、
Googleスプレッドシート上に「現在値」と「損益」を自動で反映するpythonスクリプトになります。

元々、母親の資産管理を任されており、その管理を楽にするために自身の手で設計・開発しました。
プログラミング初心者の立場から、chatGPTと協力しながら、一つ一つ動く形にしていきました。

## 使用技術

 - Python 3.x
 - [yfinance](https://pypi.org/project/yfinance/)：株価データ取得
 - [gspread](https://pypi.org/project/gspread/)：Google Sheets API操作
 - pandas：データ整形・損益計算
 - oauth2client：Google認証（サービスアカウント）

## 機能概要

 - Googleスプレッドシートから銘柄一覧を読み込み
 - 全角・小文字・空白などの入力ミスを自動修正
 - 米国株／日本株のティッカーに応じて `.T` を自動付与
 - 株価APIから最新の「現在値」を取得
 - 「保有数量」と「平均取得額」から損益を自動計算
 - スプレッドシートのF列（現在値）／G列（損益）に上書き反映
 - エラー処理（取得失敗・NaN・空欄スキップ）対応済


## chatGPT活用について

本プロジェクトの開発では、OpenAIのChatGPTを活用しました。
スクリプト構造、エラー原因の特定、例外処理、コードの最適化など、AIとの対話を通して目標達成の手段を得るというプロセスを取りました。


## セットアップ
1. Google Cloud Consoleでサービスアカウントを作成し、認証ファイル（JSON）を取得
2. 対象のGoogleスプレッドシートを作成し、シート名・セル範囲を設定
3. 認証ファイルとPythonスクリプトを同じディレクトリに配置
4. 必要ライブラリをインストール：
    ```bash
    pip install -r requirements.txt
    ```
5. `portfolio_tracker.py` を実行
    ```bash
    python portfolio_tracker.py
    ```

## ファイル構成

```
portfolio-tracker/
├── portfolio_tracker.py     # メインスクリプト 
├── requirements.txt         # 使用ライブラリ一覧
├── README.md                # この説明書 
└── .gitignore               # 認証情報などの除外設定
```

## 今後の予定

 -資産グラフの可視化　（円グラフ、折れ線グラフ）
 -評価損益の通知　（Gmail,LINE）
 -ログ保存機能　（過去の記録を自動追記）
 -自動実行（Windowsタスクスケジューラ）

## 作者について

神坂 心（Kamisaka Shin）　ペンネーム｜インフラエンジニア（SES）｜創造思考 × 実現力

コード職人ではないけれど、「やりたいことをAIの力を借りて実現する」。 そんな柔軟なエンジニア像を目指しています。

## 注意点

- 認証ファイル（.json）は `.gitignore` に追加し、GitHubには絶対にアップロードしないようにしてください。

##  ご意見・ご感想

「動かしてみた！」「こういう拡張したい」などあれば、IssueやPRでお気軽にどうぞ