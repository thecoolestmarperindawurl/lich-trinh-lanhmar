# Setup: chay Lich trinh LANHMAR hoan toan tu dong tren GitHub Actions

Sau khi lam xong cac buoc duoi, he thong chay tren server cua GitHub —
**khong can mo Claude Desktop hay bat may tinh**. 3 khung gio giu nguyen:
06:00 (cap nhat lich tuan), 07:00 (nhac lich quan trong hom nay), 20:00
(nhac lich quan trong ngay mai) — gio Viet Nam.

Can lam 3 viec mot lan duy nhat: (1) tao OAuth Client cho Google Calendar,
(2) lay Telegram Bot Token, (3) khai bao 5 Secret tren GitHub. Sau do moi
thu tu chay.

---

## Buoc 1 — Tao Google OAuth Client (de doc Calendar)

1. Vao https://console.cloud.google.com/ → tao project moi (hoac dung
   project co san) → ten gi cung duoc, vi du "lanhmar-automation".
2. Vao **APIs & Services > Library**, tim "Google Calendar API" → bam
   **Enable**.
3. Vao **APIs & Services > OAuth consent screen**:
   - User type: **External**.
   - Dien ten app, email lien he (dung chinh gmail cua ban).
   - O muc **Test users**, them `anhduong.talkandshare@gmail.com`.
   - Luu lai (khong can submit de Google duyet — che do Testing la du).
4. Vao **APIs & Services > Credentials** → **Create Credentials >
   OAuth client ID**:
   - Application type: **Desktop app**.
   - Dat ten bat ky → **Create**.
   - Bam **Download JSON** → doi ten file thanh `credentials.json`.

## Buoc 2 — Lay Refresh Token (chay 1 lan tren may ban)

1. Dat `credentials.json` (vua tai o Buoc 1) va file `scripts/get_refresh_token.py`
   (trong repo nay) vao cung mot thu muc tren may tinh cua ban.
2. Mo terminal tai thu muc do, chay:
   ```
   pip install google-auth-oauthlib
   python get_refresh_token.py
   ```
3. Trinh duyet tu mo → dang nhap bang `anhduong.talkandshare@gmail.com` →
   dong y cap quyen doc Calendar (Google se canh bao "app chua xac minh" —
   bam **Advanced > Go to [ten app] (unsafe)**, day la app do chinh ban
   tao nen an toan).
4. Terminal in ra 3 dong — **giu lai de dung o Buoc 4**:
   ```
   GOOGLE_CLIENT_ID     = ...
   GOOGLE_CLIENT_SECRET = ...
   GOOGLE_REFRESH_TOKEN = ...
   ```

## Buoc 3 — Lay Telegram Bot Token

Bot `@lanhmar_schedule_bot` da co san (dang dung de gui thong bao). Lay
token goc cua no:

1. Mo Telegram, chat voi **@BotFather**.
2. Go `/mybots` → chon **lanhmar_schedule_bot**.
3. Chon **API Token** → BotFather hien ra chuoi dang
   `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` → copy lai.

Chat ID (noi bot gui tin) da biet san la **8654887902**.

## Buoc 4 — Khai bao GitHub Secrets

1. Mo repo https://github.com/thecoolestmarperindawurl/lich-trinh-lanhmar
2. Vao **Settings > Secrets and variables > Actions > New repository
   secret**, them lan luot 5 secret sau (ten phai khop chinh xac):

   | Ten secret | Gia tri |
   |---|---|
   | `GOOGLE_CLIENT_ID` | tu Buoc 2 |
   | `GOOGLE_CLIENT_SECRET` | tu Buoc 2 |
   | `GOOGLE_REFRESH_TOKEN` | tu Buoc 2 |
   | `TELEGRAM_BOT_TOKEN` | tu Buoc 3 |
   | `TELEGRAM_CHAT_ID` | `8654887902` |

## Buoc 5 — Chay thu

1. Vao tab **Actions** tren repo → chon workflow **LANHMAR Lich Trinh
   Automation** → **Run workflow** (dung input mac dinh `update`) → chay.
2. Kiem tra: trang https://thecoolestmarperindawurl.github.io/lich-trinh-lanhmar/
   cap nhat dung tuan hien tai, va co tin Telegram gui toi.
3. Neu loi, mo log cua run do trong tab Actions de xem thong bao loi cu
   the (thuong la do go sai ten/gia tri secret).

## Buoc 6 — Bao lai cho Claude

Sau khi buoc 5 chay on, bao lai trong Claude — se tat 3 scheduled task cu
trong Claude Desktop (de tranh gui trung lap thong bao), va tu do toan bo
he thong chay doc lap tren GitHub, khong phu thuoc Claude Desktop hay may
tinh cua ban co bat hay khong.
