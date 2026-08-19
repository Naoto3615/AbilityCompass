# ステップアップナビ 仕様書

> 最終更新: 2026-08-19

---

## 1. サービス概要

**ステップアップナビ** は、障害を持つ方々の自立と就労・進路をサポートする Django 製 Web アプリケーションです。大きく2つのサービスを一つのシステムで提供します。

1. **就労支援サービス（大人向け）** — 障害特性の診断、就労ロードマップの提示、日常記録、AIアバターチャット機能を通じて、利用者が「自分に向いている仕事」を見つけ、就労準備を段階的に進められるよう支援します。
2. **放課後デイサービス（児童向け）** — 放課後等デイサービスに通う児童の発達・成長を記録・見える化し、支援員と保護者が連携できるプラットフォームを提供します。また、児童本人には将来の夢に向けたアドバイスを表示する専用ダッシュボードを提供します。

---

## 2. 対象ユーザーと役割

| ロール | 説明 | 使用画面 |
|---|---|---|
| **利用者（大人）** | 就労支援を受ける障害者（障害区分: 軽度・中度・その他）。診断・ロードマップ・日常記録・AIチャットを利用する。 | 診断、ロードマップ、ダッシュボード（大人）、日常記録、アバターチャット |
| **利用者（児童）** | 放課後デイに通う児童。学年・なりたい職業を設定し、専用ダッシュボードでアドバイスを受ける。 | 児童ダッシュボード |
| **支援員** | 就労支援の支援員。担当利用者の記録閲覧・AIアドバイス確認・メモ追記が可能。放課後デイの支援員も兼ねる場合は別アカウント。 | 支援員ダッシュボード（accounts）、放課後デイ支援員画面 |
| **保護者** | 放課後デイに通う児童の保護者。支援員が「共有する」フラグをオンにした支援記録のみ閲覧できる。 | 保護者ダッシュボード（daycare） |
| **管理者** | Django 管理サイト（`/admin/`）でユーザーやデータを管理する。 | Django Admin |

### 利用者種別（`user_type`）

| 値 | 表示 |
|---|---|
| `adult` | 就労を目指す大人 |
| `child` | 児童 |

---

## 3. 技術スタック

### バックエンド

| 項目 | 内容 |
|---|---|
| フレームワーク | Django（Python） |
| アプリ構成 | `diagnosis` / `roadmap` / `accounts` / `daily` / `daycare` |
| 言語設定 | `LANGUAGE_CODE = 'ja'` / `TIME_ZONE = 'Asia/Tokyo'` |
| 認証 | Django 標準認証（`django.contrib.auth`） |

### フロントエンド

| 項目 | 内容 |
|---|---|
| テンプレートエンジン | Django Templates |
| CSS フレームワーク | Tailwind CSS（推定）、インライン Tailwind クラス多用 |
| 静的ファイル配信 | WhiteNoise（`whitenoise.middleware.WhiteNoiseMiddleware`） |
| チャートライブラリ | Chart.js（週間感情グラフ、発達グラフ、レーダーチャート） |
| React アプリ | `kanji-app/`（漢字練習アプリ、別プロジェクト） |

### データベース

| 環境 | DB |
|---|---|
| 本番（Railway） | PostgreSQL（`DATABASE_URL` 環境変数が存在する場合、`dj_database_url` で接続） |
| ローカル開発 | SQLite3（`db.sqlite3`、フォールバック） |

### AI機能

| 項目 | 内容 |
|---|---|
| AI プロバイダ | OpenAI API |
| 環境変数 | `OPENAI_API_KEY` |
| 用途 | 診断結果分析（`diagnosis/services.py`）、ロードマップ生成（`roadmap/services.py`）、アバターチャット（`daily/services.py`）、支援員向けAIアドバイス（`roadmap/services.py`） |

### デプロイ

| 項目 | 内容 |
|---|---|
| プラットフォーム | Railway（`*.railway.app`、`*.up.railway.app`） |
| 本番URL（確認済み） | `https://web-production-c0abe.up.railway.app` |
| HTTPS 設定 | `SECURE_PROXY_SSL_HEADER` によるリバースプロキシ終端 |
| セキュリティ | `SESSION_COOKIE_SECURE`、`CSRF_COOKIE_SECURE`、`SECURE_HSTS_SECONDS=31536000`（本番のみ） |

---

## 4. URL一覧（画面一覧）

### グローバル

| URL | ビュー | 説明 |
|---|---|---|
| `/` | `HomeView` | トップページ |
| `/admin/` | Django Admin | 管理サイト |
| `/toggle-text-mode/` | `toggle_text_mode` | ひらがな⇔漢字モード切り替え（セッション） |

### accounts アプリ（`/accounts/`）

| URL | ビュー | 説明 |
|---|---|---|
| `/accounts/signup/` | `UserSignupView` | 利用者（大人・児童）新規登録 |
| `/accounts/signup/supporter/` | `SupporterSignupView` | 支援員新規登録 |
| `/accounts/login/` | `LoginView` | ログイン |
| `/accounts/logout/` | `logout_view` | ログアウト |
| `/accounts/dashboard/` | `SupporterDashboardView` | 支援員ダッシュボード |
| `/accounts/add-user/` | `AddSupportedUserView` | 担当利用者の追加（支援員） |
| `/accounts/avatar/` | `AvatarCreateView` | アバター作成・編集 |
| `/accounts/avatar/preview/` | `AvatarPreviewView` | アバタープレビュー（AJAX） |

### diagnosis アプリ（`/diagnosis/`）

| URL | ビュー | 説明 |
|---|---|---|
| `/diagnosis/` | `DiagnosisStartView` | 診断スタート画面 |
| `/diagnosis/questions/` | `DiagnosisQuestionsView` | 診断質問回答画面 |
| `/diagnosis/result/` | `DiagnosisResultView` | 診断結果画面 |

### roadmap アプリ（`/roadmap/`）

| URL | ビュー | 説明 |
|---|---|---|
| `/roadmap/` | `JobTypeSelectView` | 仕事タイプ選択画面 |
| `/roadmap/<job_type_key>/` | `RoadmapView` | 3ステップロードマップ表示 |

### daily アプリ（`/daily/`）

| URL | ビュー | 説明 |
|---|---|---|
| `/daily/` | `DashboardView` | 利用者（大人）ダッシュボード |
| `/daily/child/` | `child_dashboard` | 児童ダッシュボード |
| `/daily/record/` | `DailyRecordView` | 日常記録入力 |
| `/daily/chat/` | `AvatarChatView` | アバターチャット |
| `/daily/chat/clear/` | `AvatarChatClearView` | チャット履歴クリア |

### daycare アプリ（`/daycare/`）

| URL | ビュー | 説明 |
|---|---|---|
| `/daycare/staff/` | `staff_dashboard` | 支援員ダッシュボード（放課後デイ） |
| `/daycare/staff/signup/` | `staff_signup` | 支援員サインアップ（放課後デイ） |
| `/daycare/staff/children/add/` | `child_add` | 担当児童の追加 |
| `/daycare/staff/children/<id>/` | `child_detail` | 児童詳細・記録一覧 |
| `/daycare/staff/children/<id>/record/` | `record_add` | 支援記録追加 |
| `/daycare/staff/children/<id>/add-parent/` | `add_parent_to_child` | 保護者を児童に紐付け |
| `/daycare/staff/children/<id>/scores/` | `score_add` | 発達スコア記録 |
| `/daycare/children/<id>/growth/` | `child_growth` | 発達グラフ（支援員・保護者共用） |
| `/daycare/parent/` | `parent_dashboard` | 保護者ダッシュボード |
| `/daycare/parent/signup/` | `parent_signup` | 保護者サインアップ |

