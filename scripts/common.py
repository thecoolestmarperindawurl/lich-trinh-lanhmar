"""
Ham dung chung: lay Google OAuth access token tu refresh token, goi Google
Calendar API, parse su kien theo quy uoc cua LANHMAR, va gui tin Telegram.
Khong phu thuoc Claude/Composio - chi dung requests thuan.
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

TZ = ZoneInfo("Asia/Ho_Chi_Minh")
CALENDAR_ID = os.environ.get("GOOGLE_CALENDAR_ID", "anhduong.talkandshare@gmail.com")


def get_access_token() -> str:
    r = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def list_events(time_min_iso: str, time_max_iso: str):
    token = get_access_token()
    url = f"https://www.googleapis.com/calendar/v3/calendars/{requests.utils.quote(CALENDAR_ID, safe='')}/events"
    params = {
        "timeMin": time_min_iso,
        "timeMax": time_max_iso,
        "timeZone": "Asia/Ho_Chi_Minh",
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": 100,
    }
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("items", [])


def parse_event(ev: dict) -> dict:
    summary = (ev.get("summary") or "").strip()
    color_id = ev.get("colorId")

    status = "pending"
    title = summary
    if summary.startswith("✅"):
        status = "done"
        title = summary.lstrip("✅").lstrip("️").strip()
    elif summary.startswith("❌"):
        status = "notdone"
        title = summary.lstrip("❌").lstrip("️").strip()

    start_dt = ev.get("start", {}).get("dateTime")
    end_dt = ev.get("end", {}).get("dateTime")
    start_s = datetime.fromisoformat(start_dt).astimezone(TZ).strftime("%H:%M") if start_dt else "00:00"
    end_s = datetime.fromisoformat(end_dt).astimezone(TZ).strftime("%H:%M") if end_dt else "23:59"

    return {
        "title": title,
        "status": status,
        "start": start_s,
        "end": end_s,
        "important": color_id == "11",
        "has_time": bool(start_dt),
    }


def send_telegram(text: str) -> dict:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": text},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()
