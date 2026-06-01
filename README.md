# App — Django アプリ

Python 3.12 / Django 4.2 製の Web アプリです。  
diagnosis / roadmap / accounts / daily の 4 アプリで構成されています。

---

## 必要な環境変数

| 変数名 | 説明 | 必須 |
|---|---|---|
| `SECRET_KEY` | Django のシークレットキー（本番では必ず設定） | ✅ |
| `DEBUG` | デバッグモード（本番は `False`） | ✅ |
| `DATABASE_URL` | Railway が自動設定する PostgreSQL 接続 URL | ✅（本番） |
| `OPENAI_API_KEY` | OpenAI API キー | ✅ |

---

## Railway へのデプロイ手順

### 1. GitHub リポジトリを準備する

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

### 2. Railway でプロジェクトを作成する

1. [Railway](https://railway.app) にログイン
2. **New Project** → **Deploy from GitHub repo** を選択
3. 対象リポジトリを選択してデプロイを開始

### 3. PostgreSQL を追加する

1. プロジェクト画面で **+ New** → **Database** → **Add PostgreSQL** を選択
2. Railway が自動的に `DATABASE_URL` 環境変数をアプリに注入します

### 4. 環境変数を設定する

Railway のプロジェクト → **Variables** タブで以下を設定：

| キー | 値の例 |
|---|---|
| `SECRET_KEY` | `your-very-secret-key-here`（長くランダムな文字列） |
| `DEBUG` | `False` |
| `OPENAI_API_KEY` | `sk-...` |

> `DATABASE_URL` は PostgreSQL を追加すると自動設定されるため、手動設定不要です。

### 5. デプロイを確認する

- Railway の **Deployments** タブでビルドログを確認
- ビルドコマンド（`collectstatic` / `migrate`）が正常終了したらデプロイ完了
- 表示される URL（`*.up.railway.app`）にアクセスして動作確認

---

## ローカル開発の起動方法

### 前提

- Python 3.12
- `.env` ファイルをプロジェクトルートに配置（`.env.example` を参考に）

### セットアップ

```bash
# 仮想環境の作成と有効化
python3.12 -m venv .venv
source .venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# マイグレーション
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
```

ブラウザで http://localhost:8000 にアクセスしてください。

### スーパーユーザーの作成

```bash
python manage.py createsuperuser
```

---

## プロジェクト構成

```
App/
├── config/          # Django 設定・URL・WSGI
├── diagnosis/       # 診断アプリ
├── roadmap/         # ロードマップアプリ
├── accounts/        # 認証・アカウント管理
├── daily/           # デイリーログアプリ
├── templates/       # HTML テンプレート
├── static/          # 静的ファイル（CSS 等）
├── staticfiles/     # collectstatic の出力先（git 管理外）
├── requirements.txt
├── Procfile         # Railway / Heroku 用プロセス定義
├── railway.json     # Railway デプロイ設定
└── runtime.txt      # Python バージョン指定
```
