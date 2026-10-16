# Đề 34: Hệ thống Quản lý Hợp đồng (Contract Management System)

Dự án bài tập lớn xây dựng hệ thống quản lý hợp đồng kinh tế theo kiến trúc vi dịch vụ container hóa với **Django**, **PostgreSQL**, **Nginx (HTTPS + Security Headers)**, quản lý qua **Docker Compose** trên môi trường **Ubuntu WSL2** (`Ubuntu-Test`).

---

## 🏗️ Kiến trúc Commit 1

Commit 1 tập trung xây dựng nền tảng ứng dụng cốt lõi, bảo mật mạng và cổng vào HTTPS:

1. **Django App (`cm_django_web`)**:
   - Chạy trên Python 3.12, ứng dụng quản lý hợp đồng (`contracts`) có đầy đủ các model: Đối tác (`Partner`), Loại hợp đồng (`ContractType`), Hợp đồng (`Contract`).
   - Được container hóa với **Non-Root user** (`appuser`, UID `1001`).
   - WSGI server: **Gunicorn** với 3 workers.
2. **PostgreSQL 15 (`cm_postgres_db`)**:
   - Lưu trữ dữ liệu hệ thống trong mạng nội bộ `backend_net`.
   - **Tuyệt đối không công khai cổng ra máy host**.
   - Có cơ chế `healthcheck` tự động trước khi Django khởi động.
3. **Nginx Reverse Proxy (`cm_nginx_proxy`)**:
   - Cổng giao tiếp duy nhất ra bên ngoài, **chỉ mở cổng HTTPS 443** trên máy cục bộ.
   - Chứng chỉ tự ký SSL/TLS 2048-bit (TLSv1.2, TLSv1.3).
   - Tích hợp bộ **Security Headers**: HSTS, `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection`, `Referrer-Policy`, và `Content-Security-Policy`.
   - Phục vụ trực tiếp tập tin tĩnh (`/static/`) và tệp đính kèm (`/media/`).
4. **Phân tách mạng (Network Segmentation)**:
   - `frontend_net`: Kết nối Nginx $\leftrightarrow$ Django Web.
   - `backend_net`: Kết nối Django Web $\leftrightarrow$ PostgreSQL.

---

## 🚀 Hướng dẫn khởi chạy (Sử dụng WSL2 Ubuntu-Test)

Vì Docker Engine chạy trong môi trường WSL2 distro `Ubuntu-Test`, bạn có thể thực hiện theo một trong hai cách:

### Cách 1: Thao tác từ Windows PowerShell

1. **Khởi động toàn bộ hệ thống (Build và chạy nền)**:
   ```powershell
   wsl -d Ubuntu-Test bash -c "cd /mnt/d/ContractManagement && docker compose up -d --build"
   ```

2. **Kiểm tra trạng thái các container**:
   ```powershell
   wsl -d Ubuntu-Test bash -c "cd /mnt/d/ContractManagement && docker compose ps"
   ```

3. **Xem log hoạt động thời gian thực**:
   ```powershell
   wsl -d Ubuntu-Test bash -c "cd /mnt/d/ContractManagement && docker compose logs -f"
   ```

4. **Tạo tài khoản quản trị (Django Superuser)**:
   ```powershell
   wsl -d Ubuntu-Test bash -c "cd /mnt/d/ContractManagement && docker compose exec web python manage.py createsuperuser"
   ```

5. **Dừng toàn bộ hệ thống**:
   ```powershell
   wsl -d Ubuntu-Test bash -c "cd /mnt/d/ContractManagement && docker compose down"
   ```

---

### Cách 2: Mở Terminal Ubuntu WSL2 trực tiếp

Mở terminal WSL: `wsl -d Ubuntu-Test` và di chuyển đến thư mục dự án:
```bash
cd /mnt/d/ContractManagement

# Khởi động hệ thống
docker compose up -d --build

# Kiểm tra container
docker compose ps

# Tạo tài khoản admin
docker compose exec web python manage.py createsuperuser
```

---

## 🔍 Hướng dẫn kiểm thử Commit 1

### 1. Kiểm tra kết nối HTTPS và Security Headers bằng cURL

> **Lưu ý trên Windows 10:** Trong PowerShell 5.1, từ khóa `curl` là alias của `Invoke-WebRequest`. Do đó, bạn **bắt buộc dùng `curl.exe`** để gọi cURL gốc:

