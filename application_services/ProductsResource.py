from __future__ import print_function
from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService


class ProductResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return 'aaaaaF21E6156', 'products'

    @classmethod
    def get_all_product_data(cls):
        res = RDBService.get_full_table("ProductsInfo", "ProductsInfo")
        return res

    @classmethod
    def get_select_product_data(cls, template):
        res = RDBService.find_by_template("ProductsInfo", "ProductsInfo", template)
        return res

    @classmethod
    def create_product(cls, data):
        res = RDBService.create("ProductsInfo", "ProductsInfo", data)
        return res

    @classmethod
    def delete_product(cls, product_no):
        res = RDBService.delete("ProductsInfo", "ProductsInfo", product_no)
        return res
