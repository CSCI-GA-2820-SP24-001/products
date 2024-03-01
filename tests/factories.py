"""
Test Factory to make fake objects for testing
"""

import factory
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    description = factory.Faker("sentence")
    price = factory.Faker("random_number")
    category = factory.Faker("sentence")
    available = factory.Faker("boolean")
    image_url = factory.Faker("image_url")

    # Todo: Add your other attributes here...
