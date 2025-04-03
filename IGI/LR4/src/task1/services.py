from .models import ExportProductRepository


class ExportProductService(object):
    """
    A service for managing and processing export product information.

    This class provides functionalities to retrieve and manipulate
    product export data, such as fetching countries by product name,
    calculating total exports for a product, finding detailed product
    information, and sorting product records by country.
    """

    def __init__(self, repository: ExportProductRepository):
        self._repo = repository

    def get_countries_by_product_name(self, product_name: str) -> set[str]:
        """
        Fetch the set of countries associated with a given product name.

        :param product_name: The name of the product to look up in the repository.

        :return: A set containing the names of countries associated with the specified product name.
        """
        return set(product.country for product in self._repo.products.get(product_name))

    def get_total_export(self, product_name: str) -> int:
        """
        Calculates the total export count for a specified product.

        :param product_name: The name of the product for which the total export count is to be calculated.

        :return: The total sum of export counts for the specified product.
        """

        return sum(product.export_count for product in self._repo.products.get(product_name))

    def find_product_info(self, product_name: str) -> dict | None:
        """
        Finds and retrieves detailed product information including the countries where the product
        is exported and the total export count.

        :param product_name: The name of the product for which the information is to be fetched.

        :return: A dictionary containing the product name, the countries exporting the product, and
            the total export value. Returns None if no data exists for the specified product name.
        """

        countries = self.get_countries_by_product_name(product_name)
        if not countries:
            return None

        return {
            'product name': product_name,
            'countries': countries,
            'total_export': self.get_total_export(product_name)
        }

    def sort_by_country(self, reverse: bool = False):
        """
        Sorts product records by their country attribute.

        :param reverse: If True, the list is sorted in descending order by country. Defaults to False.
        """

        for product_record in self._repo.products.values():
            product_record.sort(key=lambda product: product.country, reverse=reverse)
