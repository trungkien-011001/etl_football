# Football Data ETL Pipeline
Dự án cá nhân về quy trình ETL từ thu thập dữ liệu bóng cầu thủ đá từ trang thông tin chuyển nhượng Transfermarket bằng thư viện Selenium (Python), xử lí và làm sạch dữ liệu bằng Pandas và dbt, lưu trữ vào Hệ quản trị cơ sở dữ liệu (PostgreSQL) đến trực quan hóa dữ liệu bằng Microsoft Power BI

---

## ✅ Mô tả dự án
- Crawl dữ liệu từ trang chủ đến trang đích (trang chứa dữ liệu cần thu thập)
- Từ trang chủ (Home Page) -> Vào trang chứa thông tin các Giải đấu (COMPETITIONS) -> Lọc ra các giải đấu cần lấy (do mỗi trang giải đấu sẽ có đuôi url khác biệt, có thể xem trong Developer Tools) -> Vào từng giải đấu để lấy url của các CLB -> Vào từng CLB để lấy url của từng cầu thủ (tên, năm sinh, vị trí thi đấu, quốc tịch, clb chủ quản, giải đấu, số áo, giá trị chuyển nhượng, ngày cập nhật giá trị chuyển nhượng)
- Xử lí lỗi 403 bằng cách refresh trang sau 1 hàm delay ngẫu nhiên
- Khai báo và lưu dữ liệu thô vào Hệ cơ sở dữ liệu
- Xử lí dữ liệu thô thành dữ liệu sạch phụ vụ cho nhu cầu phân tích (reports/dashboards)

---
## 🏗️ Kiến trúc dự án

<img width="1650" height="800" alt="Architecture" src="https://github.com/user-attachments/assets/e669aa2c-09e1-4381-bd31-ad6013c666f7" />

---
## 🧱 Cấu trúc dự án

```bashbash
etl_football/
│
├── README.md
│
├── dbt_project/                	 # dbt setup ✅
│   ├── dbt_project.yml
│   ├── models/
│	  ├── Staging
│	  │	 ├── stg_players.sql
│	  │	 └── stg_schema.yml
│	  ├── Intermediate
│	  │	 ├── int_players.sql
│	  │	 └── int_schema.yml
│	  └── Marts
│			 ├── marts_players.sql
│			 └── marts_schema.yml
│
├── airflow-docker                  # Airflow setup ✅
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── dags/
│   └── scripts/
│      ├── etl_premier_league.py
│      ├── etl_laliga.py
│      ├── etl_serie_a.py
│      ├── etl_bundesliga.py
│      └── etl_ligue_1.py
│
├── imgs/                         	  # Architecture, dashboards ✅
│   ├── architecture.png
│   ├── dbt_run.png
│   ├── airflow_dags.png
│   ├── postgres_schema.png
│   ├── powerbi_dashboard_overview.png
│   ├── powerbi_dashboard_players.png
│   └── project_structure.png
└──
```

---
## 📸 Hình ảnh minh họa
### Database schema (Postgres)
<img width="950" height="550" alt="postgres_schema" src="https://github.com/user-attachments/assets/a8aa4c40-9857-4e9b-b705-eb14dab5a347" />

### dbt run
<img width="862" height="463" alt="dbt_run" src="https://github.com/user-attachments/assets/35e55419-a003-4665-a869-7573b3a29a37" />

### Airflow DAGs
<img width="950" height="550" alt="airflow_dags" src="https://github.com/user-attachments/assets/748637d2-1fd4-4787-82ec-52f13a21ddf9" />

### Power BI Overview Page (1)
<img width="572" height="398" alt="powerbi_dashboard_overview" src="https://github.com/user-attachments/assets/b4d44317-e10d-48c0-9393-6ff07589445a" />

### Power BI Players Page (2)
<img width="476" height="374" alt="powerbi_dashboard_players" src="https://github.com/user-attachments/assets/a0a5286c-b6ad-41fa-a55b-b7585c796895" />

---
## 🛠️ Công cụ
-------------------------------------------------------------------------
- **Ngôn ngữ**: Python 3.10+
- **Web Scraping**: Selenium, Google Chrome + Chrome Driver
- **Công cụ biến đổi dữ liệu**: pandas, dbt
- **Database**: PostgreSQL
- **Quản lý pipeline**: Apache Airflow (Dockerized)
- **Trực quan hóa dữ liệu**: Power BI
- **Môi trường**: Window Subsystem for Linux (WSL), Docker
-------------------------------------------------------------------------

---
## 📄 License
MIT — dùng cho mục đích học tập & nghiên cứu
