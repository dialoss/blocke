import json
import time
from mitmproxy import http
from base import Base
from tools import format_response, async_to_sync

class Spb(Base):
    def get_accounts(self):
        balance = self.api.get_card_balance(1)
        return {"accountsAvailability": {"dataIsOutdated": False, "lastUpdateTime": "2024-10-14T10:29:47.063"},
                "productSections": [{"title": "Счета и карты", "type": "ACCOUNTS_WITH_CARDS", "products": [{
                    "account": {
                        "id": 2084280965210,
                        "number": "40817810190270190626",
                        "available": balance,
                        "ownFunds": balance,
                        "balance": balance,
                        "reserved": 0,
                        "currency": "RUB",
                        "bic": "044030790",
                        "type": "CURRENT",
                        "enabledForLoan": True,
                        "allowedOperations": {
                            "common": [
                                "STATEMENT",
                                "CARD",
                                "DEPOSIT",
                                "LOAN"],
                            "debit": [
                                "PERSONAL",
                                "DOMESTIC",
                                "EXCHANGE",
                                "FROM_CARD_TO_CARD",
                                "VENDOR"],
                            "credit": [
                                "PERSONAL",
                                "DOMESTIC",
                                "EXCHANGE",
                                "FROM_CARD_TO_CARD"]},
                        "allowedCardTypeRefs": [],
                        "requisites": [
                            {
                                "Получатель": "Фоменко Алексей Андреевич"},
                            {
                                "Счёт получателя": "40817810190270190626"},
                            {
                                "ИНН": "7831000027"},
                            {
                                "КПП": "780601001"},
                            {
                                "Банк получателя": "ПАО \"БАНК \"САНКТ-ПЕТЕРБУРГ\""},
                            {
                                "БИК": "044030790"},
                            {
                                "Кор. счёт": "30101810900000000790"},
                            {
                                "Назначение платежа": "Перевод денежных средств на счёт 40817810190270190626 Фоменко Алексей Андреевич"}]},
                    "cards": [
                        {
                            "id": 2084280966087,
                            "number": "2200330661931807097",
                            "ref": "10f6dd5ffa749a0b575cc44b0bae80afb9e9bdeb27c315faac7d1856f5f98387515717b1289c1699312f7eaee351d01ade959cd4fb050520d4c0711e6981ec45",
                            "status": "ACTIVE",
                            "expiration": "2028-08-31T00:00:00.000",
                            "cardName": "Классическая",
                            "holderName": "ALEKSEI FOMENKO",
                            "accountNumber": "40817810190270190626",
                            "linkedToCurrentCustomersAccount": True,
                            "cardRef": "821",
                            "visual": "classic",
                            "imageUrl": "https://i.bspb.ru/private-mobile-app-middleware/images/cards/classic.png",
                            "paymentSystem": "mir",
                            "shortCardName": "Классическая",
                            "primary": True,
                            "tariffUrl": "https://www.bspb.ru/retail/banking-services/docs/cards/tariff-personal.pdf",
                            "allowedActions": [
                                "BLOCK",
                                "LIMIT_CHANGE",
                                "SECURE_3D",
                                "NOTIFICATION_CHANGE",
                                "PIN_UPDATE"],
                            "notifications": {
                                "SMS": {
                                    "main": "79124531782",
                                    "additional": [],
                                    "fee": 99},
                                "EMAIL": {
                                    "additional": [],
                                    "fee": 30}},
                            "requisites": [],
                            "branchCode": "001-999",
                            "vanilla": True,
                            "unlimitedFreeAtmWithdrawal": True,
                            "yaSchitayuLevelCode": 1,
                            "allowedFreeAtmWithdrawal": 1000000,
                            "loyaltyProgramType": "MAIN",
                            "bonusBalance": 8.00}],
                    "productType": "ACCOUNT",
                    "productRef": "ACCOUNT:2084280965210"}]},
                                    {"title": "К счетам других клиентов", "type": "FOREIGN_CARDS",
                                     "products": []}, {"title": "Вклады", "type": "DEPOSITS", "products": []},
                                    {"title": "Кредиты", "type": "LOANS", "products": []},
                                    {"title": "Карты сторонних банков", "type": "OTHER_BANK_CARDS",
                                     "products": []}], "hiddenProductSection": {"title": "Скрытые продукты",
                                                                                "productSections": [
                                                                                    {"title": "Счета и карты",
                                                                                     "type": "ACCOUNTS_WITH_CARDS",
                                                                                     "products": []}, {
                                                                                        "title": "К счетам других клиентов",
                                                                                        "type": "FOREIGN_CARDS",
                                                                                        "products": []},
                                                                                    {"title": "Вклады",
                                                                                     "type": "DEPOSITS",
                                                                                     "products": []},
                                                                                    {"title": "Кредиты",
                                                                                     "type": "LOANS",
                                                                                     "products": []}, {
                                                                                        "title": "Карты сторонних банков",
                                                                                        "type": "OTHER_BANK_CARDS",
                                                                                        "products": []}]}}

    def request(self, flow: http.HTTPFlow):
        url = flow.request.pretty_url
        if url.startswith(
                'https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/draft'):
            flow.response = http.Response.make(200, json.dumps({
                "draftId": "288060776"
            }), {'content-type': 'application/json;charset=utf-8'})
        if url.startswith(
                'https://i.bspb.ru/private-mobile-app-middleware/v2/payments/faster-payments-system/payment'):
            time.sleep(2)
            self.phone = json.loads(flow.request.data.content)['beneficiaryPhoneNumber']
            flow.response = http.Response.make(200, json.dumps(
                {"paymentId": 119653590, "beneficiaryName": self.name,
                 "confirmation": {"confirmationKey": "4034223b-9a8a-423f-a9aa-01e821751154"}}),
                                               {'content-type': 'application/json;charset=utf-8'})
        if url.startswith(
                'https://i.bspb.ru/private-mobile-app-middleware/v2/payments/faster-payments-system/confirm-payment'):
            time.sleep(2)
            card = self.api.get_card(1)
            flow.response = format_response(
                {"paymentId": 119653590, "ref": "FAST_PAYMENT_SERVICE:119653590",
                 "beneficiaryName": self.name,
                 "description": "Перевод", "amount": {"amount": -1 * self.amount, "currency": "RUB"},
                 "fee": {"amount": 0.00, "currency": "RUB"}, "remitterAccountName": "Счёт • " + card['number'][-4:],
                 "beneficiaryPhoneNumber": self.phone, "status": "PENDING",
                 "receiptPdfUrl": "https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/payment/119653590/outgoing-pdf",
                 "canBeFavorite": True, "canBeRepeated": True})
            self.api.insert_operation({"type": "outcome", "title": "Перевод " + self.name, "amount": self.amount})
        if url.startswith(
                'https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/fee'):
            flow.response = http.Response.make(200, '0')
            self.amount = float(flow.request.query.get('paymentAmount'))
        if url.startswith('https://i.bspb.ru/private-mobile-app-middleware/v2/home'):
            flow.response = format_response(self.get_accounts())
        if url.startswith('https://i.bspb.ru/private-mobile-app-middleware/v2/statement'):
            if not flow.request.query.get('txRef'):
                flow.response = format_response({"summary": {"incomes": 1212121, "outcomes": -4002.00}, "statement": [
                    {"date": "2024-10-14T00:00:00.000", "transactions": [
                        {"id": 2363011048013, "ref": "STATEMENT_SERVICE:2363011048013",
                         "time": "2024-10-14T13:38:43.000",
                         "type": "FAST_PAYMENT", "status": "DONE", "amount": 22992990, "currency": "RUB",
                         "counterpartyName": "Алексей Андреевич Ф.", "ownerName": "Счёт • 0626",
                         "accountId": 2084280965210,
                         "description": "Входящий перевод по СБП, Алексей Андреевич Ф, 0079935324905, Т-Банк, , Код операции B4288103841375200000120011350901. НДС не облагается..",
                         "docNumber": "94499", "terminal": "ПАО \"БАНК \"САНКТ-ПЕТЕРБУРГ\"",
                         "iconUrl": "https://i.bspb.ru/public/images/sbp/bank-icons/mobile/100000000004.png",
                         "category": "Пополнения", "phoneNumber": "79935324905",
                         "receiptPdfUrl": "https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/transaction/2363011048013/incoming-pdf",
                         "operationCode": "B4288103841375200000120011350901", "comment": "",
                         "counterpartyAccount": "30233810990001041000", "counterpartyBankName": "Т-Банк",
                         "allowedActions": [], "actionsAllowed": [], "estimatedRefundDate": "2024-10-16"},
                        {"id": 119655869, "ref": "FAST_PAYMENT_SERVICE:119655869", "time": "2024-10-14T10:56:11.000",
                         "type": "FAST_PAYMENT", "status": "DONE", "amount": -323231.00, "currency": "RUB",
                         "counterpartyName": "Алексей Андреевич Ф.", "ownerName": "Счёт • 0626",
                         "accountId": 2084280965210,
                         "description": "",
                         "iconUrl": "https://i.bspb.ru/public/images/sbp/bank-icons/mobile/100000000004.png",
                         "category": "Переводы", "phoneNumber": "79935324905", "paymentId": 119655869, "fee": 0.00,
                         "feeCurrency": "RUB",
                         "receiptPdfUrl": "https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/payment/119655869/outgoing-pdf",
                         "operationCode": "A4288075551328260000020011350901", "counterpartyBankName": "Т-Банк",
                         "allowedActions": ["makeFavorite", "repeat"], "actionsAllowed": [],
                         "estimatedRefundDate": "2024-10-16"},
                        {"id": 119653590, "ref": "FAST_PAYMENT_SERVICE:119653590", "time": "2024-10-14T10:42:43.000",
                         "type": "FAST_PAYMENT", "status": "DONE", "amount": -1.00, "currency": "RUB",
                         "counterpartyName": "Алексей Андреевич Ф.", "ownerName": "Счёт • 0626",
                         "accountId": 2084280965210,
                         "description": "",
                         "iconUrl": "https://i.bspb.ru/public/images/sbp/bank-icons/mobile/100000000004.png",
                         "category": "Переводы", "phoneNumber": "79935324905", "paymentId": 119653590, "fee": 0.00,
                         "feeCurrency": "RUB",
                         "receiptPdfUrl": "https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/payment/119653590/outgoing-pdf",
                         "operationCode": "A42880742178564E0000030011350901", "counterpartyBankName": "Т-Банк",
                         "allowedActions": ["makeFavorite", "repeat"], "actionsAllowed": [],
                         "estimatedRefundDate": "2024-10-16"},
                        {"id": 2362910326198, "ref": "STATEMENT_SERVICE:2362910326198",
                         "time": "2024-10-14T10:40:37.000",
                         "type": "FAST_PAYMENT", "status": "DONE", "amount": 10, "currency": "RUB",
                         "counterpartyName": "Алексей Андреевич Ф.", "ownerName": "Счёт • 0626",
                         "accountId": 2084280965210,
                         "description": "Входящий перевод по СБП, Алексей Андреевич Ф, 0079935324905, Т-Банк, , Код операции A42880740345942B0000040011350901. НДС не облагается..",
                         "docNumber": "894798", "terminal": "ПАО \"БАНК \"САНКТ-ПЕТЕРБУРГ\"",
                         "iconUrl": "https://i.bspb.ru/public/images/sbp/bank-icons/mobile/100000000004.png",
                         "category": "Пополнения", "phoneNumber": "79935324905",
                         "receiptPdfUrl": "https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/transaction/2362910326198/incoming-pdf",
                         "operationCode": "A42880740345942B0000040011350901", "comment": "",
                         "counterpartyAccount": "30233810990001041000", "counterpartyBankName": "Т-Банк",
                         "allowedActions": [], "actionsAllowed": [], "estimatedRefundDate": "2024-10-16"}]}]})
            else:
                flow.response = format_response({
                    "statement": [],
                    "summary": {
                        "incomes": 4020,
                        "outcomes": -4002.0
                    }
                })
        if url.startswith('https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/payment/'):
            flow.response = http.Response.make(200, self.api.get_check(), {'content-type': 'application/pdf'})

        if url.startswith(
                'https://i.bspb.ru/private-mobile-app-middleware/payments/faster-payments-system/transaction/'):
            flow.response = http.Response.make(200, self.api.get_check(), {'content-type': 'application/pdf'})

# addons = [Spb('spb')]