"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    description = factory.Faker("paragraph", nb_sentences=3)
    price = factory.Faker("random_number", digits=2)
    category = FuzzyChoice(
        choices=[
            "Electronics",
            "Clothing",
            "Home",
            "Books",
            "Toys & Games",
            "Beauty",
            "Sale",
        ]
    )
    available = FuzzyChoice(choices=[True, False])
    image_url = factory.Faker("image_url")
