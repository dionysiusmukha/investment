class Client:
    def __init__(self, client_id, name, type_of_property, address, phone):
        self.__client_id = client_id
        self.__name = name
        self.__type_of_property = type_of_property
        self.__address = address
        self.__phone = phone

    def get_client_id(self):
        return self.__client_id

    def set_client_id(self, client_id):
        self.__client_id = client_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_type_of_property(self):
        return self.__type_of_property

    def set_type_of_property(self, type_of_property):
        self.__type_of_property = type_of_property

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone):
        self.__phone = phone
