# ETL Football Project
Dự án cá nhân về quy trình ETL từ thu thập dữ liệu bóng cầu thủ đá từ trang thông tin chuyển nhượng Transfermarket bằng thư viện Selenium (Python), xử lí và làm sạch dữ liệu bằng Pandas và dbt, lưu trữ vào Hệ quản trị cơ sở dữ liệu (PostgreSQL) đến trực quan hóa dữ liệu bằng Microsoft Power BI

---

## ✅ Mô tả dự án
- Crawl dữ liệu từ trang chủ đến trang đích (trang chứa dữ liệu cần thu thập)
- Từ trang chủ (Home Page) -> Vào trang chứa thông tin các Giải đấu (COMPETITIONS) -> Lọc ra các giải đấu cần lấy (do mỗi trang giải đấu sẽ có đuôi url khác biệt, có thể xem trong Developer Tools) -> Vào từng giải đấu để lấy url của các CLB -> Vào từng CLB để lấy url của từng cầu thủ -> Trích xuất thông tin cầu thủ (tên, năm sinh, vị trí thi đấu, quốc tịch, clb chủ quản, giải đấu, số áo, giá trị chuyển nhượng, ngày cập nhật giá trị chuyển nhượng)
- Xử lí lỗi 403 bằng cách refresh trang sau 1 hàm delay ngẫu nhiên
- Khai báo và lưu dữ liệu thô vào Hệ cơ sở dữ liệu
- Xử lí dữ liệu thô thành dữ liệu sạch phụ vụ cho nhu cầu phân tích (reports/dashboards)

---
## 🏗️ Kiến trúc dự án
![Architecture](https://github.com/trungkien-011001/etl_football/blob/main/imgs/architecture.png)

---
## 🧱 Cấu trúc dự án

```bashbash
etl_football/
│
├── README.md
├── structure.txt
├── LICENSE
│
├── dbt_project/                	# dbt setup ✅
│   ├── dbt_project.yml
│   ├── models/
│	  ├── Staging/
│	  │	 ├── stg_players.sql
│	  │	 └── stg_schema.yml
│	  ├── Intermediate/
│	  │	 ├── int_players.sql
│	  │	 └── int_schema.yml
│	  └── Marts/
│		 ├── marts_players.sql
│		 └── marts_schema.yml
│
├── airflow-docker/                  # Airflow setup ✅
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
![postgres_schema](https://github.com/trungkien-011001/etl_football/blob/main/imgs/postgres_schema.png)

### dbt run
![dbt_run](https://github.com/trungkien-011001/etl_football/blob/main/imgs/dbt_run.png)

### Airflow DAGs
![Airflow_DAGS](https://github.com/trungkien-011001/etl_football/blob/main/imgs/airflow_dags.png)

### Power BI Overview Page (1)
![pbi_1](https://github.com/trungkien-011001/etl_football/blob/main/imgs/powerbi_dashboard_overview.png)

### Power BI Players Page (2)
![pbi_2](https://github.com/trungkien-011001/etl_football/blob/main/imgs/powerbi_dashboard_players.png)

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
