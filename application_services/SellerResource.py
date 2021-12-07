from __future__ import print_function
from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService


class SellerResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return 'aaaaaF21E6156', 'sellers'

    @classmethod
    def get_all_seller_data(cls):
        res = RDBService.get_full_table("CharityStoreDB", "SellersInfo")
        return res

    @classmethod
    def get_select_seller_data(cls, data):
        res = RDBService.find_by_template("CharityStoreDB", "SellersInfo", data)
        return res

    @classmethod
    def create_seller(cls, data):
        res = RDBService.create("CharityStoreDB", "SellersInfo", data)
        return res

    @classmethod
    def delete_seller(cls, data):
        res1 = RDBService.find_by_template("CharityStoreDB", "SellersInfo", data)
        res = RDBService.delete("CharityStoreDB", "SellersInfo", data)
        return res1

    @classmethod
    def find_related_product(cls, args_list):
        res = RDBService.get_by_foreign_id('CharityStoreDB', 'SellersInfo', 'ProductsInfo', args_list)
        return res