---

## 5. データモデル一覧

### accounts アプリ

#### `UserProfile`（就労支援利用者プロフィール）

| フィールド | 型 | 説明 |
|---|---|---|
| `user` | OneToOneField(User) | Django標準ユーザーと1対1紐付け |
| `nickname` | CharField(30) | ニックネーム |
| `disability_level` | CharField | 障害区分（`mild`/`moderate`/`other`） |
| `avatar_emoji` | CharField(10) | アバター絵文字（デフォルト: 🌟） |
| `avatar_config` | JSONField | アバター外見設定（JSON） |
| `supporter` | ForeignKey(SupporterProfile) | 担当支援員（NULL可） |
| `user_type` | CharField | 利用者種別（`adult`/`child`） |
| `grade` | CharField | 学年区分（児童のみ。`elementary_low`/`elementary_high`/`junior_high`/`high_school`） |
| `desired_career` | CharField | なりたい職業（児童のみ） |
| `created_at` | DateTimeField | 作成日時 |

#### `SupporterProfile`（支援員プロフィール）

| フィールド | 型 | 説明 |
|---|---|---|
| `user` | OneToOneField(User) | Django標準ユーザーと1対1紐付け |
| `created_at` | DateTimeField | 作成日時 |

#### `SupporterNote`（支援員メモ）

| フィールド | 型 | 説明 |
|---|---|---|
| `supporter` | ForeignKey(User) | メモを書いた支援員 |
| `target_user` | ForeignKey(User) | メモの対象ユーザー |
| `content` | TextField | メモ内容 |
| `created_at` | DateTimeField | 作成日時（降順ソート） |

---

### daily アプリ

#### `DailyRecord`（日々の記録）

| フィールド | 型 | 説明 |
|---|---|---|
| `user` | ForeignKey(User) | 記録者 |
| `date` | DateField | 記録日（デフォルト: 今日、ユーザー×日付でユニーク） |
| `did_well` | TextField | できたこと |
| `struggled_with` | TextField | むずかしかったこと |
| `emotion_stamp` | IntegerField | 気持ちスタンプ（1〜5。1=とてもつらい〜5=とてもよい） |
| `health_score` | IntegerField | からだのようす（1〜3。1=つらい〜3=からだがよい） |
| `created_at` | DateTimeField | 作成日時 |

#### `AvatarChatMessage`（アバターチャット履歴）

| フィールド | 型 | 説明 |
|---|---|---|
| `profile` | ForeignKey(UserProfile) | チャットを行ったユーザープロフィール |
| `role` | CharField(10) | メッセージの送信者（`user` または `avatar`） |
| `content` | TextField | メッセージ本文 |
| `created_at` | DateTimeField | 送信日時（昇順ソート） |

---

### diagnosis アプリ

#### `DiagnosisSession`（診断セッション）

| フィールド | 型 | 説明 |
|---|---|---|
| `session_key` | CharField(100) | セッション識別キー（UUID、ユニーク） |
| `answers` | TextField | 回答データ（JSON文字列） |
| `focus_score` | IntegerField | 集中力スコア（0〜50程度） |
| `communication_score` | IntegerField | コミュニケーション力スコア |
| `endurance_score` | IntegerField | 体力・持続力スコア |
| `accuracy_score` | IntegerField | 几帳面さ・正確性スコア |
| `emotion_control_score` | IntegerField | 感情コントロールスコア |
| `learning_score` | IntegerField | 学習意欲・変化への適応スコア |
| `job_type` | CharField | 向いている仕事タイプ |
| `result_strengths` | TextField | 強み一覧（JSON） |
| `result_challenges` | TextField | 課題一覧（JSON） |
| `result_summary` | TextField | 診断サマリ文（JSON or プレーンテキスト） |
| `created_at` | DateTimeField | 作成日時 |

---

### roadmap アプリ

#### `GrowthStep`（就労ステップタスク）

| フィールド | 型 | 説明 |
|---|---|---|
| `user` | ForeignKey(User) | 対象ユーザー（NULL可） |
| `session_key` | CharField(100) | 非ログイン時のセッションキー |
| `step_number` | IntegerField | ステップ番号（1/2/3） |
| `job_type` | CharField | 仕事タイプ |
| `category` | CharField(50) | カテゴリ名 |
| `content` | TextField | タスク内容 |
| `daily_action` | TextField | 今日できる小さな行動 |
| `is_completed` | BooleanField | 完了フラグ |
| `completed_at` | DateTimeField | 完了日時（NULL可） |
| `created_at` | DateTimeField | 作成日時 |

#### `RoadmapCache`（AIロードマップキャッシュ）

| フィールド | 型 | 説明 |
|---|---|---|
| `job_type` | CharField | 仕事タイプ（ユニーク） |
| `content` | TextField | AIが生成したロードマップ内容（JSON） |
| `created_at` | DateTimeField | 作成日時 |

---

### daycare アプリ

#### `Child`（児童）

| フィールド | 型 | 説明 |
|---|---|---|
| `nickname` | CharField(50) | ニックネーム |
| `notes` | TextField | 特記事項（任意） |
| `created_at` | DateTimeField | 作成日時 |

#### `StaffProfile`（放課後デイ支援員プロフィール）

| フィールド | 型 | 説明 |
|---|---|---|
| `user` | OneToOneField(User) | Django標準ユーザーと1対1紐付け |
| `created_at` | DateTimeField | 作成日時 |

#### `StaffChildLink`（支援員〜児童 中間テーブル）

| フィールド | 型 | 説明 |
|---|---|---|
| `staff` | ForeignKey(StaffProfile) | 支援員 |
| `child` | ForeignKey(Child) | 担当児童（ユニーク制約: staff×child） |

#### `ParentProfile`（保護者プロフィール）

| フィールド | 型 | 説明 |
|---|---|---|
| `user` | OneToOneField(User) | Django標準ユーザーと1対1紐付け |
| `created_at` | DateTimeField | 作成日時 |

#### `ParentChildLink`（保護者〜児童 中間テーブル）

| フィールド | 型 | 説明 |
|---|---|---|
| `parent` | ForeignKey(ParentProfile) | 保護者 |
| `child` | ForeignKey(Child) | 対象児童（ユニーク制約: parent×child） |

#### `SupportRecord`（支援記録）

| フィールド | 型 | 説明 |
|---|---|---|
| `child` | ForeignKey(Child) | 対象児童 |
| `author` | ForeignKey(User) | 記録者（支援員） |
| `date` | DateField | 記録日 |
| `content` | TextField | 支援記録本文 |
| `achievement` | TextField | 今日のできた！（任意） |
| `share_with_parent` | BooleanField | 保護者への共有フラグ（デフォルト: False） |
| `created_at` | DateTimeField | 作成日時 |

#### `DevelopmentScore`（発達スコア）

