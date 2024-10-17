import urllib.request
import json


class API:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def _perform_request(self, url, method='GET', post_data=None):
        if method == 'POST':
            data = json.dumps(post_data).encode('utf-8')
            req = urllib.request.Request(url, data=data, method='POST')
            req.add_header('Content-Type', 'application/json')
        else:
            req = urllib.request.Request(url)

        with urllib.request.urlopen(req) as response:
            body = response.read()
        return json.loads(body.decode('utf-8'))

    def get_card_balance(self, card_id):
        url = f"{self.url}/{self.name}/get_card_balance/{card_id}"
        data = self._perform_request(url)
        return data["balance"]

    def get_card(self, id):
        url = f"{self.url}/{self.name}/get_card/{id}"
        data = self._perform_request(url)
        return data

    def get_history(self):
        url = f"{self.url}/{self.name}/get_history"
        data = self._perform_request(url)
        return data["history"]

    def insert_operation(self, operation):
        url = f"{self.url}/{self.name}/insert_operation"
        data = self._perform_request(url, method='POST', post_data=operation)
        return data["success"]

    def get_settings(self):
        url = f"{self.url}/{self.name}/get_settings"
        return self._perform_request(url)

    def get_check(self, data={}):
        data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(f"{self.url}/{self.name}/get_check", data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req) as response:
            return response.read()


class Base():
    def __init__(self, db_name):
        self.name = ""
        self.amount = 0
        self.phone = ""
        self.card = ""
        self.api = API(db_name, "http://localhost:5000")
