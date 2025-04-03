import csv
import pickle
from abc import ABC, abstractmethod

from .models import ExportProductRepository, ExportedProduct


class ExportProductFileHandler(ABC):
    @abstractmethod
    def save(self, repo: ExportProductRepository, filename: str): ...

    @abstractmethod
    def load(self, repo: ExportProductRepository, filename: str): ...


class PickleExportProductFileHandler(ExportProductFileHandler):
    def save(self, repo: ExportProductRepository, filename: str):
        data = pickle.dumps(repo.products)
        with open(filename, 'wb') as file:
            file.write(data)

    def load(self, repo: ExportProductRepository, filename: str):
        with open(filename, 'rb') as file:
            products = pickle.load(file)
        repo.products = products


class CSVExportProductFileHandler(ExportProductFileHandler):
    def save(self, repo: ExportProductRepository, filename: str):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Country', 'Count'])
            for product_records in repo.products.values():
                for product in product_records:
                    writer.writerow([product.name, product.country, product.export_count])

    def load(self, repo: ExportProductRepository, filename: str):
        repo.clear()
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                repo.add_product(ExportedProduct(
                    row['Name'], row['Country'], row['Count']
                ))
