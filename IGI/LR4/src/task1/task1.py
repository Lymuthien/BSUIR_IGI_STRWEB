from .models import ClearingExportProductRepository
from .serializers import ExportProductFileHandler, PickleExportProductFileHandler, CSVExportProductFileHandler
from .services import ExportProductService
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask


class Task1(ITask):
    """
    The source data in the form of a dictionary are placed in files (pickle and csv).
    Data reading, searching, and sorting are organized.
    The summary of exported goods indicates: the name of the product, the country exporting the product,
    the volume of the supplied batch in pieces. A list of countries to which the product is exported and
    the total volume of its export are printed. Information about the product entered from the keyboard displayed.
    """

    def __init__(self, filepath: str):
        self._repo = ClearingExportProductRepository()
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
