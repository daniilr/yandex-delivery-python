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
        secret_string = "".join([str(data[key]) for key in sorted(data) if data[key]]) + secret_key
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

    def get_requisite_info(self, requisite_id):
        """
        http://docs.yandexdelivery.apiary.io/#reference/0/getrequisiteinfo/.
        Args:
            requisite_id (int): Идентификатор реквизитов магазина из аккаунта в сервисе

        Returns:
            dict: Получение информации о реквизитах магазина из аккаунта в сервисе.
        """
        return self.request("getRequisiteInfo", requisite_id=requisite_id)

    def autocomplete(self, term, complete_type="address", locality_name=None, geo_id=None, street=None):
        """
        Args:
            term (str): Часть адреса для последующего автодополнения
            complete_type (str): Тип автодополнения
            locality_name (str): Название города. Обязательный параметр, если type=street или type=house
            geo_id (int): Идентификатор локации. Аналог locality_name. Обязательный параметр, если type=street
                или type=house и не указан locality_name.
            street (str): Название улицы. Обязательный параметр, если type=house.
        Returns:
            dict: Автоматическое дополнение названий города, улицы и дома.
        Raises:

        """
        if (complete_type == "street" or complete_type == "house") and not (geo_id or locality_name):
            raise AttributeError("Type '%s' requires geo_id or locality_name keyword arguments" % complete_type)
        if complete_type == "house" and not street:
            raise AttributeError("Type '%s' requires street keyword argument" % complete_type)

        return self.request("autocomplete", term=term, type=complete_type, locality_name=locality_name,
                            geo_id=geo_id, street=street)

    def get_index(self, address):
        """
        http://docs.yandexdelivery.apiary.io/#reference/0/getindex/.
        Args:
            address (str): Введенный адрес

        Returns:
            dict: индекс
        """
        return self.request("getIndex", address=address)

    def search_delivery_list(self, city_from, city_to, weight, width, height, length,
                             geo_id_to=None, geo_id_from=None, delivery_type=None, total_cost=None,
                             index_city=None, to_yd_warehouse=None, order_cost=None, assessed_value=None):
        """

        Args:
            city_from (str): Обязательное поле. Город, из которого осуществляется доставка
            city_to (str): Обязательное поле. Город, в который осуществляется доставка
            weight (float): Обязательное поле. Вес посылки, в кг.
            width (int): Обязательное поле. Высота посылки, в см.
            height (int): Обязательное поле. Ширина посылки, в см.
            length (int): Обязательное поле. Длина посылки, в см.
            geo_id_to (str): Идентификатор города, в который осуществляется доставка. В случае,
                когда указаны оба параметра (city_to и geo_id_to) больший приоритет имеет geo_id_to
            geo_id_from (str): Идентификатор города, из которого осуществляется доставка. В случае, когда указаны
                оба параметра (city_from и geo_id_from) больший приоритет имеет geo_id_from
            delivery_type (str): Тип доставки: курьером до двери либо в пункт выдачи заказов. Если тип не указан,
                будут загружены все варианты.
            total_cost (float): Общая стоимость отправления, в руб. При передаче будут автоматически рассчитано кассовое
                обслуживание.
            order_cost (float): Стоимость товарных позиций, в руб. При передаче будут применены правила редактора тарифов,
                зависящие от стоимости заказа.
            assessed_value (float): Объявленная ценность отправления, в руб. При передаче будут автоматически рассчитана
                страховка, а также применены правила редактора тарифов.
            index_city (int): Индекс получателя. Будут отфильтрованы службы, которые не осуществляют доставку по данному
                индексу.
            to_yd_warehouse (int): Тип отгрузки: напрямую в службу доставки или через единый склад

        Returns:

        """
        return self.request("searchDeliveryList", city_from=city_from, city_to=city_to, weight=weight, width=width, height=height,
                            length=length,
                            geo_id_to=geo_id_to, geo_id_from=geo_id_from, delivery_type=delivery_type,
                            total_cost=total_cost,
                            index_city=index_city, to_yd_warehouse=to_yd_warehouse, order_cost=order_cost,
                            assessed_value=assessed_value)
