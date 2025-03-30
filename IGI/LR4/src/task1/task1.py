import csv
import pickle
from abc import ABC, abstractmethod

from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program


# models
class ExportedProduct(object):
    def __init__(self, name: str, country: str, export_count: int | str):
        self._name = name
        self._country = country
        self._export_count = int(export_count)

    @property
    def name(self) -> str:
        return self._name

    @property
    def country(self) -> str:
        return self._country

    @property
    def export_count(self) -> int:
        return self._export_count


# models
class ExportProductRepository:
    def __init__(self):
        self._products: dict[str, list[ExportedProduct]] = {}

    @property
    def products(self) -> dict[str, list[ExportedProduct]]:
        return self._products.copy()

    @products.setter
    def products(self, products: dict[str, list[ExportedProduct]]) -> None:
        self._products = products.copy()

    def add_product(self, product: ExportedProduct):
        self._products.setdefault(product.name.lower(), []).append(product)

    def clear(self):
        self._products.clear()


# services
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


# services
class ExportProductService(object):
    def __init__(self, repository: ExportProductRepository):
        self._repo = repository

    def get_countries_by_product_name(self, product_name: str) -> set[str]:
        return set(product.country for product in self._repo.products.get(product_name))

    def get_total_export(self, product_name: str) -> int:
        return sum(product.export_count for product in self._repo.products.get(product_name))

    def find_product_info(self, product_name: str) -> dict | None:
        countries = self.get_countries_by_product_name(product_name)
        if not countries:
            return None

        return {
            'product name': product_name,
            'countries': countries,
            'total_export': self.get_total_export(product_name)
        }

    def sort_by_country(self, reverse: bool = False):
        for product_record in self._repo.products.values():
            product_record.sort(key=lambda product: product.country, reverse=reverse)


class Task1(object):
    def __init__(self):
        self._repo = ExportProductRepository()
        self._service = ExportProductService(self._repo)
        self._export_methods: dict[str, ExportProductFileHandler] = {'pickle': PickleExportProductFileHandler(),
                                                                     'csv': CSVExportProductFileHandler()}

    @repeating_program
    def run(self):
        export_method = input_with_validating(lambda msg: msg.lower().strip() in self._export_methods,
                                              'Enter export method (pickle, csv): ').lower().strip()
        self._export_methods[export_method].load(self._repo, f'data/products.{export_method}')
        self._service.sort_by_country()

        self._find_product_info()

    def _find_product_info(self) -> dict | None:
        product_name = input('Enter product name: ').lower().strip()
        try:
            print(*self._service.find_product_info(product_name).items(), sep='\n')
        except Exception as e:
            print('No item.')
