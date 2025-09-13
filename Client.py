


class Client:
    def __init__(self, client_id, name, type_of_property, address, phone):
        self.__client_id = Client.valid_client_id(client_id)
        self.__name = Client.valid_client_name(name)
        self.__type_of_property = Client.valid_type_of_property(type_of_property)
        self.__address = Client.valid_address(address)
        self.__phone = Client.valid_phone(phone)

    def get_client_id(self):
        return self.__client_id

    def set_client_id(self, client_id):
        self.__client_id = Client.valid_client_id(client_id)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = Client.valid_client_name(name)

    def get_type_of_property(self):
        return self.__type_of_property

    def set_type_of_property(self, type_of_property):
        self.__type_of_property = Client.valid_type_of_property(type_of_property)

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = Client.valid_address(address)

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone):
        self.__phone = Client.valid_phone(phone)

    @staticmethod
    def valid_client_id(client_id):
        if not isinstance(client_id, int):
            raise ValueError("ID клиента должно быть целым числом")
        if client_id < 0:
            raise ValueError("ID клиента должен быть >= 0")
        return client_id

    @staticmethod
    def valid_client_name(name):
        name = name.strip()
        if name == '':
            raise ValueError("Строка имени должна быть непустой")
        return name

    @staticmethod
    def valid_type_of_property(type_of_property):
        acceptable_values = ["ООО", "ЗАО", "ОАО", "ИП"]
        if type_of_property == '':
            raise ValueError("Строка формы организации должна быть не пустой")
        f = False
        for i in acceptable_values:
            if i in type_of_property:
                f = True
        if not f:
            raise ValueError('Строка формы организации должна содержать: "ООО", "ЗАО", "ОАО", "ИП"')
        return type_of_property

    @staticmethod
    def valid_address(address):
        if address == '':
            raise ValueError("Строка адресса должна быть не пустой")
        return address

    @staticmethod
    def valid_phone(phone):
        if phone == '':
            raise ValueError("Строка номера телефона должна быть не пустой")
        if len(phone) < 10:
            raise ValueError("Телефон должен содержать от 10 цифр")
        if phone[0] == '+':
            phone = phone[1:]
        if '-' in phone:
            phone = phone.replace('-', '')
        if '(' in phone:
            phone = phone.replace('(', '')
        if ')' in phone:
            phone = phone.replace(')', '')
        for s in phone:
            if not s.isdigit():
                raise ValueError("Телефон должент содержать только цифры и символы: '-','(',')','+'")
        if phone[0] == '8' and len(phone) == 11:
            phone = '7' + phone[1:]
        if len(phone) == 10:
            phone = '7' + phone

        return phone





try:
    c = Client(1,'    dede   ',"ООО zao","kalinina","9899993678")
    print(c.get_phone())
except ValueError as e:
    print("Ошибка:", e)