| フィールド | 型 | 説明 |
|---|---|---|
| `child` | ForeignKey(Child) | 対象児童 |
| `author` | ForeignKey(User) | 記録者（支援員） |
| `date` | DateField | 記録日 |
| `focus` | IntegerField(1〜5) | 集中力スコア |
| `communication` | IntegerField(1〜5) | コミュニケーションスコア |
| `daily_living` | IntegerField(1〜5) | 生活習慣スコア |
| `social` | IntegerField(1〜5) | 社会性スコア |
| `motor` | IntegerField(1〜5) | 運動・身体スコア |
| `memo` | TextField | メモ（任意） |

---

## 6. 機能詳細

### 6.1 認証・ユーザー管理

- **利用者登録** (`/accounts/signup/`): ニックネーム、ユーザー名、パスワード、障害区分、利用者種別（大人/児童）、学年（児童のみ）を入力。登録後、ロールに応じてダッシュボードへリダイレクト。
- **支援員登録** (`/accounts/signup/supporter/`): ユーザー名、パスワード、担当利用者のユーザー名（任意）を入力。登録後、担当利用者の `supporter` フィールドを更新。
- **ログイン** (`/accounts/login/`): ロール別（利用者大人/児童/支援員/放課後デイ支援員/保護者）に適切なダッシュボードへリダイレクト。エラーメッセージはテキストモードに応じてひらがな/漢字で表示。
- **担当利用者の追加** (`/accounts/add-user/`): 支援員がログイン後、ユーザー名を指定して後から担当利用者を追加できる。
- **支援員ダッシュボード** (`/accounts/dashboard/`): 担当利用者ごとに7日間の感情トレンドグラフ、平均感情スコア、最新記録3件、AIアドバイス、支援員メモを表示。支援員メモのPOSTにより新規メモを追加できる。

### 6.2 診断機能

- **診断スタート** (`/diagnosis/`): セッションキー（UUID）を発行してセッションに保存し、質問画面へ遷移。
- **質問回答** (`/diagnosis/questions/`): 6特性（集中力・コミュニケーション力・体力持続力・几帳面さ正確性・感情コントロール・学習意欲変化への適応）に関する複数の質問を1〜5点で回答。すべての質問への回答が必須で、未回答があるとエラーを表示。
- **結果分析** (`/diagnosis/result/`): 回答データを OpenAI API（`diagnosis/services.py`の `analyze_with_ai`）に送信し、6特性スコア・仕事タイプ・強み・課題・サマリを取得。セッション（`DiagnosisSession`）に保存。ログインユーザーのアバター設定（仕事アウトフィット、表情、アクセサリー）を診断結果に基づいて自動更新。
- **結果表示**: 6特性のレーダーチャート（Chart.js）、向いている仕事タイプ、強み・課題一覧、AI生成サマリを表示。ログインユーザーにはアバターも表示し、未アバター設定の場合はアバター作成を促す。
- **ゲストでも利用可能**: ログインなしでも診断可能（セッションキーで管理）。

#### 診断質問一覧（`DIAGNOSIS_QUESTIONS`）

全13問。各質問は `id`（q1〜q13）、`category`（特性キー）、漢字・ひらがな両対応の `text` を持つ。

| id | category | 質問（漢字） |
|---|---|---|
| q1 | focus | 同じ作業をずっとくりかえすことができる |
| q2 | focus | 好きな作業は時間を忘れて一生懸命できる |
| q3 | focus | 最後まであきらめずに作業を続けられる |
| q4 | communication | わからないとき「わかりません」と言える |
| q5 | communication | 「おはようございます」「ありがとうございます」のあいさつができる |
| q6 | endurance | 体を動かす仕事が好き |
| q7 | endurance | 1日中立って仕事をしても疲れにくい |
| q8 | accuracy | ものをきれいに並べたり整理することが好き |
| q9 | accuracy | まちがいを見つけることや丁寧にやることが得意 |
| q10 | emotion_control | うまくできないとき、落ち着いてやり直せる |
| q11 | emotion_control | 予定が変わっても、パニックになりにくい |
| q12 | learning | 新しいことを教えてもらうのが好き |
| q13 | learning | できないことができるようになると嬉しい |

#### 回答スコアラベル（`SCORE_LABELS`）

| 値 | 漢字ラベル | ひらがなラベル | 絵文字 |
|---|---|---|---|
| 1 | 全然あてはまらない | ぜんぜん　あてはまらない | 😔 |
| 2 | あまりあてはまらない | あまり　あてはまらない | 🤔 |
| 3 | どちらとも言えない | どちらとも　いえない | 😐 |
| 4 | 少しあてはまる | すこし　あてはまる | 🙂 |
| 5 | とてもあてはまる | とても　あてはまる | 😊 |

#### スコア計算ロジック（`_calc_trait_scores`）

各特性カテゴリに属する質問の回答値を**平均**し、1.0〜5.0 の小数スコアを算出する（`round(..., 1)`）。

`DiagnosisSession` に保存する際は `×10`（整数: 0〜50）に変換する。

#### 仕事タイプ判定ロジック（`_determine_job_type`）

各仕事タイプに対して下記重み付け合計を計算し、最大のものを選択する。

| 仕事タイプ | 計算式 |
|---|---|
| agriculture | endurance × 0.4 + focus × 0.3 + emotion_control × 0.3 |
| manufacturing | focus × 0.4 + accuracy × 0.4 + endurance × 0.2 |
| cleaning | endurance × 0.4 + accuracy × 0.3 + focus × 0.3 |
| food_processing | accuracy × 0.4 + focus × 0.3 + endurance × 0.3 |
| service | communication × 0.4 + emotion_control × 0.3 + learning × 0.3 |

#### AI分析の仕様（`analyze_with_ai`）

- モデル: `gpt-4o-mini`、`temperature=0.7`、`response_format={"type": "json_object"}`
- 返却 JSON スキーマ: `strengths`（2件）、`challenges`（2件）、`job_type`、`summary`（80文字以内の励まし文）
- 強み・課題の各要素: `trait`（特性キー）、`title`（10文字以内）、`description`（40文字以内）、`emoji`
- OpenAI API 失敗時は `_fallback_analysis`（静的データ）を使用

#### 診断結果とアバターの連動（`_apply_diagnosis_to_avatar`）

診断完了後（ログインユーザーのみ）、アバター設定を以下ルールで自動更新する。

| 条件 | 更新内容 |
|---|---|
| 常に | `job_outfit` を仕事タイプに対応する値に更新（下表参照） |
| endurance 平均スコア ≥ 3.5 | `expression='happy'`、`rosy_cheeks=True` |
| communication 平均スコア ≥ 3.5（上記に非該当） | `expression='happy'`、`rosy_cheeks=False` |
| 上記のいずれにも非該当 | `expression` はユーザー設定を維持、`rosy_cheeks=False` |
| focus 平均スコア ≥ 3.5 かつ `accessory='none'` | `accessory='glasses'` |

**`job_outfit` の値一覧**

| 仕事タイプキー | job_outfit 値 |
|---|---|
| agriculture | farming |
| manufacturing | manufacturing |
| cleaning | cleaning |
| food_processing | food |
| service | retail |
| （未マッチ） | none |

#### 仕事タイプ一覧

