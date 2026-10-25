"""Generate reproducible synthetic data; no real vehicle records are used."""
import csv
import random
from pathlib import Path

def generate():
    rng = random.Random(42)
    brands = {
        'Toyota': ['Corolla', 'RAV4', 'Camry'], 'Volkswagen': ['Golf', 'Tiguan', 'Polo'],
        'Ford': ['Focus', 'Explorer', 'Escape'], 'BMW': ['320i', 'X3', 'X5'],
        'Mercedes-Benz': ['C200', 'GLC', 'A180'], 'Honda': ['Civic', 'CR-V', 'Accord'],
        'Hyundai': ['Tucson', 'Elantra', 'Santa Fe'], 'Nissan': ['Qashqai', 'X-Trail', 'Sentra'],
        'Kia': ['Sportage', 'Sorento', 'Rio'], 'Tesla': ['Model 3', 'Model Y', 'Model S'],
    }
    rows = []
    for index in range(1, 1001):
        brand = rng.choices(list(brands), weights=[22, 15, 13, 10, 9, 9, 8, 6, 5, 3])[0]
        year = rng.randint(2015, 2025)
        fuel = 'Electric' if brand == 'Tesla' else rng.choices(['Petrol', 'Diesel', 'Hybrid', 'Electric'], [57, 26, 14, 3])[0]
        mileage = max(500, (2026-year)*rng.randint(6500, 18000))
        premium = 18000 if brand in ['BMW', 'Mercedes-Benz', 'Tesla'] else 0
        price = max(4500, 31000 + premium - (2026-year)*1800 + rng.randint(-4500, 7500))
        rows.append([f'VH-{index:04d}', brand, rng.choice(brands[brand]), year, fuel, mileage, price])
    with Path(__file__).with_name('vehicles_data_1000.csv').open('w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['vehicle_id', 'manufacturer', 'model', 'year', 'fuel_type', 'mileage_km', 'price_usd'])
        writer.writerows(rows)

if __name__ == '__main__':
    generate()
