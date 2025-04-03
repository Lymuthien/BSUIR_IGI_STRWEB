from .models import ExportProductRepository
from .serializers import ExportProductFileHandler, PickleExportProductFileHandler, CSVExportProductFileHandler
from .services import ExportProductService
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program


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
