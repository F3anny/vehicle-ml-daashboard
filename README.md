# Fleetwise — Vehicle ML Django Dashboard

Implementation of the supplied Vehicle ML Django Dashboard tutorial: Django project `config`, app `vehicles`, CSV source in `data/vehicles_ml_dataset.csv`, pandas manufacturer frequency table, template at `vehicles/templates/vehicles/index.html`, and the dashboard at `/`.

The frontend adds a responsive workspace layout, Plotly charts, summary statistics, manufacturer/fuel/search filters, a vehicle preview, and CSV export of the current selection. Bootstrap and Plotly are served locally. Google Fonts are optional; system fonts work offline.

## Run on Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/. If PowerShell blocks activation, use `venv\Scripts\python.exe` in place of `python`; activation is optional.

## Data

The dashboard uses 10,000 vehicle records from the supplied `vehicles_ml_dataset.csv`. The local copy in `data/vehicles_ml_dataset.csv` includes only vehicle fields; client names, demographics, professions, and income fields are excluded from both the dashboard and exports. The original file in Downloads is unchanged.

Inventory shows body type because the dataset has no model column. Record IDs are generated sequentially for display. Selling prices are shown without a currency symbol because the source does not identify a currency. Fuel labels are capitalized for display. The tutorial describes descriptive analysis, not predictive model training.

Required columns: `vehicle_id`, `manufacturer`, `body_type`, `year`, `fuel_type`, `kilometers_driven`, `selling_price`. Numeric columns must contain numbers; required fields cannot be empty. The dashboard reloads the file on each request. Inventory previews 20 records; export includes every matching record. The previous synthetic dataset and generator remain in `dummy_data/` for reference and are no longer loaded.

## Validate

```powershell
python manage.py check
python manage.py test
```

Development settings default to localhost and DEBUG on. For hosting, set a private `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=0`, configure allowed hosts, and serve collected static files using a production web server.