| キー | 表示 |
|---|---|
| `agriculture` | 🌱 農業・園芸系 |
| `manufacturing` | 🔧 製造・組み立て系 |
| `cleaning` | 🧹 清掃・環境整備系 |
| `food_processing` | 🍱 食品加工系 |
| `service` | 🛒 接客・販売補助系 |

### 6.3 ロードマップ機能

- **仕事タイプ選択** (`/roadmap/`): 診断で決定した仕事タイプを確認・選択できる。診断後にセッションへ保存された `diagnosis_job_type` を候補として表示。
- **3ステップロードマップ** (`/roadmap/<job_type_key>/`): 選択した仕事タイプに対する3段階のロードマップを表示。
- ロードマップデータは `RoadmapCache` テーブルにキャッシュされ、未キャッシュ時は `get_job_roadmap`（AIまたは静的データ）で生成。

#### ステップ定義（`STEP_DEFINITIONS`）

| ステップ | テーマ（漢字） | 絵文字 | 色 | 説明（漢字） |
|---|---|---|---|---|
| 1 | 生活習慣・基本スキル | 🌱 | green | 働く前に、まず毎日の生活を整えよう |
| 2 | 作業スキル | 🔧 | blue | 指示どおりに動けるよう、くりかえし練習しよう |
| 3 | 就労準備 | 🚀 | orange | 実際の仕事に近い体験をしてみよう |

#### タスク構造

各ステップは複数のタスクと励ましメッセージを持つ。タスクは以下のフィールドから成る。

| フィールド | 説明 |
|---|---|
| category | カテゴリ名（例: 生活習慣、あいさつ、作業練習） |
| content | タスク内容（30文字以内） |
| daily_action | 今日できる小さな行動（40文字以内） |

各仕事タイプのタスク数の目安: ステップ1=4件、ステップ2=4件、ステップ3=3件。

#### AI生成の仕様（`_generate_with_ai`）

- モデル: `gpt-4o-mini`、`temperature=0.7`、`response_format={"type": "json_object"}`
- 返却 JSON スキーマ: `step1` / `step2` / `step3`（各 `tasks` 配列＋`message` 文字列）
- OpenAI API 失敗時は `_fallback_roadmap`（`ROADMAP_DATA` 静的データ）を使用

#### 支援員向けAIアドバイスの仕様（`get_supporter_advice`）

- モデル: `gpt-4o-mini`、`temperature=0.7`、`max_tokens=200`
- 過去最大7件の `DailyRecord` を入力（日付・感情・からだのようす・できたことの冒頭30文字）
- OpenAI API 失敗時は感情スコアに基づく静的フォールバックを使用（記録なし / 最新が4以上 / 最新が2以下 / それ以外）

### 6.4 日常記録・ダッシュボード（大人向け）

- **ダッシュボード** (`/daily/`): 今日の記録状況、過去7日間の感情トレンドグラフ（Chart.js）、記録日数バッジを表示。アバターの表情が当日の感情スタンプに連動して変化（4以上→happy、2以下→worried、それ以外→normal）。バッジカウントは総記録日数に連動。
- **日常記録入力** (`/daily/record/`): 当日の「できたこと」「むずかしかったこと」「気持ちスタンプ（1〜5）」「からだのようす（1〜3）」を入力。`update_or_create` により同日の再入力にも対応。

#### 気持ちスタンプ一覧

| 値 | 絵文字 | ラベル | カラー |
|---|---|---|---|
| 5 | 😄 | とてもよい | `#fde68a` |
| 4 | 😊 | まあまあ | `#86efac` |
| 3 | 😐 | ふつう | `#d1d5db` |
| 2 | 😟 | すこしつらい | `#a5b4fc` |
| 1 | 😢 | とてもつらい | `#93c5fd` |

### 6.5 児童向けダッシュボード

- **児童ダッシュボード** (`/daily/child/`): `user_type == 'child'` のユーザー専用。学年（`grade`）となりたい職業（`desired_career`）の組み合わせに応じて `CHILD_ADVICE` データから4件のアドバイスを表示。
- POSTで `desired_career` を更新可能。
- テキストモードに応じて漢字・ひらがな表示を切り替え（デフォルト: `kanji`）。

#### 対応学年

| 値 | 表示 |
|---|---|
| `elementary_low` | 小学生（低学年） |
| `elementary_high` | 小学生（高学年） |
| `junior_high` | 中学生 |
| `high_school` | 高校生 |

#### 対応職業

| 値 | 絵文字 | 表示 |
|---|---|---|
| `doctor` | 🏥 | 医師・看護師 |
| `teacher` | 📚 | 先生・保育士 |
| `engineer` | 💻 | エンジニア・プログラマー |
| `artist` | 🎨 | 絵・デザイン・音楽 |
| `sports` | ⚽ | スポーツ選手 |
| `chef` | 🍳 | 料理人・パティシエ |
| `police` | 🚔 | 警察官・消防士 |
| `vet` | 🐾 | 獣医・動物関係 |
| `other` | 🌟 | まだ決まっていない |

### 6.6 アバター機能

- **アバター作成** (`/accounts/avatar/`): SVGベースのカスタムアバターを作成・編集。以下のパーツをカスタマイズ可能。

| パーツキー | 選択肢（value: ラベル） |
|---|---|
| skin（肌色） | light: ライト / medium: ミディアム / dark: ダーク |
| hair_style（髪型） | short: ショート / long: ロング / curly: くるくる / none: なし |
| hair_color（髪色） | black: くろ / brown: ちゃいろ / blonde: きいろ / gray: グレー |
| eye_type（目） | normal: ふつう / round: まるい / happy: わらい |
| expression（表情） | happy: えがお / normal: ふつう / worried: しんぱい |
| accessory（アクセサリー） | none: なし / glasses: めがね |

- **プレビュー** (`/accounts/avatar/preview/`): GET パラメータを受け取り、SVG HTML をリアルタイムで返す AJAX エンドポイント。
- **アバター設定（`avatar_config` JSON）のデフォルト値**（`DEFAULT_AVATAR_CONFIG`）:

```json
{
  "skin": "light",
  "hair_style": "short",
  "hair_color": "black",
  "eye_type": "normal",
  "accessory": "none",
  "job_outfit": "none",
  "expression": "happy",
  "badge_count": 0,
  "rosy_cheeks": false
}
```

- **アバター作成画面で変更できるフィールド**: `skin` / `hair_style` / `hair_color` / `eye_type` / `expression` / `accessory`（6項目）。`job_outfit`、`badge_count`、`rosy_cheeks` はアバター作成画面では変更できない。
- **診断結果との連動**: 診断後に `job_outfit`（仕事コスチューム）、`expression`、`rosy_cheeks`、`accessory` が自動更新される（詳細は 6.2 節参照）。
- **ダッシュボードとの連動**: 当日の感情スタンプに応じてアバターの表情が変化する（感情スタンプ ≥ 4 → happy、≤ 2 → worried、それ以外 → normal）。なお、この表情変化はダッシュボード表示時のみ一時的に適用され、`avatar_config` を上書き保存しない。
- **`badge_count` の算出**: ダッシュボード表示時にログインユーザーの総 `DailyRecord` 件数を取得してリアルタイムで設定される（`avatar_config` への保存は行わない）。
- **SVGテンプレートの依存**: アバター描画は `templates/components/avatar.html` の SVG テンプレートに依存。スキンカラーは `SKIN_COLORS`、髪色は `HAIR_COLORS`（`diagnosis/templatetags/text_mode.py` に定義）から取得する。

