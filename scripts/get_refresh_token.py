"""
CHI CHAY 1 LAN, TREN MAY CA NHAN CUA BAN (khong chay trong GitHub Actions).
Muc dich: lay Google OAuth refresh token cho Calendar, de dan vao GitHub
Secrets. Script khong gui thong tin di dau ca, chi in ra man hinh cho ban
tu copy.

Chuan bi truoc khi chay:
  1) pip install google-auth-oauthlib
  2) Tao OAuth Client ID loai "Desktop app" tren Google Cloud Console
     (xem huong dan trong SETUP.md), tai file JSON ve, doi ten thanh
     "credentials.json" va dat cung thu muc voi script nay.

Chay:
  python get_refresh_token.py

Trinh duyet se tu mo de ban dang nhap Google va cap quyen doc Calendar.
Sau khi xong, script se in ra 3 gia tri can dan vao GitHub Secrets.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main() -> None:
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    print("\n=== COPY 3 GIA TRI DUOI DAY VAO GITHUB SECRETS (Settings > Secrets and variables > Actions) ===\n")
    print(f"GOOGLE_CLIENT_ID     = {creds.client_id}")
    print(f"GOOGLE_CLIENT_SECRET = {creds.client_secret}")
    print(f"GOOGLE_REFRESH_TOKEN = {creds.refresh_token}")
    print("\nLuu y: neu GOOGLE_REFRESH_TOKEN bi trong (None), vao Google Account")
    print("> Security > Third-party access, thu hoi quyen truy cap cu cua app nay")
    print("roi chay lai script de Google cap refresh token moi.")


if __name__ == "__main__":
    main()
