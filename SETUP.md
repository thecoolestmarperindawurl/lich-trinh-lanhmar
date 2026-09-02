# Setup: chay Lich trinh LANHMAR hoan toan tu dong tren GitHub Actions

Sau khi lam xong cac buoc duoi, he thong chay tren server — **khong can mo
Claude Desktop hay bat may tinh**. 3 khung gio giu nguyen: 06:00 (cap nhat
lich tuan), 07:00 (nhac lich quan trong hom nay), 20:00 (nhac lich quan
trong ngay mai) — gio Viet Nam.

**QUAN TRONG (cap nhat 02/09/2026):** Workflow KHONG con dung `schedule:`
(cron noi bo cua GitHub Actions) nua, vi day la co che best-effort cua
GitHub — hay bi tre hang gio hoac bi bo hoan toan khi he thong GitHub tai
cao (đa xac nhan qua thuc te: co lan tre hơn 3 tiếng, co lan khong chay
du chinh xac). Thay vao do, lich chay chinh xac duoc dieu khien tu MOT
DICH VU HEN GIO BEN NGOAI (**cron-job.org**, mien phi, chay dung phut) —
dich vu nay goi thang API `workflow_dispatch` cua GitHub vao dung gio,
va GitHub xu ly `workflow_dispatch` gan nhu ngay lap tuc (khong bi xep
hang nhu `schedule`).

Can lam 4 viec mot lan duy nhat: (1) tao OAuth Client cho Google Calendar,
(2) lay Telegram Bot Token, (3) khai bao 5 Secret tren GitHub, (4) setup
cron-job.org goi workflow_dispatch dung gio. Buoc 1-3 xem it hon, buoc 4
la phan moi quan trong nhat de dam bao dung timeline.

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
   dong y cap quyen doc Calendar.
4. Terminal in ra 3 dong — **giu lai de dung o Buoc 4**:
   ```
   GOOGLE_CLIENT_ID     = ...
   GOOGLE_CLIENT_SECRET = ...
   GOOGLE_REFRESH_TOKEN = ...
   ```

## Buoc 3 — Lay Telegram Bot Token

Bot `@lanhmar_schedule_bot` da co san. Lay token goc cua no:

1. Mo Telegram, chat voi **@BotFather**.
2. Go `/mybots` → chon **lanhmar_schedule_bot**.
3. Chon **API Token** → copy chuoi dang `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.

Chat ID (noi bot gui tin) da biet san la **8654887902**.

## Buoc 4 — Khai bao GitHub Secrets

1. Mo repo https://github.com/thecoolestmarperindawurl/lich-trinh-lanhmar
2. Vao **Settings > Secrets and variables > Actions > New repository
   secret**, them lan luot 5 secret sau:

   | Ten secret | Gia tri |
   |---|---|
   | `GOOGLE_CLIENT_ID` | tu Buoc 2 |
   | `GOOGLE_CLIENT_SECRET` | tu Buoc 2 |
   | `GOOGLE_REFRESH_TOKEN` | tu Buoc 2 |
   | `TELEGRAM_BOT_TOKEN` | tu Buoc 3 |
   | `TELEGRAM_CHAT_ID` | `8654887902` |

---

## Buoc 5 — Cron chinh xac voi cron-job.org (BAT BUOC de dung timeline)

### 5.1. Tao GitHub Personal Access Token (PAT)

1. Vao https://github.com/settings/personal-access-tokens/new (fine-grained token).
2. **Token name**: `lich-trinh-cronjob`.
3. **Expiration**: chon 1 nam (hoac tuy y, nho gia han truoc khi het han).
4. **Repository access**: chon **Only select repositories** → chon
   `lich-trinh-lanhmar`.
5. **Permissions** → **Repository permissions** → tim **Actions** → chon
   **Read and write**.
6. Bam **Generate token** → **COPY VA LUU LAI NGAY** (chi hien 1 lan duy
   nhat, dang `github_pat_xxxxxxxxxxxxxxxxxxxxx`).

### 5.2. Dang ky cron-job.org

1. Vao https://cron-job.org/en/signup/ → tao tai khoan mien phi (email +
   mat khau, hoac dang nhap Google).
2. Xac nhan email neu duoc yeu cau.

### 5.3. Tao 3 cronjob (moi cronjob goi 1 API request)

Vao **Cronjobs > Create cronjob**, lap lai 3 lan voi thong so sau (giong
nhau, chi khac **Title**, **Schedule** va **mode** trong Body):

**Chung cho ca 3:**
- **URL**: `https://api.github.com/repos/thecoolestmarperindawurl/lich-trinh-lanhmar/actions/workflows/lich-trinh.yml/dispatches`
- **Request method**: `POST`
- **Headers** (them 3 header):
  - `Authorization` = `Bearer github_pat_xxxxxxxxxxxxxxxxxxxxx` (dan PAT tu buoc 5.1)
  - `Accept` = `application/vnd.github+json`
  - `Content-Type` = `application/json`
- **Request body** (chon kieu Raw/JSON):
  ```json
  {"ref":"main","inputs":{"mode":"update"}}
  ```
  (doi `"update"` thanh `"morning"` hoac `"evening"` cho 2 cronjob con lai)
- **Timezone**: chon `Asia/Ho_Chi_Minh` (o phan Schedule, cron-job.org cho
  chon mui gio rieng cho tung job — khong can tu quy doi sang UTC).

**3 cronjob can tao:**

| Title | Schedule (gio VN) | Body |
|---|---|---|
| Lich trinh - Cap nhat tuan | 06:00 hang ngay | `{"ref":"main","inputs":{"mode":"update"}}` |
| Lich trinh - Nhac sang | 07:00 hang ngay | `{"ref":"main","inputs":{"mode":"morning"}}` |
| Lich trinh - Nhac toi | 20:00 hang ngay | `{"ref":"main","inputs":{"mode":"evening"}}` |

Sau khi tao xong, bam **Save**, roi bam nut **Execute now** (chay thu
ngay) tren tung cronjob de kiem tra request tra ve **204 No Content**
(nghia la GitHub da nhan va dang chay workflow) — vao tab **Actions** cua
repo de xem run moi xuat hien.

---

## Buoc 6 — Bao lai cho Claude

Sau khi ca 3 cronjob chay thu thanh cong (thay run moi trong tab Actions
va nhan duoc tin Telegram), bao lai — he thong se hoan toan doc lap, chay
dung gio, khong phu thuoc Claude Desktop, may tinh cua ban co bat hay
khong, hay do tin cay cua GitHub schedule.
