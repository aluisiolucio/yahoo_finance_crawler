import csv
import os

from yahoo_finance_crawler.csv_exporter import CSVExporter


def test_export_to_csv(tmp_path):
    data = [
        {
            'symbol': 'AMX.BA',
            'name': 'América Móvil, S.A.B. de C.V.',
            'price': '2089.00',
        },
        {'symbol': 'NOKA.BA', 'name': 'Nokia Corporation', 'price': '557.50'},
    ]
    csv_file = tmp_path / 'output.csv'

    CSVExporter.export_to_csv(data, csv_file)

    assert os.path.exists(csv_file)

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert rows == data
