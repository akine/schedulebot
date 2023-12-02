import os
import datetime
import pytz
import json
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# GoogleカレンダーAPIのスコープ
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Discord Webhook URL
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
if not DISCORD_WEBHOOK_URL:
    raise ValueError("Discord Webhook URLが設定されていません。")

def save_events_to_file(events, filename='events.json'):
    with open(filename, 'w') as f:
        json.dump(events, f, indent=4)

def load_events_from_file(filename='events.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def event_exists(event, events):
    return any(e['id'] == event['id'] for e in events)

def send_discord_notification(message):
    """Discordに通知を送る関数"""
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    response.raise_for_status()

def is_event_modified(event, previous_events):
    for prev_event in previous_events:
        if prev_event['id'] == event['id']:
            # イベント詳細の比較（開始時刻、終了時刻、要約、概要など）
            if (prev_event['start'] != event['start'] or 
                prev_event['end'] != event['end'] or 
                prev_event.get('summary', '') != event.get('summary', '') or
                prev_event.get('description', '') != event.get('description', '')):
                return True
    return False

def main():
    creds = None
    # token.jsonファイルがあれば、トークンをロード
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 有効な認証情報がない場合は新規に取得
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # トークンを保存
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # 現在時刻から1ヶ月後の時刻を取得
    current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    one_month_later = current_time + datetime.timedelta(days=30)

    # 現在のイベントデータを取得
    events_result = service.events().list(calendarId='primary', timeMin=current_time.isoformat(),
                                          timeMax=one_month_later.isoformat(), singleEvents=True, 
                                          orderBy='startTime').execute()
    current_events = events_result.get('items', [])

    # 以前のイベントデータを一時ファイルから読み込む
    previous_events = load_events_from_file()

    # 新しく追加されたイベントを特定
    new_events = [event for event in current_events if not event_exists(event, previous_events)]

    # 削除されたイベントを特定
    deleted_events = [event for event in previous_events if not event_exists(event, current_events)]

    # 編集されたイベントを特定
    modified_events = [event for event in current_events if event_exists(event, previous_events) and is_event_modified(event, previous_events)]

    # 新しく追加されたイベントを特定し、通知する
    for event in new_events:
        event_start = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.datetime.fromisoformat(event_start.rstrip('Z')).replace(tzinfo=pytz.UTC).isoformat()
        description = event.get('description', '説明なし')  # 説明を取得、存在しない場合は '説明なし'
        message = f"新しい予定が追加されました: {event['summary']} at {start}\n説明: {description}"
        print(message)
        send_discord_notification(message)

    # 削除されたイベントについて通知
    for event in deleted_events:
        message = f"予定が削除されました: {event['summary']}"
        print(message)
        send_discord_notification(message)

    # 編集されたイベントについて通知
    for event in modified_events:
        event_start = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.datetime.fromisoformat(event_start.rstrip('Z')).replace(tzinfo=pytz.UTC).isoformat()
        description = event.get('description', '説明なし')
        message = f"予定が編集されました: {event['summary']} at {start}\n説明: {description}"
        print(message)
        send_discord_notification(message)

    # 現在のイベントデータを一時ファイルに保存
    save_events_to_file(current_events)

if __name__ == '__main__':
    main()