#!/usr/bin/env python3
"""
Chạy trang trái tim trong mạng wifi nhà mình và in luôn mã QR ra terminal.

    python3 serve.py            (cổng mặc định 8899)
    python3 serve.py 9000

Điện thoại nối cùng wifi -> mở camera -> quét mã QR hiện ra ở terminal.
Muốn gửi cho người ở xa thì phải mở tunnel (xem README) rồi chạy:
    python3 make_qr.py <địa-chỉ-công-khai>
"""

import http.server
import os
import socket
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8899


def ip_trong_mang():
    """IP của máy trong mạng LAN — hỏi hệ điều hành bằng một socket giả."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()


class Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        # đang sửa trang liên tục, đừng để trình duyệt giữ bản cũ
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == '__main__':
    dia_chi = f'http://{ip_trong_mang()}:{PORT}/'

    try:
        sys.path.insert(0, os.path.join(ROOT, 'vendor'))
        from make_qr import tao
        print('\n  Quét mã dưới đây bằng camera điện thoại (cùng wifi):')
        tao(dia_chi)
    except Exception as e:
        print(f'  (không tạo được QR: {e})')
        print(f'  Địa chỉ: {dia_chi}')

    print(f'\n  Máy chủ đang chạy. Ctrl+C để dừng.\n')
    try:
        http.server.ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print('\n  Đã dừng. 💗\n')
