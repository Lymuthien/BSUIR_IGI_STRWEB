from .models import ExportProductRepository
from .serializers import ExportProductFileHandler, PickleExportProductFileHandler, CSVExportProductFileHandler
from .services import ExportProductService
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program


class Task1(object):
    """
    This class manages export product processing by utilizing different file handlers (pickle and csv)
    and providing functionalities to find, sort and retrieve product information.
    """

    def __init__(self, filepath: str):
        self._repo = ExportProductRepository()
        self._service = ExportProductService(self._repo)
        self._export_methods: dict[str, ExportProductFileHandler] = {
            'pickle': PickleExportProductFileHandler(),
            'csv': CSVExportProductFileHandler()
        }
        self._filepath = filepath

    @repeating_program
    def run(self):
        """
        This method repeatedly executes a program's operations. It facilitates
        exporting data from a repository in a user-specified format, such as pickle
        or csv, and then processes the repository data by sorting and searching product
        information.

        :raise ValueError: If provided input for the export method is not valid.
        """

        export_method = input_with_validating(lambda msg: msg.lower().strip() in self._export_methods,
                                              'Enter export method (pickle, csv): ').lower().strip()
        self._export_methods[export_method].load(self._repo, f'{self._filepath}.{export_method}')
        self._service.sort_by_country()

        self._find_product_info()

    def _find_product_info(self) -> dict | None:
        """
        Find product information based on user input and display the results.

        :return: The product information retrieved, or None if no such product exists or an error occurs.
        """

        product_name = input('Enter product name: ').lower().strip()
        try:
            print(*self._service.find_product_info(product_name).items(), sep='\n')
        except Exception as e:
            print('No item.')
