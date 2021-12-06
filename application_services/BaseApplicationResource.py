from abc import ABC, abstractmethod
from database_services.RDBService import RDBService


class BaseApplicationException(Exception):

    def __init__(self):
        pass


class BaseApplicationResource(ABC):

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_by_template(cls, template):
        pass

    @classmethod
    @abstractmethod
    def get_links(self, resource_data):
        pass

    @classmethod
    @abstractmethod
    def get_data_resource_info(self):
        pass


class BaseRDBApplicationResource(BaseApplicationResource):

    def __init__(self):
        pass

    @classmethod
    def get_by_template(cls, template):
        db_name, table_name = cls.get_data_resource_info()
        res = RDBService.find_by_template(db_name, table_name,
                                          template, None)
        return res

    @classmethod
    @abstractmethod
    def get_links(self, resource_data):
        pass

    @classmethod
    @abstractmethod
    def get_data_resource_info(self):
        pass

    ## leftover from template
    @classmethod
    def get_by_name_prefix(cls, name_prefix):
        res = RDBService.get_by_prefix("IMDBFixed", "names_basic_recent",
                                       "primaryName", name_prefix)
        return res