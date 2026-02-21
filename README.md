# Instagram自動投稿Webアプリ

ユーザー名・パスワード・投稿の詳細を入力すると、
1. AIでキャプションを生成
2. PlaywrightでInstagramにログイン
3. 画像付き投稿を実行

という流れで自動投稿を行うサンプル実装です。

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## 起動

```bash
export OPENAI_API_KEY=your_key   # 任意（未設定ならテンプレ文を生成）
export HEADLESS=true
python app.py
```

`http://localhost:8000` を開いて実行します。

## 注意

- Instagram側のUI変更・2FA・アカウント制限により失敗する場合があります。
- 本コードは学習目的のサンプルです。利用時はInstagramの規約と法令を遵守してください。
