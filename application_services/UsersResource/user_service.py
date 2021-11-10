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
        res = RDBService.get_full_table("UsersInfo", "UsersInfo")
        return res

    # @classmethod
    # def get_one_user_data(cls):
    #     res = RDBService.get_select_table("UsersInfo", "UsersInfo")
    #     return res

    @classmethod
    def create_user(cls, user_no, first_name, last_name, email):
        data_to_create = {"user_no": user_no,
                          "first_name": first_name,
                          "last_name": last_name,
                          "email": email}
        res = RDBService.create("UsersInfo", "UsersInfo", data_to_create)
        return res

    @classmethod
    def delete_user(cls, data):
        data_to_delete = data['user_no']
        res = RDBService.delete("UsersInfo", "UsersInfo", data_to_delete)
        return res

    # @classmethod
    # def update_user(cls, data):
    #     data_to_update = data
    #     res = RDBService.delete("UsersInfo", "UsersInfo", data_to_update)
    #     return res
