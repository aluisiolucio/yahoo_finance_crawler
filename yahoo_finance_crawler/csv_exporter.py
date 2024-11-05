import csv


class CSVExporter:
    @staticmethod
    def export_to_csv(data: list, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f'\nDados exportados para {filename} com sucesso!')
