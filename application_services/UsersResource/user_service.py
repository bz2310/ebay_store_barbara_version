from __future__ import print_function
from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService

class UserResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return 'aaaaaF21E6156', 'users'

    @classmethod
    def get_all_user_data(cls):
        res = RDBService.get_full_table("CharityStoreDB", "UsersInfo")
        return res

    @classmethod
    def get_select_user_data(cls, template):
        res = RDBService.find_by_template("CharityStoreDB", "UsersInfo", template)
        return res

    @classmethod
    def create_user(cls, data):
        res = RDBService.create("CharityStoreDB", "UsersInfo", data)
        return res

    @classmethod
    def delete_user(cls, data):
        res1 = RDBService.find_by_template("CharityStoreDB", "UsersInfo", data)
        res = RDBService.delete("CharityStoreDB", "UsersInfo", data)
        return res1
