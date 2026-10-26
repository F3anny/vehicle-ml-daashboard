import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from .dashboard import charts, frequency_table, manufacturer_counts

def dashboard_view(request):
    try:
        source = pd.read_csv(settings.BASE_DIR / 'data' / 'vehicles_ml_dataset.csv')
        required = {'vehicle_id', 'manufacturer', 'body_type', 'year', 'fuel_type', 'kilometers_driven', 'selling_price'}
        if not required.issubset(source.columns) or source[list(required)].isna().any().any():
            raise ValueError('The CSV has missing columns or values.')
        for column in ['year', 'kilometers_driven', 'selling_price']:
            source[column] = pd.to_numeric(source[column], errors='raise')
    except (OSError, ValueError, pd.errors.ParserError) as error:
        return render(request, 'vehicles/error.html', {'error': str(error)}, status=503)
    df = source.copy()
    manufacturer = request.GET.get('manufacturer', '')
    fuel = request.GET.get('fuel', '')
    query = request.GET.get('q', '').strip()
    if manufacturer:
        df = df[df.manufacturer == manufacturer]
    if fuel:
        df = df[df.fuel_type == fuel]
    if query:
        df = df[df[['manufacturer', 'body_type', 'vehicle_id']].astype(str).apply(
            lambda col: col.str.contains(query, case=False, regex=False)).any(axis=1)]
    if request.GET.get('export') == 'csv':
        response = HttpResponse(df.to_csv(index=False), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vehicles_filtered.csv"'
        return response
    bar, donut = charts(df)
    counts = manufacturer_counts(df)
    top = counts.iloc[0] if len(counts) else None
    context = {
        'frequency_table': frequency_table(df), 'bar_chart': bar, 'donut_chart': donut,
        'total': len(df), 'source_total': len(source), 'brands': df.manufacturer.nunique(),
        'avg_price': df.selling_price.mean() if len(df) else 0,
        'avg_mileage': df.kilometers_driven.mean() if len(df) else 0,
        'top_brand': top['Manufacturer'] if top is not None else 'No data',
        'top_share': round(top['Count'] / len(df) * 100, 1) if top is not None else 0,
        'manufacturers': sorted(source.manufacturer.unique()), 'fuels': sorted(source.fuel_type.unique()),
        'selected_manufacturer': manufacturer, 'selected_fuel': fuel, 'query': query,
        'vehicles': df.head(20).to_dict('records'),
    }
    return render(request, 'vehicles/index.html', context)
