"""
TestProduct API Service Test Suite
"""
# pylint disable=fixme
import os
import logging
from unittest import TestCase

# from urllib.parse import quote_plus
from wsgi import app
from service.common import status
from service.models import db, Product
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/products"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test product",
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(new_product["price"], test_product.price)
        self.assertEqual(new_product["category"], test_product.category)
        self.assertEqual(new_product["available"], test_product.available)
        self.assertEqual(new_product["image_url"], test_product.image_url)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(new_product["price"], test_product.price)
        self.assertEqual(new_product["category"], test_product.category)
        self.assertEqual(new_product["available"], test_product.available)
        self.assertEqual(new_product["image_url"], test_product.image_url)

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product(self):
        """It should Get a single Product"""
        # get the id of a product
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """It should not Get a Product thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_update_product(self):
        """It should Update an existing Product"""
        # create a product to update
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = response.get_json()
        logging.debug(new_product)
        new_product["category"] = "unknown"
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["category"], "unknown")

    # Todo work on querying products by CATEGORY
    #    def test_query_product_list_by_category(self):
    #     """It should Query Products by category"""
    #     products = self._create_category(10)
    #     test_category = str(products[0].category)
    #     category_products = [
    #         product for product in products if str(product.category) == test_category
    #     ]
    #     response = self.client.get(
    #         BASE_URL, query_string=f"category={quote_plus(test_category)}"
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     data = response.get_json()
    #     self.assertEqual(len(data), len(category_products))
    #     # check the data just to be sure
    #     for product in data:
    #         self.assertEqual(product["category"], test_category)

    ######################################################################
    #  T E S T   A C T I O N S
    ######################################################################

    # todo work on purchase and purchase not available in next sprint
    # def test_purchase_a_product(self):
    #     """It should Purchase a Product"""
    #     products = self._create_products(10)
    #     available_products = [
    #         product for product in products if product.available is True
    #     ]
    #     product = available_products[0]
    #     response = self.client.put(f"{BASE_URL}/{product.id}/purchase")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     response = self.client.get(f"{BASE_URL}/{product.id}")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     data = response.get_json()
    #     logging.debug("Response data: %s", data)
    #     self.assertEqual(data["available"], False)

    # def test_purchase_not_available(self):
    #     """It should not Purchase a Product that is not available"""
    #     products = self._create_products(10)
    #     unavailable_products = [
    #         product for product in products if product.available is False
    #     ]
    #     product = unavailable_products[0]
    #     response = self.client.put(f"{BASE_URL}/{product.id}/purchase")
    #     self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a product id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_product_no_data(self):
        """It should not Create a Product with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """It should not Create a Product with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_product_wrong_content_type(self):
        """It should not Create a Product with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_product_bad_available(self):
        """It should not Create a Product with bad available data"""
        test_product = ProductFactory()
        logging.debug(test_product)
        # change available to a string
        test_product.available = "yes"
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_bad_price(self):
        """It should not Create a Product with bad price data"""
        test_product = ProductFactory()
        logging.debug(test_product)
        # change price to a bad string
        test_product.price = "no"  # wrong case
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_product_bad_category(self):
    #     """It should not Create a Product with bad category data"""
    #     test_product = ProductFactory()
    #     logging.debug(test_product)
    #     # change category to a bad int
    #     test_product.category = 3  # wrong case
    #     response = self.client.post(BASE_URL, json=test_product.serialize())
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