### 6.7 AIチャット機能

- **アバターチャット** (`/daily/chat/`): 利用者が自分のアバターとテキストチャットできる。過去30件のチャット履歴を表示。
- POST リクエスト（JSON）でユーザーメッセージを送信 → `daily/services.py` の `chat_with_avatar` 関数が OpenAI API を使ってアバターの返信を生成 → `AvatarChatMessage` に `role='user'` と `role='avatar'` の両メッセージを保存し、返信をJSONで返す。
- テキストモード（ひらがな/漢字）に応じてアバターの返答スタイルが変わる。
- **履歴クリア** (`/daily/chat/clear/`): POSTで当該ユーザーの全チャット履歴を削除。
- **支援員へのAIアドバイス**: 支援員ダッシュボードでは、担当利用者のプロフィールと直近の記録を基に `daily/services.py` の `get_supporter_advice` 関数がAIアドバイスを生成して表示する（`roadmap/services.py` にも同名の関数が存在する）。

#### アバターチャットAIの仕様（`chat_with_avatar`）

- モデル: `gpt-4o-mini`、`temperature=0.8`、`max_tokens=300`
- APIに送るコンテキスト: システムプロンプト（利用者プロフィール・仕事タイプ・強み・課題を反映）＋直近10件のチャット履歴
- `OPENAI_API_KEY` 未設定時または例外発生時はキーワードマッチングによるルールベースフォールバックを使用
- フォールバックキーワードパターン: つかれた系 / できた系 / むずかしい系 / ふあん系 / たのしい系（各パターンに hiragana / kanji 応答を用意）
- アバターのシステムプロンプトは `get_avatar_system_prompt`（`daily/services.py`）で生成。最新の `DiagnosisSession` から仕事タイプ・強み・課題を取得し、text_mode に応じた話し方を指示する。

### 6.8 放課後デイサービス機能（支援員・保護者）

#### 支援員向け

- **支援員ダッシュボード** (`/daycare/staff/`): 担当児童の一覧と、各児童の最新支援記録・本日の記録有無を表示。
- **担当児童追加** (`/daycare/staff/children/add/`): 既存の `Child` レコードから未担当の児童を選択して担当に追加（`StaffChildLink` を作成）。
- **児童詳細** (`/daycare/staff/children/<id>/`): 対象児童の全支援記録と紐付き保護者一覧を表示。
- **支援記録追加** (`/daycare/staff/children/<id>/record/`): `SupportRecord` を作成。「今日のできた！」フィールドと保護者共有フラグを含む。
- **保護者紐付け** (`/daycare/staff/children/<id>/add-parent/`): 既存の `ParentProfile` を対象児童に紐付け（`ParentChildLink` を作成）。
- **発達スコア記録** (`/daycare/staff/children/<id>/scores/`): `DevelopmentScore`（集中力・コミュニケーション・生活習慣・社会性・運動身体、各1〜5点）を記録。

#### 保護者向け

- **保護者ダッシュボード** (`/daycare/parent/`): 紐付き児童の支援記録のうち、`share_with_parent=True` のもの最新10件を表示。

#### 共通

- **発達グラフ** (`/daycare/children/<id>/growth/`): `DevelopmentScore` の時系列データを Chart.js の折れ線グラフとレーダーチャートで可視化。支援員・保護者どちらも閲覧可能（それぞれ担当・紐付き関係がある場合のみ）。

### 6.9 ひらがな切り替え機能

- URL `/toggle-text-mode/` にアクセスすることで、セッションの `text_mode` が `hiragana` ⇔ `kanji` に切り替わる。切り替え後は元のページ（`HTTP_REFERER`）へリダイレクト。
- `hiragana` モード（大人向けビューのデフォルト）では、テンプレート内のテキストやフォームラベル、エラーメッセージをひらがな表記に変更。
- 診断質問・選択肢、ロードマップ内容、アドバイス内容などで `resolve_data` 関数を通じてバイリンガル辞書（`{kanji: ..., hiragana: ...}`）から適切なテキストを返す。
- **児童ダッシュボード**（`/daily/child/`）では `text_mode` のセッション値を読むが、デフォルトは `kanji`（`request.session.get('text_mode', 'kanji')`）。
- 就労支援系（大人向け）ビューのデフォルトは `hiragana`。

### 6.10 セッション変数一覧

| キー | 型 | 設定タイミング | 説明 |
|---|---|---|---|
| `text_mode` | str | `/toggle-text-mode/` アクセス時 | `hiragana` または `kanji`。大人向けデフォルト: `hiragana`、児童ダッシュボードデフォルト: `kanji` |
| `diagnosis_session_key` | str (UUID) | 診断スタート POST 時 | 診断セッションの識別キー。`DiagnosisSession.session_key` に対応 |
| `diagnosis_job_type` | str | 診断回答 POST 完了時 | 診断で判定された仕事タイプキー（例: `agriculture`）。ロードマップ選択画面で候補表示に使用 |

---

## 6.11 フォームバリデーション仕様

### `UserSignupForm`（`accounts/forms.py`）

| フィールド | バリデーション |
|---|---|
| nickname | 必須。max_length=30 |
| username | 必須。Django 標準の `UserCreationForm` ルール（英数字・記号） |
| password1 / password2 | 必須。Django 標準パスワードバリデーション |
| user_type | 必須。`adult` または `child` |
| grade | `user_type='child'` の場合は必須（`clean()` でクロスバリデーション） |

- フォーム初期化時に `text_mode` を受け取り、ひらがな/漢字でエラーメッセージを切り替える。
- バリデーション成功時に `UserProfile` を自動作成（`save()` 内）。

### `SupporterSignupForm`（`accounts/forms.py`）

| フィールド | バリデーション |
|---|---|
| username | 必須 |
| password1 / password2 | 必須 |
| target_username | 任意。入力された場合: ① ユーザーの存在確認、② `user_profile` を持つ利用者か確認 |

### `AddSupportedUserForm`（`accounts/forms.py`）

| フィールド | バリデーション |
|---|---|
| target_username | 必須。ユーザーの存在確認 + `user_profile` を持つ利用者か確認 |

### `AddParentForm`（`daycare/forms.py`）

| フィールド | バリデーション |
|---|---|
| username | 必須。ユーザーの存在確認 + `parent_profile` を持つ保護者か確認 |

### `SupportRecordForm`（`daycare/forms.py`）

| フィールド | 必須 | 説明 |
|---|---|---|
| date | 必須 | 記録日（`<input type="date">`） |
| content | 必須 | 支援内容（テキストエリア） |
| achievement | 任意 | 今日のできた！ |
| share_with_parent | 任意 | 保護者共有フラグ（チェックボックス） |

### `DevelopmentScoreForm`（`daycare/forms.py`）

| フィールド | 必須 | 説明 |
|---|---|---|
| date | 必須 | 記録日 |
| focus | 必須 | 集中力（1〜5、RadioSelect） |
| communication | 必須 | コミュニケーション（1〜5、RadioSelect） |
| daily_living | 必須 | 生活習慣（1〜5、RadioSelect） |
| social | 必須 | 社会性（1〜5、RadioSelect） |
| motor | 必須 | 運動・身体（1〜5、RadioSelect） |
| memo | 任意 | メモ |

