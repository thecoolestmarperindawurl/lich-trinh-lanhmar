"""
Chay 2 lan/ngay:
  - "morning" luc 07:00 gio VN (cron 00:00 UTC): nhac lai lich quan trong HOM NAY.
  - "evening" luc 20:00 gio VN (cron 13:00 UTC): nhac truoc lich quan trong NGAY MAI.
Lich "quan trong" = colorId "11" (Tomato) tren Google Calendar.
"""
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from common import TZ, list_events, parse_event, send_telegram  # noqa: E402

PAGE_URL = "https://thecoolestmarperindawurl.github.io/lich-trinh-lanhmar/"


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "morning"
    now = datetime.now(TZ)
    target = now.date() if mode == "morning" else (now + timedelta(days=1)).date()

    time_min = f"{target.isoformat()}T00:00:00+07:00"
    time_max = f"{(target + timedelta(days=1)).isoformat()}T00:00:00+07:00"
    events = list_events(time_min, time_max)

    important = []
    for ev in events:
        if ev.get("colorId") != "11":
            continue
        p = parse_event(ev)
        if not p["has_time"]:
            continue
        important.append(p)

    date_str = target.strftime("%d/%m/%Y")
    if mode == "morning":
        header = f"🔔 Lịch quan trọng HÔM NAY ({date_str})"
        empty_msg = f"Hôm nay ({date_str}) không có lịch quan trọng (Tomato) nào. 🎉"
    else:
        header = f"🔔 Nhắc chuẩn bị: lịch quan trọng NGÀY MAI ({date_str})"
        empty_msg = f"Ngày mai ({date_str}) không có lịch quan trọng (Tomato) nào."

    if not important:
        send_telegram(empty_msg)
        print("OK: no important events")
        return

    lines = [header, ""]
    lines += [f"- {p['start']}–{p['end']} {p['title']}" for p in important]
    lines += ["", f"👉 Xem chi tiết: {PAGE_URL}"]

    send_telegram("\n".join(lines))
    print(f"OK: sent {len(important)} important events")


if __name__ == "__main__":
    main()
