# qr-heart — quét mã, mở ra một trái tim

Một trang riêng biệt, tách hẳn khỏi trang `index.html` ở thư mục cha.
Quét mã QR → mở trang → trả lời hai câu hỏi → trái tim to giữa màn hình đập nhẹ,
chạm vào là nổ ra tim vàng tim hồng kèm một lời nhắn.

40 lời nhắn chia bốn nhóm: **tinh thần · công việc · quan tâm · thương em**.
Mỗi lần chạm ra một lời khác nhau, hết 40 câu mới quay vòng lại.

---

## Chạy thử ngay trên máy

```bash
python3 serve.py
```

Nó in ra một mã QR ngay trong terminal — lấy điện thoại (cùng wifi) quét là vào được.
Muốn đổi cổng: `python3 serve.py 9000`.

## Đưa lên mạng cho người ngoài quét

Lần đầu, đăng nhập GitHub một lần (lệnh này mở trình duyệt):

```bash
gh auth login
```

Rồi:

```bash
./deploy.sh
```

Script sẽ: tạo repo → đẩy code lên → bật GitHub Pages → sinh `qr.png` + `qr-card.html`
trỏ đúng vào địa chỉ `https://<tên-github>.github.io/qr-heart/`.

Địa chỉ đó cố định, sống 24/7 kể cả khi tắt máy — nên mã QR in ra dùng được mãi.
Sửa gì trong trang thì chạy lại `./deploy.sh` là xong, QR không đổi.

Đã có địa chỉ riêng rồi thì tạo QR tay:

```bash
python3 make_qr.py https://dia-chi-cua-ban.com
```

---

## Cổng vào

Trang hỏi **tên của em** và **ngày sinh của em**:

| Câu hỏi | Trả lời đúng |
|---|---|
| Tên của em là gì? | `Phạm Thu Hương` hoặc `Hương` |
| Ngày sinh của em? | `08/09/2004` (gõ kiểu gì cũng được: `08092004`, `8/9/2004`, `08-09-2004`) |

Không dấu, viết hoa viết thường tuỳ ý — đều nhận.
Sai thì trang trả lời: *"Tao không yêu mày, cút ngay."*
Đúng một lần rồi thì máy đó nhớ luôn, lần sau khỏi hỏi lại.

Trong mã nguồn **không** có sẵn câu trả lời, chỉ có bản băm SHA-256 của
`tên|ngày sinh`, nên xem mã nguồn cũng không đoán ra được.

> ⚠️ Lưu ý thật lòng: đây là khoá cho vui, không phải bảo mật thật.
> Vì trang tĩnh nên ảnh `images/2.jpg` và các lời nhắn vẫn nằm trong mã nguồn —
> ai rành kỹ thuật, cố tình mở mã nguồn thì vẫn thấy được, dù không qua được ô đăng nhập.
> Muốn kín thật thì phải mã hoá nội dung bằng chính câu trả lời — nói một tiếng là làm được.

## Muốn sửa nội dung

Mở `index.html`, tất cả nằm gần cuối file:

- `TEN_EM`, `KY_TEN` — tên hiển thị trên tiêu đề và chữ ký cuối mỗi lời nhắn.
- `LOI_NHAN` — danh sách lời nhắn, mỗi dòng là `['Nhãn','Nội dung']`. Thêm bớt thoải mái.
- `LOI_CUOI` — câu hiện ra khi đã đọc hết một vòng.
- `KHOA_DUNG` — bản băm câu trả lời. Đổi tên/ngày sinh thì tạo băm mới bằng:

  ```bash
  python3 - <<'EOF'
  import hashlib
  print(hashlib.sha256('ten khong dau|ddmmyyyy'.encode()).hexdigest())
  EOF
  ```

Ảnh nền là `images/2.jpg` — thay ảnh khác thì để cùng tên, hoặc sửa dòng
`<div class="photo"><img src="images/2.jpg">` trong `index.html`.

## Các file

| File | Việc |
|---|---|
| `index.html` | Toàn bộ trang — không phụ thuộc gì ngoài ảnh nền và font Google |
| `serve.py` | Chạy trang trong wifi nhà, in QR ra terminal |
| `make_qr.py` | Tạo `qr.png` + `qr-card.html` (thiệp in) từ một địa chỉ |
| `deploy.sh` | Đẩy lên GitHub Pages rồi tạo QR trỏ vào đó |
| `vendor/segno` | Thư viện tạo QR thuần Python, gói sẵn nên không cần cài gì |