---

## 7. 画面フロー

### 利用者（大人）のフロー

```
トップ (/)
  └─ [未登録] → 利用者登録 (/accounts/signup/)
  └─ [登録済み] → ログイン (/accounts/login/)
       └─ ダッシュボード (/daily/)
            ├─ 日常記録入力 (/daily/record/) → ダッシュボードへ戻る
            ├─ アバターチャット (/daily/chat/)
            ├─ アバター作成 (/accounts/avatar/)
            ├─ 診断スタート (/diagnosis/)
            │    └─ 質問回答 (/diagnosis/questions/)
            │         └─ 診断結果 (/diagnosis/result/)
            │              └─ ロードマップ選択 (/roadmap/)
            │                   └─ ロードマップ表示 (/roadmap/<job_type_key>/)
            └─ ログアウト (/accounts/logout/)
```

### 利用者（児童）のフロー

```
トップ (/)
  └─ 利用者登録（user_type=child） (/accounts/signup/)
  └─ ログイン (/accounts/login/)
       └─ 児童ダッシュボード (/daily/child/)
            ├─ なりたい職業を選択・更新 → 同画面更新
            └─ ログアウト (/accounts/logout/)
```

### 支援員（就労支援）のフロー

```
トップ (/)
  └─ 支援員登録 (/accounts/signup/supporter/)
  └─ ログイン (/accounts/login/)
       └─ 支援員ダッシュボード (/accounts/dashboard/)
            ├─ メモ追加（POST）
            └─ 担当利用者追加 (/accounts/add-user/)
```

### 支援員（放課後デイ）のフロー

```
支援員登録 (/daycare/staff/signup/)
  └─ 支援員ダッシュボード (/daycare/staff/)
       ├─ 担当児童追加 (/daycare/staff/children/add/)
       ├─ 児童詳細 (/daycare/staff/children/<id>/)
       │    ├─ 支援記録追加 (/daycare/staff/children/<id>/record/)
       │    └─ 保護者紐付け (/daycare/staff/children/<id>/add-parent/)
       ├─ 発達スコア記録 (/daycare/staff/children/<id>/scores/)
       └─ 発達グラフ閲覧 (/daycare/children/<id>/growth/)
```

### 保護者のフロー

```
保護者登録 (/daycare/parent/signup/)
  └─ 保護者ダッシュボード (/daycare/parent/)
       └─ 発達グラフ閲覧 (/daycare/children/<id>/growth/)
            ※ 支援員が「保護者に共有する」フラグをオンにした記録のみ閲覧可
```

---

## 8. 環境変数

| 変数名 | 必須 | 説明 |
|---|---|---|
| `SECRET_KEY` | 本番では必須 | Django シークレットキー。未設定時は起動ごとにランダム生成（本番では必ず設定すること） |
| `DEBUG` | 任意 | `True` でデバッグモード（デフォルト: `False`） |
| `DATABASE_URL` | 本番では必須 | PostgreSQL 接続URL。未設定時は SQLite3 にフォールバック |
| `OPENAI_API_KEY` | AI機能を使う場合は必須 | OpenAI API キー |

---

## 9. 管理画面（Django Admin）

Django 標準の管理サイト（`/admin/`）から以下のモデルを操作できる。

### accounts アプリ

| モデル | 登録方法 | 備考 |
|---|---|---|
| UserProfile | `admin.site.register` | 一覧・編集 |
| SupporterProfile | `admin.site.register` | 一覧・編集 |
| SupporterNote | `admin.site.register` | 一覧・編集 |

### diagnosis アプリ

| モデル | 登録方法 | 備考 |
|---|---|---|
| DiagnosisSession | `admin.site.register` | 一覧・編集 |

### roadmap アプリ

| モデル | 登録方法 | 備考 |
|---|---|---|
| GrowthStep | `admin.site.register` | 一覧・編集 |
| RoadmapCache | `admin.site.register` | 一覧・編集（キャッシュの手動削除はここから行う） |

### daily アプリ

| モデル | 登録方法 | 備考 |
|---|---|---|
| DailyRecord | `admin.site.register` | 一覧・編集 |

### daycare アプリ

| モデル | カスタム `ModelAdmin` | list_display / list_filter / search_fields |
|---|---|---|
| Child | ChildAdmin | nickname, created_at / search: nickname |
| SupportRecord | SupportRecordAdmin | child, author, date, share_with_parent / filter: share_with_parent, date / search: child__nickname, content |
| DevelopmentScore | DevelopmentScoreAdmin | child, author, date, focus, communication, social / filter: date |
| StaffProfile | StaffProfileAdmin | user, created_at |
| ParentProfile | ParentProfileAdmin | user, created_at |
| StaffChildLink | StaffChildLinkAdmin | staff, child |
| ParentChildLink | ParentChildLinkAdmin | parent, child |

---

## 10. 既知の制限・今後の課題

1. **`Child` モデルの作成画面が未実装**: `child_form.html` テンプレートと `ChildForm` は存在するが、`Child` を新規作成するビューがURLに登録されていない。現状、`child_add` ビューは既存の `Child` を担当に追加するのみ。
2. **診断機能のゲスト利用制限**: `DiagnosisSession` はセッションキーで管理されるが、ユーザーアカウントと紐付かないため、ログアウト後に診断結果を参照できない。
3. **`GrowthStep` モデルの未活用**: ロードマップアプリに `GrowthStep`（タスク完了管理）モデルが定義されているが、現行ビューはロードマップデータの表示のみでタスク完了を永続化する機能が実装されていない。
4. **`RoadmapCache` の更新ロジック**: キャッシュが一度作成されると更新されないため、AIが生成したロードマップ内容が陳腐化する可能性がある。
5. **`accounts` と `daycare` の支援員アカウント分離**: 就労支援の支援員（`SupporterProfile`）と放課後デイの支援員（`StaffProfile`）は別テーブルで管理されており、同一ユーザーが両方の役割を持つことを想定していない。
6. **テキストモードのデフォルト不統一**: 就労支援系（大人向け）は `hiragana` がデフォルト、児童向けダッシュボードは `kanji` がデフォルトと、画面によって異なる。
7. **アバターの SVG テンプレートの依存**: アバター描画は `templates/components/avatar.html` の SVG テンプレートに依存しており、スキン・髪型・表情などのバリエーションは `diagnosis/templatetags/text_mode.py` の `SKIN_COLORS` / `HAIR_COLORS` 定数と連動している。
8. **チャット履歴のAPIコンテキスト制限**: アバターチャットはページ表示では最新30件を表示するが、OpenAI APIへ送るコンテキストは最新10件に限定される。長い会話では初期の文脈がアバターに届かない。
9. **`AvatarChatMessage` の `role` 値と変換**: モデル上の `role` は `user` または `avatar`。OpenAI API へ送る際は `user`→`user`、`avatar`→`assistant` に変換される。
10. **支援員ダッシュボードのメモ表示上限**: `SupporterNote` は対象ユーザーごとに最新3件のみダッシュボードに表示される（`[:3]`）。
11. ~~**`get_supporter_advice` の重複定義**~~ **（修正済み）**: `daily/services.py` の未使用の重複定義を削除。`roadmap/services.py` の版を正規実装として維持。あわせて同関数のフォールバック処理で `daily_records[0]`（最古）を参照していたバグを `daily_records[-1]`（最新）に修正。
12. **児童アドバイスデータの静的管理**: `daily/child_advice.py` の `CHILD_ADVICE` は4学年×9職業=36パターンを静的Pythonデータとして保持している。AIによる動的生成は行われない。

