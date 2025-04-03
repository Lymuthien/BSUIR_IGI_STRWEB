class ExportedProduct(object):
    """
    Represents a product that is exported from one country to another.

    This class encapsulates the details of a product that is being exported,
    such as the product name, the country it is exported from, and the number of
    times the product has been exported. It provides read-only access to these
    attributes through its properties.
    """

    def __init__(self, name: str, country: str, export_count: int | str):
        self._name = name
        self._country = country
        self._export_count = int(export_count)

    @property
    def name(self) -> str:
        """
        Provides the name of the object as a string.
        The name represents the specific identifier or label associated with the instance of the class.

        :return: The name of the object.
        """
        return self._name

    @property
    def country(self) -> str:
        """
        Returns the country attribute.

        This property retrieves the value of the _country attribute, which represents the
        country associated with the object instance.

        :return: str: The country value as a string.
        """
        return self._country

    @property
    def export_count(self) -> int:
        return self._export_count


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
