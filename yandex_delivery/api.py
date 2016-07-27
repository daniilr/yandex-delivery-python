import requests
from .exceptions import *
from hashlib import md5

# Original API description: http://docs.yandexdelivery.apiary.io/


class DeliveryClient(object):
    API_VERSION = "1.0"
    API_URL = "https://delivery.yandex.ru/api"
    USER_AGENT = "YandexDeliveryClient/Python (https://github.com/daniilr/yandex-delivery-python)"

    def __init__(self, client_id, sender_id, warehouse_ids=[], requisite_id=[], method_keys={}):
        """
        Чтобы получить настройки, перейдите в интерфейсе сервиса на страницу
        настроек Интеграция --> API. Далее в блоке Настройки нажмите кнопку получить.

        Args:
            client_id (int): идентификатор аккаунта в сервисе
            sender_id (int): идентификаторы и URL магазинов из аккаунта в сервисе
            warehouse_ids (list): идентификаторы складов из аккаунта в сервисе
            requisite_id (list): идентификаторы реквизитов магазинов из аккаунта в сервисе
            method_keys (dict): ключ — название метода, значение — method_key
        """
        self.client_id = client_id
        self.sender_id = sender_id
        self.warehouse_ids = warehouse_ids
        self.requisite_id = requisite_id
        self.method_keys = method_keys

    def request(self, method, **kwargs):
        """

        Args:
            method (str): название метода
            **kwargs: POST-данные передаются в виде keyword-аргументов методу
        Returns:
            dict: ответ API
        Raises:
            ApiException
        """
        if method not in self.method_keys:
            raise AccessException("Method %s has method_key defined for it" % method)
        secret_key = self.method_keys[method]
        data = kwargs
        data['client_id'] = self.client_id
        data['sender_id'] = self.sender_id
        secret_string = "".join([str(data[key]) for key in sorted(data)]) + secret_key
        data['secret_key'] = md5(secret_string.encode('utf-8')).hexdigest()

        response = requests.post("/".join([self.API_URL, self.API_VERSION, method]),
                                 data, headers={'User-Agent': self.USER_AGENT}).json()
        if response["status"] == "error":
            raise ClientException("client responded with error %s. \nFull output: %s" % (response["error"], response))
        return response

    def get_sender_info(self):
        """
        http://docs.yandexdelivery.apiary.io/#reference/0/getsenderinfo/
        Returns:
            dict: информация о магазине из аккаунта в сервисе
        """
        return self.request("getSenderInfo")

    def get_warehouse_info(self, warehouse_id):
        """
        http://docs.yandexdelivery.apiary.io/#reference/0/getwarehouseinfo/.
        Args:
            warehouse_id (int): идентификатор склада
        Returns:
            dict: инормация о складе из аккаунта
        """
        return self.request("getSenderInfo", warehouse_id=warehouse_id)