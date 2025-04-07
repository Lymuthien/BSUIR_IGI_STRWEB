import csv
import pickle
from abc import ABC, abstractmethod

from .models import ClearingExportProductRepository, ExportedProduct


class ExportProductFileHandler(ABC):
    """Abstract base class responsible for handling the export and import of product files."""

    @abstractmethod
    def save(self, repo: ClearingExportProductRepository, filename: str): ...

    @abstractmethod
    def load(self, repo: ClearingExportProductRepository, filename: str): ...


class PickleExportProductFileHandler(ExportProductFileHandler):
    """Handles the export and import of product files using the pickle module."""

    def save(self, repo: ClearingExportProductRepository, filename: str):
        """
        Saves the products from the given repository to a file in binary format using pickle.

        :param repo: The repository containing products to be serialized and saved.
        :param filename: The name of the file where the serialized data will be stored.
        """

        data = pickle.dumps(repo.products)
        with open(filename, 'wb') as file:
            file.write(data)

    def load(self, repo: ClearingExportProductRepository, filename: str):
        """
        Loads product data from a file and updates the repository with the loaded products.

        :param repo: The repository where loaded products will be stored.
        :param filename: The name of the file to load product data from.

        :raise FileNotFoundError: If the specified file does not exist.
        :raise EOFError: If an unexpected end-of-file condition is encountered when reading.
        :raise pickle.PickleError: If there is an error during the unmarshalling of objects.
        """

        with open(filename, 'rb') as file:
            products = pickle.load(file)
        repo.products = products


class CSVExportProductFileHandler(ExportProductFileHandler):
    """Handles operations related to exporting and importing product data to and from CSV files."""

    def save(self, repo: ClearingExportProductRepository, filename: str):
        """
        Saves product data from a given repository to a CSV file.

        :param repo: A repository containing product data to be exported to the CSV file.
        :param filename: The name of the file where the product data will be written.
        """

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Country', 'Count'])
            for product_records in repo.products.values():
                for product in product_records:
                    writer.writerow([product.name, product.country, product.export_count])

    def load(self, repo: ClearingExportProductRepository, filename: str):
        """
        Load data from a CSV file into the repository.

        :param repo: The repository where the exported product data will be stored.
            It is cleared before loading new data.
        :param filename: The path to the CSV file containing exported product data to load.
        """

        repo.clear()
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                repo.add_product(ExportedProduct(
                    row['Name'], row['Country'], row['Count']
                ))
