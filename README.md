# ネプリス

ネップリ共有サイト「[ネプリス](https://nepris.herokuapp.com/ "ネップリ共有サイト(β)")」の開発リポジトリです。

詳細は以下をご覧ください。

- [About](https://nepris.herokuapp.com/about/ "About｜ネップリ共有サイト(β)")
- [Qiita](https://qiita.com/glyzinieh/private/16111916b39ca5048736 "初心者が「ネップリ共有サイト」をつくった話（兼メモ） - Qiita")

## 環境変数について

```.env```に以下の内容を記述します

```.env
SHEET_PROJECT_ID=(project_id)
SHEET_PRIVATE_KEY_ID=(private_key_id)
SHEET_PRIVATE_KEY=(private_key)
SHEET_CLIENT_EMAIL=(client_email)
SHEET_CLIENT_ID=(client_id)
SHEET_CLIENT_X509_CERT_URL=(client_x509_cert_url)

SHEET_DATABASE_KEY=(シートID)

DB_URL=(データベースURL)
DB_TOKEN=(データベースTOKEN)

OTP_SECRET=(OTP生成用のシークレットコード)

GMAIL_ACCOUNT=(gmailのアドレス)
GMAIL_PASS=(gmailのパスワード)
```
