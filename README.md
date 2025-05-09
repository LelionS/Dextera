# 🌱 Dextera

## 🌿 Custom Django Admin UI for Varieties, Beds, Bays, and Houses

Dextera provides a clean, responsive admin-style interface for managing agricultural records like **Varieties**, **Beds**, **Bays**, and **Houses**, designed to work outside of Django’s default admin panel.

Built with:
```

- ✅ [PicoCSS](https://picocss.com/) for minimal UI styling
- ✅ [DataTables](https://datatables.net/) for enhanced tables (filters, export, print)
- ✅ Django views and templates with full control
- ✅ Staff-only access for sensitive operations

```

## 🚀 Features
```
- ✅ Fully responsive, mobile-friendly UI
- ✅ Column-level filtering and global search
- ✅ Export to CSV, Excel, PDF
- ✅ Printable view that respects filters
- ✅ Light blue UI background and compact row layout
- ✅ Standalone UI, separate from Django admin
- ✅ Staff-only access for all custom tools

```

## 📁 Project Structure (Simplified)
```
dextera/
├── dextera/ # Project settings
├── formflow/ # Main app (models, views, templates)
├── templates/
│ └── staff/ # UI templates for varieties, beds, etc.
├── static/ # Custom JS/CSS
├── manage.py
└── requirements.txt

```

---

## 🔒 Access Control

All staff UI views are protected using:

```python
@user_passes_test(lambda u: u.is_staff)


```
Usage
```
git clone https://github.com/LelionS/dextera.git
cd dextera

python3 -m venv venv
source venv/bin/activate

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

```
---

🔐 Access Admin and Staff Interfaces
You can access the dashboards at:
```

🛠 Admin Panel: http://127.0.0.1:8000/admin/

📋 Staff Dashboard: http://127.0.0.1:8000/staff/dashboard/

