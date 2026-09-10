#!/usr/bin/env bash
#
# Đẩy trang lên GitHub Pages rồi tạo mã QR trỏ tới địa chỉ công khai đó.
#
#   ./deploy.sh                 -> repo tên "qr-heart"
#   ./deploy.sh ten-repo-khac
#
# Lần đầu chạy: phải đăng nhập GitHub trước bằng   gh auth login
#
set -e
cd "$(dirname "$0")"

REPO="${1:-qr-heart}"

if ! gh auth status >/dev/null 2>&1; then
  echo
  echo "  Chưa đăng nhập GitHub."
  echo "  Chạy lệnh này trước (nó sẽ mở trình duyệt):"
  echo
  echo "      gh auth login"
  echo
  exit 1
fi

USER=$(gh api user -q .login)

# --- 1. commit ---
[ -d .git ] || git init -b main -q
git add -A
git commit -q -m "Cập nhật trang trái tim" 2>/dev/null || echo "  (không có gì mới để commit)"

# --- 2. đẩy lên GitHub ---
if git remote get-url origin >/dev/null 2>&1; then
  echo "  Đẩy code lên $(git remote get-url origin) ..."
  git push -q -u origin main
else
  echo "  Tạo repo mới: $USER/$REPO ..."
  gh repo create "$REPO" --public --source=. --remote=origin --push
fi

# --- 3. bật GitHub Pages ---
echo "  Bật GitHub Pages ..."
gh api -X POST "repos/$USER/$REPO/pages" \
   -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
|| gh api -X PUT "repos/$USER/$REPO/pages" \
   -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
|| echo "  (Pages đã bật sẵn rồi)"

URL="https://${USER}.github.io/${REPO}/"

# --- 4. tạo QR ---
echo
echo "  Trang sẽ sống ở: $URL"
echo "  (GitHub cần khoảng 1-2 phút để lên sóng lần đầu)"
echo
python3 make_qr.py "$URL"
echo
echo "  Xong. Mở qr-card.html ra in, hoặc gửi thẳng qr.png. 💗"
echo
