"""
Chay luc 06:00 gio VN (cron 23:00 UTC). Lay lich tuan hien tai (Thu2-CN)
tu Google Calendar, cap nhat mang `days` trong index.html (giu nguyen
CSS/HTML/JS con lai), commit se duoc git thuc hien o buoc sau trong
workflow. Gui tom tat qua Telegram.
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from common import TZ, list_events, parse_event, send_telegram  # noqa: E402

DNAMES = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
PAGE_URL = "https://thecoolestmarperindawurl.github.io/lich-trinh-lanhmar/"
INDEX_PATH = os.environ.get("INDEX_PATH", "index.html")


def main() -> None:
    now = datetime.now(TZ)
    weekday = now.isoweekday()  # Mon=1 .. Sun=7
    monday = (now - timedelta(days=weekday - 1)).date()
    sunday = monday + timedelta(days=6)
    week_dates = [monday + timedelta(days=i) for i in range(7)]

    time_min = f"{monday.isoformat()}T00:00:00+07:00"
    time_max = f"{(sunday + timedelta(days=1)).isoformat()}T00:00:00+07:00"
    events = list_events(time_min, time_max)

    days = [
        {
            "key": d.isoformat(),
            "dname": DNAMES[i],
            "ddate": d.strftime("%d/%m"),
            "today": d == now.date(),
            "events": [],
        }
        for i, d in enumerate(week_dates)
    ]

    total = done = notdone = 0
    important_pending = []

    for ev in events:
        p = parse_event(ev)
        if not p["has_time"]:
            continue
        start_dt = ev["start"]["dateTime"]
        ev_date = datetime.fromisoformat(start_dt).astimezone(TZ).date()
        idx = (ev_date - monday).days
        if not (0 <= idx <= 6):
            continue

        arr = [p["start"], p["end"], p["title"], p["status"]]
        if p["important"]:
            arr.append(True)
        days[idx]["events"].append(arr)

        total += 1
        if p["status"] == "done":
            done += 1
        elif p["status"] == "notdone":
            notdone += 1
        if p["important"] and p["status"] != "done":
            important_pending.append(
                f"{DNAMES[idx]} {week_dates[idx].strftime('%d/%m')} {p['start']}–{p['end']} {p['title']}"
            )

    marked = done + notdone
    rate = round(done / marked * 100) if marked else 0
    days_json = json.dumps(days, ensure_ascii=False)

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    html, n1 = re.subn(r"const days = \[.*?\];", f"const days = {days_json};", html, flags=re.S)
    if n1 != 1:
        raise RuntimeError("Khong tim thay/khong the thay the khoi `const days = [...]` trong index.html")

    lead_new = (
        f"Thứ 2 {monday.strftime('%d/%m')} – Chủ nhật {sunday.strftime('%d/%m/%Y')} · "
        f"Nguồn: Google Calendar (anhduong.talkandshare@gmail.com) · "
        f"Trạng thái lấy từ dấu ✅ / ❌ trong tiêu đề sự kiện"
    )
    html, n2 = re.subn(r'(<p class="lead">)[^<]*(</p>)', rf"\1{lead_new}\2", html)
    if n2 != 1:
        raise RuntimeError("Khong tim thay/khong the thay the dong <p class=\"lead\"> trong index.html")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    lines = [
        f"📅 Lịch trình tuần đã cập nhật ({monday.strftime('%d/%m')}–{sunday.strftime('%d/%m')})",
        "",
        f"✅ Hoàn thành: {done}",
        f"❌ Chưa hoàn thành: {notdone}",
        f"📊 Tỷ lệ: {rate}%",
    ]
    if important_pending:
        lines += ["", "🔔 Lịch quan trọng cần chú ý:"] + [f"- {x}" for x in important_pending]
    lines += ["", f"👉 Xem chi tiết: {PAGE_URL}"]

    send_telegram("\n".join(lines))
    print(f"OK: total={total} done={done} notdone={notdone} rate={rate}%")


if __name__ == "__main__":
    main()