---

## 11. AI使用箇所 vs ハードコード（ルールベース）一覧

アプリの各機能における実装方式を以下の区分で整理します：

| 記号 | 意味 |
|---|---|
| 🤖 AI | OpenAI API（GPT-4o-mini / text-embedding-3-small）を使用 |
| 🔧 ハードコード | Pythonコード内に固定データとして記述 |
| 🗄️ DB管理 | Django Admin（管理画面）から追加・編集可能なDBデータ |
| 📐 ルールベース | コード内の条件分岐・スコア計算などのロジック |

### 11.1 診断機能

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| 診断質問13問 | 🔧 ハードコード | `diagnosis/services.py` の `DIAGNOSIS_QUESTIONS` リスト |
| 回答スコアラベル（1〜5） | 🔧 ハードコード | `SCORE_LABELS`, `SCORE_EMOJIS` |
| 特性ラベル（6特性の名前・説明） | 🔧 ハードコード | `TRAIT_LABELS` 辞書 |
| 仕事タイプ定義（5種） | 🔧 ハードコード | `JOB_TYPES` リスト（キー・名前・絵文字・説明・色） |
| 特性スコア計算（6特性） | 📐 ルールベース | カテゴリ別の平均計算。`_calc_trait_scores()` |
| 仕事タイプ判定 | 📐 ルールベース | 特性スコアへの重み付け計算。`_determine_job_type()` |
| 強み・課題の生成 | 🤖 AI（フォールバック: 🔧） | `analyze_with_ai()` → OpenAI API（gpt-4o-mini）。失敗時は `_fallback_analysis()` のハードコードデータで代替 |
| 診断サマリー文 | 🤖 AI（フォールバック: 🔧） | OpenAI APIで生成。失敗時は仕事タイプ別固定文（`job_type_messages`） |
| アバター自動更新 | 📐 ルールベース | 診断後に `_apply_diagnosis_to_avatar()` でスコアに基づき表情・服装を決定 |

### 11.2 ロードマップ機能

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| ステップ定義（3ステップ） | 🔧 ハードコード | `roadmap/services.py` の `STEP_DEFINITIONS`（テーマ・絵文字・色・説明） |
| ロードマップタスク生成 | 🤖 AI（フォールバック: 🔧） | `_generate_with_ai()` → OpenAI API（gpt-4o-mini）。失敗時は `_fallback_roadmap()` → `ROADMAP_DATA` 静的データで代替 |
| フォールバック用ロードマップデータ | 🔧 ハードコード | `ROADMAP_DATA`（5仕事タイプ×3ステップ×タスク・励ましメッセージ） |
| ロードマップキャッシュ | 🗄️ DB管理 | `RoadmapCache` モデル。一度生成したロードマップをDBにキャッシュ（Django Adminから手動削除可） |
| 支援員向けAIアドバイス | 🤖 AI（フォールバック: 📐） | `get_supporter_advice()` → OpenAI API（gpt-4o-mini）。失敗時は最新記録の感情スコアによるルールベース固定文（記録なし / スコア4以上 / スコア2以下 / それ以外の4パターン） |

### 11.3 日常記録・ダッシュボード（大人向け）

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| 気持ちスタンプ定義（1〜5） | 🔧 ハードコード | テンプレート内の絵文字・ラベル・カラー定義。`rag/services.py` の `EMOTION_LABELS` |
| 体調スコア定義（1〜3） | 🔧 ハードコード | `rag/services.py` の `HEALTH_LABELS` |
| 感情スタンプによるアバター表情変化 | 📐 ルールベース | ダッシュボード表示時: スタンプ≥4→happy、≤2→worried、それ以外→normal |
| バッジカウント | 📐 ルールベース | 総 `DailyRecord` 件数をリアルタイムで計算（DBへの保存なし） |
| 週間感情グラフ | 📐 ルールベース | 過去7日間の `DailyRecord` を集計して Chart.js に渡す |

### 11.4 児童向けダッシュボード

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| なりたい職業選択（9種） | 🔧 ハードコード | `daily/child_advice.py` の `CAREER_CHOICES`（キー・絵文字・ラベルのタプルリスト） |
| 学年別×職業別アドバイス | 🔧 ハードコード | `CHILD_ADVICE` 辞書（4学年×9職業×各4件=144件） |
| 職業・学年ラベル（漢字・ひらがな） | 🔧 ハードコード | `CAREER_LABELS`, `CAREER_LABELS_HIRAGANA`, `GRADE_LABELS`, `GRADE_LABELS_HIRAGANA` |
| アドバイスの追加・変更 | 🔧 ハードコード | コードを直接編集する必要あり（DBでは管理されていない） |

### 11.5 AIチャット（アバターチャット）

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| システムプロンプト生成 | 📐 ルールベース（＋DB参照） | `get_avatar_system_prompt()` がユーザーのニックネーム・仕事タイプ・強み・課題（最新の `DiagnosisSession` から取得）を組み込んでプロンプトを組み立てる |
| アバター返答生成 | 🤖 AI（フォールバック: 🔧） | `chat_with_avatar()` → OpenAI API（gpt-4o-mini、temperature=0.8、max_tokens=300）。`OPENAI_API_KEY` 未設定または例外発生時は `_fallback_avatar_response()` を使用 |
| フォールバック返答 | 🔧 ハードコード | `_fallback_avatar_response()` のキーワードマッチング（つかれた系・できた系・むずかしい系・ふあん系・たのしい系の5パターン＋デフォルト）。ひらがな・漢字各2候補をランダム選択 |
| チャット履歴 | 🗄️ DB管理 | `AvatarChatMessage` モデル。APIへは最新10件を送信 |

### 11.6 RAG AI（支援記録ベースアドバイス）

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| 支援記録のベクトル化 | 🤖 AI | `embed_support_record()` → OpenAI API（text-embedding-3-small）でベクトル生成 → `SupportRecordEmbedding` モデルに保存 |
| 類似記録検索 | 🤖 AI（フォールバック: 📐） | `search_similar_records()` → クエリをベクトル化してコサイン類似度で上位5件を取得。APIなし時は日付降順の最新5件 |
| コサイン類似度計算 | 📐 ルールベース | `cosine_similarity()` → numpy でベクトル演算（AIではなく数学的処理） |
| 児童向けRAGアドバイス生成 | 🤖 AI（フォールバック: 🔧） | `generate_rag_advice_for_child()` → 支援記録・発達スコアをコンテキストに OpenAI API（gpt-4o-mini、max_tokens=800）で生成。APIなし時は固定エラーメッセージ |
| 利用者向けRAGアドバイス生成 | 🤖 AI（フォールバック: 🔧） | `generate_rag_advice_for_user()` → 日常記録・プロフィールをコンテキストに OpenAI API（gpt-4o-mini、max_tokens=800）で生成。APIなし時は固定エラーメッセージ |
| コンテキスト組み立て | 📐 ルールベース | 支援記録・発達スコア・プロフィールを文字列に整形してプロンプトに渡す（AIは使用しない） |

