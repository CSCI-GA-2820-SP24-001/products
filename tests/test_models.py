"""
Test cases for Product Model
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import Product, DataValidationError, db
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
# pylint: disable=duplicate-code
class TestCaseBase(TestCase):
    """Base Test Case for Common Setup"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()


######################################################################
#  P R O D U C T  M O D E L   T E S T   C A S E S
######################################################################
class TestProductModel(TestCaseBase):
    """Product Model CRUD Tests"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should create a Product"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)
        found = Product.all()
        self.assertEqual(len(found), 1)
        data = Product.find(product.id)
        self.assertEqual(data.id, product.id)
        self.assertEqual(data.name, product.name)
        self.assertEqual(data.description, product.description)
        self.assertEqual(data.price, product.price)
        self.assertEqual(data.category, product.category)
        self.assertEqual(data.available, product.available)
        self.assertEqual(data.image_url, product.image_url)
        self.assertEqual(data.like, product.like)

    def test_delete_a_product(self):
        """It should delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch it back
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.category, product.category)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.image_url, product.image_url)
        self.assertEqual(found_product.like, product.like)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        logging.debug(product)
        self.assertIsNotNone(product.id)
        # Change it an save it
        product.category = "electronics"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.category, "electronics")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].category, "electronics")

    def test_update_no_id(self):
        """It should not Update a Product with no id"""
        product = ProductFactory()
        product.create()
        logging.debug(product)
        product.id = None
        self.assertRaises(DataValidationError, product.update)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        # Create 5 Products
        for _ in range(5):
            product = ProductFactory()
            product.create()
        # See if we get back 5 products
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_serialize_a_product(self):
        """It should serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("description", data)
        self.assertEqual(data["description"], product.description)
        self.assertIn("price", data)
        self.assertEqual(data["price"], product.price)
        self.assertIn("category", data)
        self.assertEqual(data["category"], product.category)
        self.assertIn("available", data)
        self.assertEqual(data["available"], product.available)
        self.assertIn("image_url", data)
        self.assertEqual(data["image_url"], product.image_url)
        self.assertIn("like", data)
        self.assertEqual(data["like"], product.like)

    def test_deserialize_a_product(self):
        """It should de-serialize a Product"""
        data = ProductFactory().serialize()
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.description, data["description"])
        self.assertEqual(product.price, data["price"])
        self.assertEqual(product.category, data["category"])
        self.assertEqual(product.available, data["available"])
        self.assertEqual(product.image_url, data["image_url"])
        self.assertEqual(product.like, data["like"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Product with missing data"""
        data = {
            "id": 1,
            "name": "name",
            "description": "description",
            "price": "price",
            "category": "category",
        }
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_available(self):
        """It should not deserialize a bad available attribute"""
        data = {"available": "yes"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_category(self):
        """It should not deserialize a bad category attribute"""
        data = {"category": "electronics"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCaseBase):
    """Product Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.delete)


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestCaseBase):
    """Product Model Query Tests"""

    def test_find_product(self):
        """It should Find a Product by ID"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        logging.debug(products)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 5)
        # find the 2nd product in the list
        product = Product.find(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.price, products[1].price)
        self.assertEqual(product.category, products[1].category)
        self.assertEqual(product.available, products[1].available)
        self.assertEqual(product.description, products[1].description)
        self.assertEqual(product.image_url, products[1].image_url)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        category = products[0].category
        count = len([product for product in products if product.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        available = products[0].available
        count = len([product for product in products if product.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, available)

    # def test_find_by_price(self):
    #     """It should Find Products by Price"""
    #     products = ProductFactory.create_batch(10)
    #     for product in products:
    #         product.create()
    #     price = products[0].price
    #     count = len([product for product in products if product.price == price])
    #     found = Product.find_by_price(price)
    #     self.assertEqual(found.count(), count)
    #     for product in found:
    #         self.assertEqual(product.price, price)
    # todo add/fix a 'def find_by_price' function to models.py before uncommmenting this # pylint: disable=fixme
