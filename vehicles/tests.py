import os
import pandas as pd
from django.conf import settings
from django.test import TestCase
from .dashboard import manufacturer_counts

class DashboardTests(TestCase):
    def test_dashboard_totals_match_csv(self):
        response = self.client.get('/')
        data = pd.read_csv(settings.BASE_DIR / 'data/vehicles_ml_dataset.csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total'], len(data))
        self.assertEqual(manufacturer_counts(data)['Count'].sum(), len(data))
        self.assertContains(response, 'Manufacturer frequency')

    def test_combined_filters_and_export(self):
        filters = {'manufacturer': 'Toyota', 'fuel': 'Hybrid', 'q': 'sedan'}
        response = self.client.get('/', filters)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.context['total'], 0)
        for vehicle in response.context['vehicles']:
            self.assertEqual(vehicle['manufacturer'], 'Toyota')
            self.assertEqual(vehicle['fuel_type'], 'Hybrid')
            self.assertEqual(vehicle['body_type'], 'Sedan')
        export = self.client.get('/', {**filters, 'export': 'csv'})
        self.assertEqual(export['Content-Type'], 'text/csv')
        self.assertNotIn('client_name', export.content.decode())
        self.assertNotIn('estimated_income', export.content.decode())
        self.assertEqual(len(export.content.decode().splitlines()) - 1, response.context['total'])

    def test_no_results_and_literal_search(self):
        for query in ['no-such-vehicle', '.*', '<script>alert(1)</script>']:
            response = self.client.get('/', {'q': query})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['total'], 0)
            self.assertContains(response, 'No vehicles match')
            self.assertNotContains(response, '<script>alert(1)</script>')

    def test_source_path_does_not_depend_on_working_directory(self):
        original = os.getcwd()
        try:
            os.chdir(settings.BASE_DIR / 'dummy_data')
            self.assertEqual(self.client.get('/').status_code, 200)
        finally:
            os.chdir(original)
