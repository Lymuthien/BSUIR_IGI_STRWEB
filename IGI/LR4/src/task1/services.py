from .models import ExportProductRepository


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