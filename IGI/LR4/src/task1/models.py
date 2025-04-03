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

        :return: The name of the object.
        """
        return self._name

    @property
    def country(self) -> str:
        """
        Returns the country attribute, which represents the country associated with the object instance.

        :return: The country value as a string.
        """
        return self._country

    @property
    def export_count(self) -> int:
        """
        Represents a property that retrieves the current count of exports.

        :return: The number of exports currently tracked by the instance.
        """
        return self._export_count


class ExportProductRepository:
    """
    Provides an in-memory repository for managing exported products.

    This class manages a collection of exported products, allowing addition of
    new products, retrieval of the stored products, and clearing the repository.
    It ensures that products are organized by their case-insensitive names.
    """

    def __init__(self):
        self._products: dict[str, list[ExportedProduct]] = {}

    @property
    def products(self) -> dict[str, list[ExportedProduct]]:
        """
        Returns a copy of the product dictionary.

        :return: A shallow copy of the product dictionary.
        """
        return self._products.copy()

    @products.setter
    def products(self, products: dict[str, list[ExportedProduct]]) -> None:
        """
        Sets the value of the products attribute.

        :param products: A dictionary where keys are strings representing product categories or identifiers,
        and the corresponding values are lists of ExportedProduct instances.
        """
        self._products = products.copy()

    def add_product(self, product: ExportedProduct):
        """
        Adds a product to the internal product storage.

        The method stores the provided product in a dictionary where the key is the
        lowercase version of the product name and the value is a list of products
        with the same name. If the product name already exists in the storage, the
        new product is appended to the existing list.

        :param product: The product to be added to the internal storage.
        """

        self._products.setdefault(product.name.lower(), []).append(product)

    def clear(self):
        """Clears all items from the internal product storage, making it empty."""

        self._products.clear()