### 11.7 ひらがな変換

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| テンプレートテキストの自動変換 | 📐 ルールベース（pykakasi） | `{% t "漢字" %}` タグで pykakasi を使用して自動変換（`diagnosis/templatetags/text_mode.py`） |
| 手動指定（優先） | 🔧 ハードコード | `{% t "漢字" "ひらがな" %}` の第2引数で上書き可能 |
| 誤読の補正 | 🔧 ハードコード | `_POST_REPLACEMENTS` リストで `さむらい→し`（「士」の誤読）などを後処理補正 |
| 変換結果キャッシュ | 📐 ルールベース | `@lru_cache(maxsize=2048)` で変換結果をメモリキャッシュ（APIは使用しない） |

### 11.8 ゲーミフィケーション（称号・ポイント・ストリーク）

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| 称号定義（9種） | 🔧 ハードコード | `gamification/models.py` の `TITLE_DEFINITIONS`（キー・名前・説明・閾値・種別） |
| ストリーク更新・ポイント付与 | 📐 ルールベース | `UserStreak.update_streak()` — 連続日数に応じてポイントを計算（基本10pt＋連続日数×2pt） |
| 称号自動付与 | 📐 ルールベース | `UserTitle.check_and_award()` — ストリーク・ポイント・診断回数・記録回数・クイズ正解数と閾値を比較して自動付与 |
| 称号獲得ボーナスポイント | 📐 ルールベース | 称号獲得時に +50pt 付与 |
| スタンプ種別（6種） | 🔧 ハードコード | `learning/models.py` の `STAMP_TYPES`（login/record/quiz/read/emotion/challenge） |
| 週間チャレンジ定義（5件） | 🔧 ハードコード（初回のみ） | `gamification/seed_data.py` の `CHALLENGES`。`python manage.py seed_data` で投入 |
| チャレンジ進捗管理 | 📐 ルールベース | `UserChallengeProgress` モデルで進捗カウント。完了時にポイント付与 |
| 模擬面接練習ポイント | 📐 ルールベース | 面接回答送信時に +15pt 付与（`learning/views.py`） |

### 11.9 就労マナークイズ

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| クイズ問題・選択肢 | 🗄️ DB管理 | Django Admin から追加・編集可能（`MannerQuiz`, `QuizChoice` モデル） |
| クイズカテゴリ（5種） | 🔧 ハードコード | `learning/models.py` の `QUIZ_CATEGORIES`（greeting/report/manner/safety/team） |
| 初期8問 | 🔧 ハードコード（初回のみ） | `gamification/seed_data.py` の `QUIZZES` リスト。`python manage.py seed_data` で投入 |
| 正解判定 | 📐 ルールベース | `QuizChoice.is_correct` フラグで判定 |
| ポイント付与 | 📐 ルールベース | 正解: +20pt、不正解でも回答: +5pt |

### 11.10 模擬面接練習

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| 面接質問6問 | 🔧 ハードコード | `learning/models.py` の `INTERVIEW_QUESTIONS`（id・質問文・ヒント・絵文字） |
| AIフィードバック | 🤖 AI（フォールバック: 📐） | `_generate_interview_feedback()` → OpenAI API（gpt-4o-mini、100字以内の優しい評価）。APIなし時は回答の文字数（20字未満・50字未満・50字以上）による3段階ルールベースフィードバック |
| 練習ポイント付与 | 📐 ルールベース | 回答送信時に +15pt 付与 |

### 11.11 職業情報・求人マッチング

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| 職業5タイプの詳細情報 | 🔧 ハードコード | `diagnosis/job_data.py` の `JOB_TYPE_DETAILS`（特徴・1日のスケジュール・必要スキル・練習タスク・勤務先例） |
| サンプル求人6件 | 🔧 ハードコード | `JOB_LISTINGS`（架空のサンプルデータ。農業2件・製造1件・清掃1件・食品加工1件・接客1件） |
| 求人マッチング | 📐 ルールベース | `job_type` フィールドが一致する求人を表示するのみ（スコアリングや類似度計算なし） |

### 11.12 連絡帳・スケジュール・スタンプ

| 機能 | 実装方式 | 詳細 |
|---|---|---|
| 連絡帳（`ContactNote`） | 🗄️ DB管理 | 支援員が保護者へ送信。今日のようす（1〜5）・連絡内容・おうちでやってほしいこと等をDjango Admin・ビューから管理 |
| 今日のようす選択肢（5段階） | 🔧 ハードコード | `ContactNote.mood` の choices（5=とても良かった〜1=心配）および絵文字マップ `get_mood_emoji()` |
| 活動スケジュールテンプレート | 🗄️ DB管理 | `DailyScheduleTemplate` / `ScheduleItem` モデル。Django Adminや専用ビューから曜日別テンプレートを作成・編集 |
| スタンプ種別（6種） | 🔧 ハードコード | `learning/models.py` の `STAMP_TYPES`（login/record/quiz/read/emotion/challenge） |
| スタンプ付与タイミング | 📐 ルールベース | ログイン・記録・クイズ回答・読書記録・気持ち選択・チャレンジの各アクション時にビュー側でルールとして付与 |

---

## 12. ハードコード箇所の管理方法（今後の改善候補）

各ハードコード箇所をより柔軟に管理するための対応方針を以下に記載する。

| ハードコード箇所 | 現状の問題 | 改善方針 |
|---|---|---|
| `CHILD_ADVICE`（4学年×9職業×4件=144件） | コード直接編集が必要。非エンジニアが変更できない | `ChildAdvice` DBモデルを作成し、Django Admin から追加・編集できるようにする |
| `DIAGNOSIS_QUESTIONS`（13問） | 問題文・カテゴリ変更にコード修正が必要 | `DiagnosisQuestion` DBモデル化。Admin から追加・並び替えを可能にする |
| `INTERVIEW_QUESTIONS`（6問） | 問題・ヒント追加にコード修正が必要 | `InterviewQuestion` DBモデル化。Admin から管理 |
| `ROADMAP_DATA`（フォールバック用静的データ） | 仕事タイプ追加時に Python コードの修正が必要 | `RoadmapFallback` DBモデル化（または `RoadmapCache` の手動投入フローを整備） |
| `JOB_TYPE_DETAILS` / `JOB_LISTINGS` | 求人情報が架空データのため実用性がない | `JobListing` DBモデル化し、Django Admin から実際の求人・実習先情報を登録できるようにする |
| `TITLE_DEFINITIONS`（9称号） | 称号の追加・閾値変更にコード修正が必要 | `TitleDefinition` DBモデル化。称号の名前・閾値を Admin から管理 |
| `CHALLENGES`（週間チャレンジ5件） | 既に `WeeklyChallenge` DBモデルが存在するが、初回は seed_data でのみ投入 | Admin UI の整備とシード不要な初期データ管理フロー（`data migrations` や `fixtures`）に移行 |
| フォールバック応答文（診断・ロードマップ・チャット） | 硬直的な固定文。改善にコード修正が必要 | 最低限の修正で `FallbackMessage` テーブル化し、Admin から編集可能にする（優先度は低） |
