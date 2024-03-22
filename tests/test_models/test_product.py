#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.product import Product


class test_Product(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Product"
        self.value = Product

    def test_product_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.product_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.description), str)

    def test_number_pieces(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_pieces), int)

    def test_price(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.price), int)
