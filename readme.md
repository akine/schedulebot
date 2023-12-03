# ScheduleBot 🤖📅

ScheduleBotは、あなたのGoogleカレンダーに追加、編集、削除されたイベントを監視し、Discordへ通知するPythonスクリプトです。あなたの日々の予定を見逃さないように、便利で簡単に設定できます。

## 主な機能 🌟

- Googleカレンダーのイベントをリアルタイムで監視
- 新しく追加されたイベントの通知
- イベントの編集や削除に関する通知
- Discordを通じての通知機能

## 設定方法 🛠️

1. **GoogleカレンダーAPIの設定**: Google Cloud Consoleでプロジェクトを作成し、カレンダーAPIを有効にして認証情報を取得します。
2. **Discord Webhookの設定**: DiscordサーバーにWebhookを作成し、取得したURLを環境変数に設定します。
3. **Pythonスクリプトの準備**: 必要なライブラリをインストールし、スクリプトを設定します。
4. **スクリプトの実行**: スクリプトを定期的に実行するために、cronなどのスケジューラを設定します。

## 依存関係のインストール 📦

スクリプトを実行する前に、必要なPythonライブラリをインストールしてください。

```bash
pip install -r requirements.txt
```

### 環境変数の設定 🔑
- `.env` ファイルを作成し、以下のように環境変数を設定します。

```bash
DISCORD_WEBHOOK_URL=あなたのDiscord Webhook URL
```

### 実行方法 ▶️
- すべての設定が完了したら、スクリプトを実行してください。

```bash
python calendar_access.py
```

### 注意事項 ⚠️
- GoogleカレンダーのAPIキーは安全に保管してください。
- Discord Webhook URLは漏洩しないように注意してください。
- 定期実行の設定は、サーバーの設定により異なる場合があります。

- ScheduleBotは、あなたの日々の予定を簡単に管理するためのツールです。楽しんでご利用ください！ 🎉🗓️