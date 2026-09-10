#!/usr/bin/env python3
"""
Tạo mã QR trỏ tới trang trái tim.

Dùng:
    python3 make_qr.py https://dia-chi-cua-ban.com
    python3 make_qr.py                 (không truyền gì thì nó hỏi)

Sinh ra:
    qr.png        — ảnh QR để gửi/in
    qr-card.html  — tấm thiệp có mã QR, mở ra in cho đẹp
    và in luôn mã QR ra màn hình terminal để quét thử ngay.
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'vendor'))   # dùng segno đóng gói sẵn

import segno   # noqa: E402

HONG_DAM = '#c93f6d'
NEN      = '#fff5f8'


def tao(url, thu_muc=ROOT, in_terminal=True):
    qr = segno.make(url, error='m')       # mức sửa lỗi M — chịu được xước, mờ

    png = os.path.join(thu_muc, 'qr.png')
    qr.save(png, scale=14, border=4, dark=HONG_DAM, light=NEN)

    the = os.path.join(thu_muc, 'qr-card.html')
    with open(the, 'w', encoding='utf-8') as f:
        f.write(THIEP.replace('{{DATA}}', qr.png_data_uri(
            scale=10, border=2, dark=HONG_DAM, light=NEN)))

    if in_terminal:
        print()
        qr.terminal(compact=True)
        print()

    print(f'  Địa chỉ  : {url}')
    print(f'  Ảnh QR   : {png}')
    print(f'  Tấm thiệp: {the}')
    return png, the


THIEP = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quét đi nhé 💗</title>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@200;300&family=Dancing+Script:wght@700&display=swap&subset=vietnamese" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{
    min-height:100vh;display:grid;place-items:center;padding:28px;
    background:radial-gradient(ellipse at 50% 0%,#ffe3ec 0%,#fff5f8 60%);
    font-family:'Be Vietnam Pro',-apple-system,sans-serif;color:#7a3550;
  }
  .the{
    width:min(400px,92vw);padding:38px 32px 30px;border-radius:26px;text-align:center;
    background:#fff;border:1px solid #ffd3e0;
    box-shadow:0 24px 60px rgba(201,63,109,.16);
  }
  h1{font-family:'Dancing Script',cursive;font-size:38px;color:#c93f6d;line-height:1.1}
  .sub{font-size:11px;font-weight:200;letter-spacing:.28em;text-transform:uppercase;color:#c795a8;margin-top:8px}
  img{width:100%;max-width:280px;margin:26px auto 18px;display:block;border-radius:14px}
  .chan{font-size:14px;font-weight:300;line-height:1.7;color:#9c5a75}
  .tim{font-size:20px;margin-top:14px}
  @media print{body{background:#fff}.the{box-shadow:none;border-color:#eee}}
</style>
</head>
<body>
  <div class="the">
    <h1>Có một điều<br>muốn nói với em</h1>
    <p class="sub">quét mã này nhé</p>
    <img src="{{DATA}}" alt="Mã QR">
    <p class="chan">Mở camera điện thoại lên,<br>hướng vào đây một chút là thấy.</p>
    <div class="tim">💗</div>
  </div>
</body>
</html>
"""


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dia_chi = sys.argv[1].strip()
    else:
        dia_chi = input('Dán địa chỉ trang vào đây: ').strip()

    if not dia_chi:
        print('Chưa có địa chỉ nào cả.')
        sys.exit(1)
    if '://' not in dia_chi:
        dia_chi = 'https://' + dia_chi

    tao(dia_chi)