* **Từ Windows PowerShell:**
  ```powershell
  curl.exe -kI https://localhost
  ```
* **Hoặc từ WSL2 Ubuntu-Test:**
  ```bash
  wsl -d Ubuntu-Test curl -kI https://localhost
  ```

**Kết quả mong đợi**:
* Trả về mã trạng thái: `HTTP/1.1 200 OK` (hoặc `HTTP/2 200`).
* Xuất hiện các tiêu đề an ninh (Security Headers) không bị trùng lặp:
  * `strict-transport-security: max-age=31536000; includeSubDomains`
  * `x-content-type-options: nosniff` (duy nhất 1 dòng)
  * `x-frame-options: SAMEORIGIN` (giúp Django Admin an toàn và không bị chặn iframe)
  * `x-xss-protection: 1; mode=block`
  * `referrer-policy: strict-origin-when-cross-origin`
  * `content-security-policy: default-src 'self' ...`

### 2. Kiểm tra chuyển hướng HTTP sang HTTPS trong Docker

Khối chuyển hướng HTTP (cổng 80) sang HTTPS (cổng 443) được kiểm tra trực tiếp bên trong Docker network:
```powershell
wsl -d Ubuntu-Test bash -c "cd /mnt/d/ContractManagement && docker compose exec nginx wget --spider -S http://localhost 2>&1"
```
hoặc bằng lệnh cURL từ service `web`:
```powershell
wsl -d Ubuntu-Test bash -c "cd /mnt/d/ContractManagement && docker compose exec web curl -I http://nginx"
```
**Kết quả mong đợi**:
* Trả về mã chuyển hướng: `HTTP/1.1 301 Moved Permanently`.
* Tiêu đề vị trí chuyển tiếp: `Location: https://localhost/` (hoặc `Location: https://nginx/`).

### 3. Kiểm thử trên Trình duyệt Web

1. Mở trình duyệt và truy cập: [https://localhost](https://localhost)
2. Vì sử dụng chứng chỉ SSL tự ký (Self-signed Certificate), trình duyệt sẽ hiện cảnh báo bảo mật ban đầu. Nhấn **Nâng cao (Advanced)** $\rightarrow$ **Tiếp tục truy cập localhost (Proceed to localhost)**.
3. Giao diện trang chủ hiển thị tiêu đề **Hệ thống Quản lý Hợp đồng**, bảng điều khiển thống kê và các chỉ số bảo mật.
4. Truy cập trang quản trị: [https://localhost/admin](https://localhost/admin) và đăng nhập bằng tài khoản superuser.

### 4. Kiểm tra User Non-Root bên trong Container Django

Chạy lệnh để xác nhận tiến trình Django đang chạy dưới user `appuser` (UID 1001) thay vì `root`:
```powershell
wsl -d Ubuntu-Test bash -c "cd /mnt/d/ContractManagement && docker compose exec web id"
```
**Kết quả mong đợi**:
```text
uid=1001(appuser) gid=1001(appgroup) groups=1001(appgroup)
```

### 5. Kiểm tra cô lập mạng (PostgreSQL không mở port ra host)

Kiểm tra trực tiếp các cổng được công khai của container `cm_postgres_db` qua Docker Engine:
```powershell
wsl -d Ubuntu-Test docker port cm_postgres_db
```
**Kết quả mong đợi**:
* Lệnh không in ra bất kỳ dòng nào (kết quả rỗng), chứng minh cổng `5432` của PostgreSQL hoàn toàn không được map ra máy host mà chỉ tồn tại trong mạng nội bộ `contractmanagement_backend_net`.

---

## 📁 Danh sách tệp tin trong Commit 1

```text
.
├── .env.example
├── .env
├── .gitignore
├── README.md
├── docker-compose.yml
├── app/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   ├── manage.py
│   ├── contract_management/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── contracts/
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py
│       ├── admin.py
│       ├── views.py
│       ├── urls.py
│       ├── migrations/
│       │   ├── __init__.py
│       │   └── 0001_initial.py
│       └── templates/
│           └── contracts/
│               └── index.html
└── nginx/
    ├── conf.d/
    │   └── default.conf
    └── ssl/
        ├── generate_ssl.sh
        ├── cert.pem
        └── key.pem
```
