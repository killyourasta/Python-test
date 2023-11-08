import requests

WEATHER_API_KEY = '99ba78ee79a2a24bc507362c5288a81b'


class WeatherAPI:
    def __init__(self):
        """
        Инициализирует класс.
        """
        self.session = requests.Session()

    def create_weather_request_url(self, city):
        """
        Генерирует url, включая в него необходимые параметры.
        """
        # Можно url написать в одну строку во избежание ошибок.
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": WEATHER_API_KEY
        }
        return base_url, params

    def send_request(self, url, params=None):
        """
        Отправляет запрос на сервер.
        """
        response = requests.get(url, params=params)
        return response

    def get_weather_data(self, city):
        """
        Отправляет запрос на сервер,
        чтобы получить данные о погоде для указанного города.
        """
        url, params = self.create_weather_request_url(city)
        response = self.send_request(url, params=params)
        return response

    def get_city_weather(self, city):
        """
        Достает погоду из ответа.
        """
        response = self.get_weather_data(city)
        if response is not None and response.status_code == 200:
            # Получите данные о погоде
            data = response.json()
            temperature = data.get("main", {}).get("temp")
            if temperature is not None:
                # Значение переменной temperature переводится из Кельвинов в Цельсии путем вычитания 273.15.
                temperature_celsius = temperature - 273.15
                return temperature_celsius
        return None

    def check_city_exists(self, city):
        """
        Проверка наличия города (запросом к серверу погоды).
        """
        response = self.get_weather_data(city)
        return response is not None and response.status_code == 200
