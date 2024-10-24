import json
import random
from datetime import datetime

from mitmproxy import http
from tools import format_response
from base import Base


def format_cards(cards):
    return [{"id": 3900034455303300 + i, "name": "", "order": 1, "hidden": True,
             "description": "", "cardHolder": "SBERKARTA MOMENTUM",
             "number": ('9999999999999999' + card['number'])[-16:], "selfEmployed": False, "isMain": True,
             "type": "debit",
             "availableLimit": {"amount": str(card['balance']), "currency": {"code": "RUB", "name": "руб."}},
             "availableTotalLimit": {"amount": str(card['balance']), "currency": {"code": "RUB", "name": "руб."}},
             "state": "active", "cardAccount": ('9999999999999999' + card['chet'])[-20:], "arrested": False,
             "showArrestDetail": True,
             "isc": False, "isAllowedPriorityP2P": True, "tokenExists": False, "tokenList": [],
             "expireDate": "05/2034", "statusWay4": "+-active", "rarelyUsed": False, "imageCode": "wp",
             "sbercardLevel": 2, "needRqDeliveryStatus": False, "needRqDeliveryStatusReissue": False,
             "needRqChangeOfficeWidget": False, "realExpireDate": "05/2034", "issueDate": "15.10.2024",
             "multiCurrencyAccounts": [], "issueType": 0, "isCTA": True, "cardCode": "111857",
             "iconCode": "wp",
             "iconCodeAddSign": "2",
             "optionPermissions": {"allowedMetalPhysicalCreditCardReissue": False,
                                   "changeCreditLimit": False,
                                   "setPINAvailable": True, "setPayrollAvailable": False,
                                   "activationAvailableUfs": False, "block": True,
                                   "isAnimatedCardDesignAvailable": False, "isMainCardCompWallet": False,
                                   "additionalCardAvailable": False, "isAllowedPriorityP2P": True,
                                   "cardClientLimitsMainScreen": True, "pay": True, "createMoneyBox": True,
                                   "needLimitForPensionProduct": False, "closeCreditCard": False,
                                   "allowedChangeTariffPPRBCreditCard": False,
                                   "allowedMetalPhysicalCreditCardOrder": False,
                                   "activateCreditCard": False,
                                   "isSocialPackageAvailable": True, "closeCardAvailable": False,
                                   "changeGracePeriod": False, "replenish": True,
                                   "changeCardTariffAvailable": False, "changePaymentDate": False,
                                   "isSbercardTariffV3": True, "activationAvailable": False,
                                   "increaseLimitCreditCard": False, "setCardDesign": True,
                                   "setPriorityCard": True,
                                   "isMultiCurrency": False, "needRqChangeOfficeWidget": False,
                                   "ownBusiness": False, "sberPayTokenizable": True, "getCashInAtm": True,
                                   "getCvcCode": False, "activateCreditCardMigration": False,
                                   "autopay": False,
                                   "samsungPayTokenizable": True, "googlePayTokenizable": True,
                                   "needRqDeliveryStatus": False, "getInsurance": False,
                                   "multiCurrencyCardAvailable": False, "needRqLifeCycleStatusV2": False,
                                   "physicalCardOrderAvailable": False, "reissueCreditCard": False,
                                   "isCreditCardAccountToClose": False, "displayCardDesign": False,
                                   "transfer2Organization": True, "transfer2Person": True,
                                   "applePayTokenizable": True, "cashWithdrawalTransferFree": False,
                                   "changeCardProduct": False, "decreaseRateForCategoryOperations": False,
                                   "transfer2Self": True},
             "creditOwnSum": {"amount": str(card['balance']), "currency": {"code": "RUB", "name": "руб."}},
             "isReissuedCard": False, "location": ["header"]} for i, card in enumerate(cards)]


def format_cards_small(cards):
    return [{"id": 3900008975103250 + i, "name": "Платёжный счёт", "order": 1, "hidden": False,
             "description": "Платёжный счёт", "number": ('9999999999999999' + card['chet'])[-20:],
             "balance": {"amount": card['balance'], "currency": {"code": "RUB", "name": "руб."}}, "state": "active",
             "arrested": False, "location": ["wallet", "header"], "grantor": "Алексей Андреевич Ф",
             "documents": []} for i, card in enumerate(cards)]


class Sber(Base):
    def get_accounts(self):
        return {"success": True, "body": {
            "personalization": {"segments": {"name": "0"}, "isNewClient": False, "isSberPrimeOnMainScreen": False},
            "generalPermissions": {"CreditCardAvailable": True, "VirtualCardMP": False, "DebitCardAppMP": True},
            "sectionDisplaySettings": [{"sections": [
                {"order": 1, "title": "Кошелёк", "hidden": False, "enabled": False, "expanded": True, "locked": True,
                 "expandable": False, "keepState": False, "sections": [
                    {"order": 1, "title": "Платёжные счета", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "ctaccounts", "default": False},
                    {"order": 2, "title": "Карты в кошельке", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "cardsInWallet",
                     "default": False},
                    {"order": 3, "title": "Детские СберКарты", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "kidsSberCards",
                     "default": False},
                    {"order": 4, "title": "Детские карты", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "kidsCards", "default": False},
                    {"order": 5, "title": "СберСпасибо", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "sberThanks", "default": False},
                    {"order": 6, "title": "Продукты опенбанкинга", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "obpctaccounts",
                     "default": False}], "code": "newWallet", "default": True},
                {"order": 2, "title": "Переводы на Сбер", "hidden": False, "enabled": False, "expanded": True,
                 "locked": False, "expandable": False, "keepState": False, "hidingSectionDisable": False,
                 "sections": [{"order": 1, "title": "Переводы на Сбер", "code": "payments"}], "code": "payments",
                 "default": True},
                {"order": 3, "title": "Расходы", "hidden": False, "enabled": False, "expanded": True, "locked": False,
                 "expandable": False, "keepState": False,
                 "sections": [{"order": 1, "title": "Расходы", "code": "expenses"}], "code": "expenses",
                 "default": True},
                {"order": 4, "title": "Вклады и счета", "hidden": False, "enabled": False, "expanded": False,
                 "locked": False, "expandable": True, "keepState": False, "sections": [
                    {"order": 1, "title": "Счета", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "accounts", "default": False},
                    {"order": 2, "title": "Металлы", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "ima", "default": False}],
                 "disabled": True, "code": "accountsAndIma", "default": False},
                {"order": 5, "title": "Кредиты", "hidden": False, "enabled": False, "expanded": False, "locked": False,
                 "expandable": True, "keepState": False,
                 "sections": [{"order": 1, "title": "Кредиты", "code": "loans"}], "code": "loans", "default": False},
                {"order": 6, "title": "Цели", "hidden": False, "enabled": False, "expanded": False, "locked": False,
                 "expandable": True, "keepState": False, "sections": [
                    {"order": 1, "title": "Цели", "hidden": False, "enabled": False, "expanded": False, "locked": False,
                     "expandable": False, "keepState": False, "code": "goals", "default": False}], "disabled": True,
                 "code": "goalsAndEnvelopes", "default": False},
                {"order": 7, "title": "Инвестиции", "hidden": False, "enabled": False, "expanded": False,
                 "locked": False, "expandable": True, "keepState": False, "sections": [
                    {"order": 1, "title": "Инвестиции", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "investments",
                     "default": False}], "disabled": True, "code": "investmentsAndPensions", "default": False},
                {"order": 8, "title": "Пенсии", "hidden": False, "enabled": False, "expanded": False, "locked": False,
                 "expandable": True, "keepState": False,
                 "sections": [{"order": 1, "title": "Пенсии", "code": "pensions"}], "disabled": True,
                 "code": "pensions", "default": False},
                {"order": 9, "title": "Валюты и металлы", "hidden": False, "enabled": False, "expanded": False,
                 "locked": False, "expandable": True, "keepState": False,
                 "sections": [{"order": 1, "title": "Валюты и металлы", "code": "rates"}], "code": "rates",
                 "default": False},
                {"order": 10, "title": "Сервисы", "hidden": False, "enabled": False, "expanded": False, "locked": True,
                 "expandable": False, "keepState": False,
                 "sections": [{"order": 1, "title": "Сервисы", "code": "services"}], "code": "services",
                 "default": False},
                {"order": 11, "title": "Рекомендуем", "hidden": False, "enabled": False, "expanded": False,
                 "locked": True, "expandable": False, "keepState": False,
                 "sections": [{"order": 1, "title": "Рекомендуем", "code": "recommended"}], "code": "recommended",
                 "default": False},
                {"order": 12, "title": "Курсы валют", "hidden": False, "enabled": False, "expanded": True,
                 "locked": True, "expandable": False, "keepState": False, "sections": [
                    {"order": 1, "title": "Клиентские курсы валют", "hidden": False, "enabled": False,
                     "expanded": False, "locked": False, "expandable": False, "keepState": False,
                     "code": "currencyRates", "default": False},
                    {"order": 2, "title": "Курсы валют ЦБ", "hidden": False, "enabled": False, "expanded": False,
                     "locked": False, "expandable": False, "keepState": False, "code": "currencyCbRates",
                     "default": False}], "disabled": True, "code": "currencies", "default": True},
                {"order": 13, "title": "Сбер и партнёры", "hidden": False, "enabled": False, "expanded": True,
                 "locked": True, "expandable": False, "keepState": False,
                 "sections": [{"order": 1, "title": "Сбер и партнёры", "code": "geomap"}], "code": "geomap",
                 "default": False}], "code": "body"}], "sections": {"technicalSection": {"sectionProductData": {
                "cardsInWallet": {"data": format_cards(self.api.get_cards()),
                                  "url": "/main-screen/rest/v2/mobile/section/data/cardsInWallet", "state": "SUCCESS"},
                "currencyCbRates": {"data": [{"baseCurrency": "USD", "lotSize": 1, "value": 96.4172},
                                             {"baseCurrency": "EUR", "lotSize": 1, "value": 104.8565}],
                                    "url": "/main-screen/rest/v2/mobile/section/data/currencyCbRates",
                                    "state": "SUCCESS"},
                "loans": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/loans",
                          "state": "NOT_REQUESTED"},
                "rates": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/rates",
                          "state": "NOT_REQUESTED"},
                "payments": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/payments",
                             "state": "NOT_REQUESTED"},
                "kidsSberCards": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/kidsSberCards",
                                  "state": "SUCCESS"},
                "services": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/services",
                             "state": "NOT_REQUESTED"},
                "investments": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/investments",
                                "state": "NOT_REQUESTED"},
                "geomap": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/geomap",
                           "state": "NOT_REQUESTED"}, "sberThanks": {"data": [
                    {"id": 1, "order": 2, "hidden": False, "loyaltyType": "SBERSPASIBO", "state": "PARTICIPANT",
                     "balance": {"amount": "0.00", "status": "ACTIVE"}, "location": ["wallet", "header"]}],
                    "url": "/main-screen/rest/v2/mobile/section/data/sberThanks",
                    "state": "SUCCESS"},
                "recommended": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/recommended",
                                "state": "NOT_REQUESTED"},
                "pensions": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/pensions",
                             "state": "NOT_REQUESTED"}, "ctaccounts": {"data": format_cards_small(self.api.get_cards()),
                                                                       "url": "/main-screen/rest/v2/mobile/section/data/ctaccounts",
                                                                       "state": "SUCCESS"},
                "obpctaccounts": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/obpctaccounts",
                                  "state": "SUCCESS"},
                "kidsCards": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/kidsCards",
                              "state": "SUCCESS"}, "accounts": {"data": [
                    {"id": 3600104275103400, "name": "Текущий счет", "rate": "0.00", "closeDate": "01.01.2099",
                     "number": "40817810668781584175",
                     "balance": {"amount": "26.13", "currency": {"code": "RUB", "name": "руб."}},
                     "availCash": {"amount": "26.13", "currency": {"code": "RUB", "name": "руб."}}, "state": "OPENED",
                     "moneyBoxAvailable": False, "arrested": False, "showArrestDetail": True}],
                    "url": "/main-screen/rest/v2/mobile/section/data/accounts",
                    "state": "SUCCESS"},
                "ima": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/ima", "state": "SUCCESS"},
                "expenses": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/expenses",
                             "state": "NOT_REQUESTED"}, "currencyRates": {"data": [
                    {"type": "ERNP-2", "description": "CURRENCY_ACCOUNTS", "rates": [
                        {"base": "CNY", "quote": "RUB", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "13.1200", "offer": "13.7000", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "NONE", "trendOffer": "NONE"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "USD", "quote": "RUB", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "91.7000", "offer": "99.8000", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "NONE", "trendOffer": "NONE"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "AED", "quote": "RUB", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "25.2400", "offer": "27.4900", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "DOWN", "trendOffer": "NONE"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "KZT", "quote": "RUB", "lotSize": 100, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "19.0300", "offer": "20.6000", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "NONE", "trendOffer": "NONE"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "BYN", "quote": "RUB", "lotSize": 1, "trend": "DOWN",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "28.0300", "offer": "30.7800", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "UP", "trendOffer": "DOWN"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "INR", "quote": "RUB", "lotSize": 10, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "11.1000", "offer": "12.0800", "minimumVolume": "0",
                             "maximumVolume": "499999.99999999", "trendBid": "NONE", "trendOffer": "NONE"},
                            {"bid": "11.3400", "offer": "11.6000", "minimumVolume": "500000",
                             "maximumVolume": "9999999999.99", "trendBid": "NONE", "trendOffer": "NONE"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "EUR", "quote": "RUB", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "98.1000", "offer": "109.1000", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "NONE", "trendOffer": "NONE"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "GBP", "quote": "RUB", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "106.1000", "offer": "136.5000", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "NONE", "trendOffer": "NONE"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "CHF", "quote": "RUB", "lotSize": 1, "trend": "UP", "startDate": "2024-10-19T00:02:18",
                         "ranges": [{"bid": "90.9200", "offer": "119.8400", "minimumVolume": "0",
                                     "maximumVolume": "9999999999.99", "trendBid": "UP", "trendOffer": "UP"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "JPY", "quote": "RUB", "lotSize": 100, "trend": "UP",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "52.5100", "offer": "71.5900", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "UP", "trendOffer": "UP"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "SGD", "quote": "RUB", "lotSize": 1, "trend": "UP", "startDate": "2024-10-19T00:02:18",
                         "ranges": [{"bid": "60.2900", "offer": "82.5400", "minimumVolume": "0",
                                     "maximumVolume": "9999999999.99", "trendBid": "NONE", "trendOffer": "UP"}],
                         "volatilities": [], "variabilities": []}]},
                    {"type": "ERNP-2", "description": "CROSS_CURRENCY_RATES", "rates": [
                        {"base": "CNY", "quote": "USD", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "0.1322", "offer": "0.1486", "minimumVolume": "0", "maximumVolume": "9999999999.99",
                             "trendBid": "NONE", "trendOffer": "NONE"}], "volatilities": [], "variabilities": []},
                        {"base": "AED", "quote": "USD", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "0.2602", "offer": "0.2804", "minimumVolume": "0", "maximumVolume": "9999999999.99",
                             "trendBid": "NONE", "trendOffer": "NONE"}], "volatilities": [], "variabilities": []},
                        {"base": "USD", "quote": "CNY", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "6.7317", "offer": "7.5654", "minimumVolume": "0", "maximumVolume": "9999999999.99",
                             "trendBid": "NONE", "trendOffer": "NONE"}], "volatilities": [], "variabilities": []},
                        {"base": "USD", "quote": "AED", "lotSize": 1, "trend": "NONE",
                         "startDate": "2024-10-19T00:02:18", "ranges": [
                            {"bid": "3.5662", "offer": "3.8432", "minimumVolume": "0", "maximumVolume": "9999999999.99",
                             "trendBid": "NONE", "trendOffer": "NONE"}], "volatilities": [], "variabilities": []}]},
                    {"type": "ERNP-4", "description": "CARDS", "rates": [
                        {"base": "USD", "quote": "RUB", "lotSize": 1, "trend": "DOWN",
                         "startDate": "2024-10-19T06:00:01", "ranges": [
                            {"bid": "91.7100", "offer": "104.5500", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "UP", "trendOffer": "DOWN"}],
                         "volatilities": [], "variabilities": []},
                        {"base": "EUR", "quote": "RUB", "lotSize": 1, "trend": "DOWN",
                         "startDate": "2024-10-19T06:00:01", "ranges": [
                            {"bid": "99.8300", "offer": "114.9200", "minimumVolume": "0",
                             "maximumVolume": "9999999999.99", "trendBid": "UP", "trendOffer": "DOWN"}],
                         "volatilities": [], "variabilities": []}]},
                    {"type": "PMR-3", "description": "METAL_ACCOUNTS", "packageCode": "0", "rates": [
                        {"base": "A98", "quote": "RUB", "trend": "DOWN", "startDate": "2024-10-18T23:48:41", "ranges": [
                            {"bid": "7922", "offer": "8706", "minimumVolume": "0", "maximumVolume": "9999999999.99",
                             "trendBid": "UP", "trendOffer": "DOWN"}],
                         "volatilities": [{"period": "за день", "value": "0.0", "percent": "0.0"},
                                          {"period": "за месяц", "value": "822.0", "percent": "10.4"},
                                          {"period": "за год", "value": "2428.0", "percent": "38.7"}],
                         "variabilities": [{"type": "offer", "period": "за день", "value": "0.0", "percent": "0.0"},
                                           {"type": "bid", "period": "за день", "value": "0.0", "percent": "0.0"},
                                           {"type": "offer", "period": "за месяц", "value": "822.0", "percent": "10.4"},
                                           {"type": "bid", "period": "за месяц", "value": "704.0", "percent": "9.8"},
                                           {"type": "offer", "period": "за год", "value": "2428.0", "percent": "38.7"},
                                           {"type": "bid", "period": "за год", "value": "2183.0", "percent": "38.0"}]},
                        {"base": "A99", "quote": "RUB", "trend": "UP", "startDate": "2024-10-18T23:48:41", "ranges": [
                            {"bid": "96.55", "offer": "110.04", "minimumVolume": "0", "maximumVolume": "9999999999.99",
                             "trendBid": "UP", "trendOffer": "UP"}],
                         "volatilities": [{"period": "за день", "value": "0.0", "percent": "0.0"},
                                          {"period": "за месяц", "value": "15.6", "percent": "16.5"},
                                          {"period": "за год", "value": "34.2", "percent": "45.0"}],
                         "variabilities": [{"type": "offer", "period": "за день", "value": "0.0", "percent": "0.0"},
                                           {"type": "bid", "period": "за день", "value": "0.0", "percent": "0.0"},
                                           {"type": "offer", "period": "за месяц", "value": "15.6", "percent": "16.5"},
                                           {"type": "bid", "period": "за месяц", "value": "13.2", "percent": "15.9"},
                                           {"type": "offer", "period": "за год", "value": "34.2", "percent": "45.0"},
                                           {"type": "bid", "period": "за год", "value": "29.3", "percent": "43.6"}]},
                        {"base": "A76", "quote": "RUB", "trend": "UP", "startDate": "2024-10-18T23:48:41", "ranges": [
                            {"bid": "2885", "offer": "3319", "minimumVolume": "0", "maximumVolume": "9999999999.99",
                             "trendBid": "UP", "trendOffer": "UP"}],
                         "volatilities": [{"period": "за день", "value": "0.0", "percent": "0.0"},
                                          {"period": "за месяц", "value": "243.0", "percent": "7.9"},
                                          {"period": "за год", "value": "267.0", "percent": "8.7"}],
                         "variabilities": [{"type": "offer", "period": "за день", "value": "0.0", "percent": "0.0"},
                                           {"type": "bid", "period": "за день", "value": "0.0", "percent": "0.0"},
                                           {"type": "offer", "period": "за месяц", "value": "243.0", "percent": "7.9"},
                                           {"type": "bid", "period": "за месяц", "value": "217.0", "percent": "8.1"},
                                           {"type": "offer", "period": "за год", "value": "267.0", "percent": "8.7"},
                                           {"type": "bid", "period": "за год", "value": "464.0", "percent": "19.2"}]},
                        {"base": "A33", "quote": "RUB", "trend": "UP", "startDate": "2024-10-18T23:48:41", "ranges": [
                            {"bid": "3093", "offer": "3579", "minimumVolume": "0", "maximumVolume": "9999999999.99",
                             "trendBid": "UP", "trendOffer": "UP"}],
                         "volatilities": [{"period": "за день", "value": "0.0", "percent": "0.0"},
                                          {"period": "за месяц", "value": "187.0", "percent": "5.5"},
                                          {"period": "за год", "value": "-318.0", "percent": "8.2"}],
                         "variabilities": [{"type": "offer", "period": "за день", "value": "0.0", "percent": "0.0"},
                                           {"type": "bid", "period": "за день", "value": "0.0", "percent": "0.0"},
                                           {"type": "offer", "period": "за месяц", "value": "187.0", "percent": "5.5"},
                                           {"type": "bid", "period": "за месяц", "value": "167.0", "percent": "5.7"},
                                           {"type": "offer", "period": "за год", "value": "-318.0", "percent": "8.2"},
                                           {"type": "bid", "period": "за год", "value": "-19.0", "percent": "0.6"}]}]}],
                    "url": "/main-screen/rest/v2/mobile/section/data/currencyRates",
                    "state": "SUCCESS"},
                "goals": {"data": [], "url": "/main-screen/rest/v2/mobile/section/data/goals", "state": "SUCCESS"}}}}}}

    def response(self, flow: http.HTTPFlow):
        url = flow.request.pretty_url
        try:
            r = json.loads(flow.response.content)
        except Exception as e:
            r = {}

        if 'online.sberbank.ru:8543/sm-uko/v3/mobile/gzip/session/create' in url:
            settings = self.api.get_settings()
            try:
                f, i, o = settings['fio'].split()
            except:
                f, i, o = 'Скам Скамыч Скаменко'.split()
            r["body"]["clientInfo"]["person"]["firstName"] = i
            r["body"]["clientInfo"]["person"]["secondName"] = f
            r["body"]["clientInfo"]["person"]["middleName"] = o
            r["body"]["clientInfo"]["person"]["phones"][0] = settings['phone']
            flow.response = http.Response.make(flow.response.status_code, json.dumps(r), flow.response.headers)

        if 'online.sberbank.ru:8543/pfpv_alf_mb/v1.00/alf/amounts' in url:
            settings = self.api.get_settings()
            r['body']['amounts'][0]['nationalAmount']['amount'] = settings['income']
            r['body']['amounts'][0]['visibleAmount']['amount'] = settings['income']
            flow.response = format_response(r)

        if 'online.sberbank.ru:8543/transfer/enter/v1/workflow?cmd=START&name=enterFlow' in url or \
                'online.sberbank.ru:8543/transfer/partner-bank-phone/send/v1/workflow?cmd=START&name=sendFlow' in url:
            balance = self.api.get_card_balance(1)
            self.name = r["body"]["output"]["screens"][0]["widgets"][0]["fields"][0]["title"]
            self.phone = r["body"]["output"]["screens"][0]["widgets"][0]["fields"][0]["value"]
            r["body"]["output"]["references"]["resourceList"]["items"][0]["properties"]["balance"] = balance
            flow.response = format_response(r)
        if 'online.sberbank.ru:8543/transfer/partner-bank-phone/send/v1/workflow?cmd=EVENT' in url:
            balance = self.api.get_card_balance(1)
            if r.get('body'):
                r["body"]["output"]["references"]["resourceList"]["items"][0]["properties"]["balance"] = balance
                r["body"]["output"]["screens"][0]["footer"][0]["events"][0]["title"] = f'Перевести {self.amount} ₽'
                r["body"]["output"]["screens"][0]["widgets"][3]["fields"][1]["description"] = 'Комиссия — 0 ₽'
                r["body"]["output"]["screens"][0]["widgets"][3]["fields"][1]["value"] = f"{self.amount} ₽"
                self.name = r["body"]["output"]["screens"][0]["widgets"][3]["fields"][0]["value"]
                self.phone = r["body"]["output"]["screens"][0]["widgets"][2]["fields"][0]["value"]
                flow.response = format_response(r)
        if 'online.sberbank.ru:8543/p2ptransfer-xb-card/v1/workflow?cmd=START' in url:
            card = self.api.get_card(1)
            r['body']['output']['references']['fromResource']['items'][0]["properties"]["balance"] = card['balance']
            r['body']['output']['references']['fromResource']['items'][0]["properties"]["maskedNumber"] = '•• ' + card[
                                                                                                                      'number'][
                                                                                                                  -4:]
            r['body']['output']['references']['fromResource']['items'][0]['title'] = 'Платёжный счёт •• ' + card[
                                                                                                                'number'][
                                                                                                            -4:]

            flow.response = format_response(r)

        if 'messenger.sberbank.ru/api/payment/v2/p2p/save' in url:
            d = r['data']
            req = json.loads(flow.request.content)
            self.amount = req['amount']
            card = self.api.get_card(1)
            d['amount'] = self.amount
            d['amount_in_rub'] = self.amount
            d['fee'] = 0.0
            d['available_accounts'][0]['title'] = f"Платёжный счёт {card['balance']} ₽"
            d['available_accounts'][0]['properties']['masked_number'] = card['number']
            d['available_accounts'][0]['properties']['number'] = card['number']
            d['available_accounts'][0]['properties']['balance'] = card['balance']
            if r.get('warning'):
                del r['warning']
            flow.response = format_response(r)

        if 'online.sberbank.ru:8543/uoh-bh/v1/operations/list' in url:
            def transform(op):
                return {
                    "uohId": str(op['id']),
                    "ufsId": str(op['id']),
                    "date": datetime.strptime(op['timestamp'], "%a, %d %b %Y %H:%M:%S GMT").strftime(
                        "%d.%m.%YT%H:%M:%S"),
                    "creationChannel": 3,
                    "form": "UfsP2PSBPOutTransfer",
                    "state": {
                        "name": "EXECUTED",
                        "category": "executed"
                    },
                    "description": "Перевод по СБП",
                    "fromResource": {
                        "id": "card:3900034455303300",
                        "displayedValue": " •• 9340"
                    },
                    "correspondent": op['receiver_name'],
                    "operationAmount": {
                        "amount": -op['amount'],
                        "currencyCode": "RUB"
                    },
                    "nationalAmount": {
                        "amount": -op['amount'],
                        "currencyCode": "RUB"
                    },
                    "commission": {
                        "amount": 0.00,
                        "currencyCode": "RUB"
                    },
                    "attributes": {
                        "copyable": False,
                        "nfc": False,
                        "cashReceipt": False,
                        "compositePayment": False
                    },
                    "type": "ufsPayment",
                    "billingAmount": {
                        "amount": 41.70,
                        "currencyCode": "RUB"
                    },
                    "externalId": str(op['id']),
                    "isFinancial": True
                }

            ops = [transform(op) for op in self.api.get_history()]
            flow.response = format_response(
                {
                    "success": True,
                    "body": {
                        "operations": ops + r['body']['operations']
                    }
                }
            )

        if 'online.sberbank.ru:8543/p2ptransfer-xb-card/v1/workflow?cmd=EVENT' in url:
            card = self.api.get_card(1)
            r["body"]["output"]["screens"][0]["widgets"][2]["fields"][0]["value"] = self.amount
            r["body"]["output"]["screens"][0]["widgets"][2]["fields"][1]["value"] = self.amount + 30

            r["body"]["output"]["references"]["resourceList"]["items"][0]["properties"]["maskedNumber"] = card['number']
            r["body"]["output"]["references"]["resourceList"]["items"][0]["properties"]["balance"] = card['balance']
            r["body"]["output"]["screens"][0]["footer"][0]["events"][0]["title"] = f"Перевести {self.amount} ₽"
            flow.response = format_response(r)

    def request(self, flow: http.HTTPFlow):
        url = flow.request.pretty_url

        if 'online.sberbank.ru:8543/sbptransfer/v1/workflow?cmd=START&name=main' in url:
            req = json.loads(flow.request.content)
            op = self.api.get_operation(req['document']['srcDocumentId'])
            self.op = op
            flow.response = format_response({"success": True, "body": {"result": "SUCCESS",
                                                                       "pid": "cffd7dfe-8faf-11ef-add9-e9d511af02f9",
                                                                       "flow": "info", "state": "showInfo", "output": {
                    "screens": [{"properties": {"status": "success", "disabledAnimation": True,
                                                "eventForAnalytic": "INFOdirect_showInfo_success"},
                                 "type": "StatusScreen", "header": [
                            {"type": "StatusNavBar", "title": "Перевод отправлен",
                             "description": f"{op['amount']} ₽ → Алексей Андреевич Ф",
                             "properties": {"status": "success"},
                             "events": [{"cmd": "EXIT", "name": "exit", "type": "exit"}]},
                            {"type": "StatusHeaderIcon", "properties": {"status": "success"}},
                            {"type": "StatusHeaderResult", "title": "Перевод отправлен",
                             "description": f"{op['amount']} ₽"},
                            {"type": "StatusHeaderSummary", "title": f"В {op['receiver_bank']} через СБП",
                             "description": op['receiver_name']}], "widgets": [{"type": "StatusWhatNext", "fields": [
                            {"id": "sbptransfer:status:whatnext", "type": "text", "format": "string",
                             "value": "Узнать о зачислении денежных средств на счёт вы можете у получателя перевода",
                             "title": "Статус перевода"}]}, {"type": "CoreSavePDF",
                                                             "title": "Сохранить или отправить чек",
                                                             "properties": {"styleBtn": "CHECK_ORDER",
                                                                            "url": "/sbptransfer/v1/receipt/UfsP2PSBPOutTransfer/" + str(
                                                                                op['id'])}},
                                                                               {"type": "CoreCollapse", "fields": [{
                                                                                   "id": "CoreCollapse:paymentDetails",
                                                                                   "type": "checkbox",
                                                                                   "value": "False",
                                                                                   "title": "Подробности операции",
                                                                                   "style": "info"}]},
                                                                               {"type": "CoreFieldSet", "visible": {
                                                                                   "id": "CoreCollapse:paymentDetails",
                                                                                   "regexp": "True"}, "fields": [
                                                                                   {"id": "sbptransfer:init:phone",
                                                                                    "type": "text", "format": "phone",
                                                                                    "value": op['receiver_number'],
                                                                                    "title": "Номер телефона получателя",
                                                                                    "style": "phone",
                                                                                    "readonly": True},
                                                                                   {"id": "sbptransfer:init:name",
                                                                                    "type": "text",
                                                                                    "value": op['receiver_name'],
                                                                                    "title": "ФИО получателя",
                                                                                    "style": "user",
                                                                                    "readonly": True}, {
                                                                                       "id": "sbptransfer:init:targetBank",
                                                                                       "type": "text",
                                                                                       "value": op['receiver_bank'],
                                                                                       "title": "Банк получателя",
                                                                                       "style": "branch",
                                                                                       "readonly": True},
                                                                                   {"id": "sbptransfer:init:summ",
                                                                                    "type": "text", "format": "money",
                                                                                    "formatConfig": "RUB",
                                                                                    "value": op['amount'],
                                                                                    "title": "Сумма перевода",
                                                                                    "style": "moneyPocket",
                                                                                    "readonly": True}]},
                                                                               {"type": "CoreFieldSet", "visible": {
                                                                                   "id": "CoreCollapse:paymentDetails",
                                                                                   "regexp": "True"}, "fields": [{
                                                                                   "id": "sbptransfer:init:commission",
                                                                                   "type": "text",
                                                                                   "format": "money",
                                                                                   "formatConfig": "RUB",
                                                                                   "value": "0",
                                                                                   "title": "Комиссия",
                                                                                   "style": "commission",
                                                                                   "readonly": True}]},
                                                                               {"type": "CoreFieldSet", "visible": {
                                                                                   "id": "CoreCollapse:paymentDetails",
                                                                                   "regexp": "True"}, "fields": [{
                                                                                   "id": "sbptransfer:init:outcomeAccount",
                                                                                   "type": "select",
                                                                                   "format": "resource",
                                                                                   "referenceId": "accounts",
                                                                                   "value": "once_id",
                                                                                   "title": "Счёт списания",
                                                                                   "readonly": True}]},
                                                                               {"type": "CoreFieldSet", "visible": {
                                                                                   "id": "CoreCollapse:paymentDetails",
                                                                                   "regexp": "True"}, "fields": [
                                                                                   {"id": "sbptransfer:init:sbpId",
                                                                                    "type": "text",
                                                                                    "value": "A4293055623450170000000011360501",
                                                                                    "title": "Номер операции в СБП",
                                                                                    "style": "documentSeriesNumber",
                                                                                    "readonly": True},
                                                                                   {"id": "sbptransfer:init:operDate",
                                                                                    "type": "text",
                                                                                    "value": datetime.strptime(
                                                                                        op['timestamp'],
                                                                                        "%a, %d %b %Y %H:%M:%S GMT").strftime(
                                                                                        "%d.%m.%YT%H:%M:%S"),
                                                                                    "title": "Дата и время операции (МСК)",
                                                                                    "style": "calendar",
                                                                                    "readonly": True}]},
                                                                               {"type": "QpsLogo", "visible": {
                                                                                   "id": "CoreCollapse:paymentDetails",
                                                                                   "regexp": "True"}, "fields": [
                                                                                   {"id": "sbptransfer:qpsLogo",
                                                                                    "type": "text",
                                                                                    "style": "qps_grey"}]}],
                                 "footer": [{"type": "CoreButtons", "events": [
                                     {"cmd": "EXIT", "name": "exit", "type": "exit", "title": "Вернуться назад"}]}]}],
                    "references": {"accounts": {"items": [{"title": "", "value": "once_id",
                                                           "properties": {"title": "MIR", "type": "card",
                                                                          "paymentSystem": "mir",
                                                                          "name": "",
                                                                          "maskedNumber": "•••• 9340",
                                                                          "number": "•••• 9340", "currency": "",
                                                                          "balance": "", "asideMeasureUnit": " "}}]}}},
                                                                       "history": [{
                                                                           "id": "d016d272-8faf-11ef-add9-dfa52c5e79a8",
                                                                           "flow": "info",
                                                                           "state": "showInfo",
                                                                           "title": "Детальная информация по переводу",
                                                                           "status": "ACTIVE",
                                                                           "flowId": 2}]}})

        if 'online.sberbank.ru:8543/main-screen/rest/v2/mobile/section/meta' in url:
            flow.response = format_response(self.get_accounts())

        if 'online.sberbank.ru:8543/ufs-carddetail/rest/cta/v1/ctaInfo' in url:
            cards = format_cards(self.api.get_cards())

            flow.response = format_response({"success": True, "body": {"ctaDetails": {"cta": [
                {"id": 3900008975103250, "name": "Платёжный счёт", "description": "Платёжный счёт",
                 "number": ('9999999999999999' + cards[0]['chet'])[-20:],
                 "balance": {"amount": sum(card['balance'] for card in cards),
                             "currency": {"code": "RUB", "name": "руб."}}, "state": "active",
                 "isArrested": False, "thirdPersons": [], "sbercardLevel": 2, "contractOpenDate": "15/10/2024",
                 "isCtaNew": True, "background": {"imageLight": "screenBackgroundLvl_2_L.jpg",
                                                  "imageDark": "screenBackgroundLvl_2_D.jpg"}, "cards":
                     cards, "ctaOptions": {"payrollAccount": False},
                 "optionsPermissions": {"isSbercardTariffV3": True, "needLimitForPensionProduct": False}}
            ], "widgets": [
                {"type": "SurveyStarsRestEntryPoint", "title": "Оцените, насколько вы довольны платёжным счётом",
                 "description": "Расскажите подробнее. Это займет пару минут", "properties": {
                    "deeplink": "android-app://ru.sberbankmobile/customersurvey?flowName=survey&eventTypeId=465&return=entry_point&chance=1_70",
                    "launcherFeatureName": "BottomSheetEntryPoint"}}], "clientOptions": {"salaryClient": False,
                                                                                         "newLikeSalaryClient": False,
                                                                                         "seamlessLikeSalaryClient": False,
                                                                                         "likeSalaryConditionsDone": False},
                "references": [{
                    "key": "cardSettingsWidget.title",
                    "value": "Давайте настроим карту"},
                    {
                        "key": "cardSettingsWidget.activateCard.title",
                        "value": "Активировать\nкарту"},
                    {
                        "key": "cardSettingsWidget.orderPlastic.title",
                        "value": "Заказать\nпластик"},
                    {
                        "key": "cardSettingsWidget.setPin.title",
                        "value": "Установить\nПИН-код"},
                    {
                        "key": "cardSettingsWidget.setDesign.title",
                        "value": "Выбрать\nдизайн"},
                    {
                        "key": "cardSettingsWidget.activateCard.androidImageUrl",
                        "value": "https://cdn.sberbank.ru/designcards/mobile/cta/cardSettingsWidget/activateCard.png"},
                    {
                        "key": "cardSettingsWidget.orderPlastic.androidImageUrl",
                        "value": "https://cdn.sberbank.ru/designcards/mobile/cta/cardSettingsWidget/orderPlastic.png"},
                    {
                        "key": "cardSettingsWidget.setPin.androidImageUrl",
                        "value": "https://cdn.sberbank.ru/designcards/mobile/cta/cardSettingsWidget/setPin.png"},
                    {
                        "key": "cardSettingsWidget.setDesign.androidImageUrl",
                        "value": "https://cdn.sberbank.ru/designcards/mobile/cta/cardSettingsWidget/setDesign.png"},
                    {
                        "key": "redesignPaymentAccount.fileStorageUrl.android",
                        "value": "https://cms-res.online.sberbank.ru/transwallet/redesign/android/"},
                    {
                        "key": "redesignPaymentAccount.educationCTAccountCategoryUrl.android",
                        "value": "https://online.sberbank.ru/app/edutainment/library/category?id=11"},
                    {
                        "key": "replenishMe2MeSBP.imageUrl.android",
                        "value": "https://cms-res.online.sberbank.ru/transwallet/replenishMe2MeSBPImage.png"},
                    {
                        "key": "sbercardTariffWidget.title",
                        "value": "Условия тарифа"},
                    {
                        "key": "sbercardTariffWidget.subtitle",
                        "value": "Стоимость, бонусы и лимиты"},
                    {
                        "key": "sbercardTariffWidget.buttonName",
                        "value": "Посмотреть"},
                    {
                        "key": "sbercardTariffWidget.icon",
                        "value": "ds_ic_36_document_checkmark"},
                    {
                        "key": "sbercardTariffWidget.highLevelIcon",
                        "value": "ds_ic_36_crown"},
                    {
                        "key": "sbercardTariffWidget.travelIcon",
                        "value": "ds_ic_36_plane"},
                    {
                        "key": "settingForDisplayInfomessages.displayFrequencyPerDay",
                        "value": "3"}]}}})

        if 'online.sberbank.ru:8543/transfer/enter/v1/validate' in url:
            self.amount = float(json.loads(flow.request.data.content)['fromAmount'])
            flow.response = format_response({"success": True, "body": {"descriptionFromAmount": "Комиссия 0 ₽",
                                                                       "commissionFromAmount": "0",
                                                                       "commissionFromCurrency": "RUB",
                                                                       "validation": False}})

        if 'online.sberbank.ru:8543/pfpv_alf_mb/v1.00/alf/amounts' in url:
            settings = self.api.get_settings()
            transfer = settings['transfer']
            total_spend = settings['spending']

            flow.response = format_response({"success": True, "body": {"amounts": [
                {"from": "2024-10-01T00:00:00+04:00", "to": "2024-10-31T23:59:59+04:00", "incomeType": "income",
                 "nationalAmount": {"amount": "30.00", "currency": "RUB"},
                 "visibleAmount": {"amount": "30.00", "currency": "RUB"}, "categoryAmounts": [
                    {"id": 216, "name": "Переводы от людей", "externalId": "16", "hiddenCategoryFilter": False,
                     "nationalAmount": {"amount": "30.00", "currency": "RUB"},
                     "visibleAmount": {"amount": "30.00", "currency": "RUB"}, "countOperations": 2,
                     "countHiddenOperations": 0}], "productAmounts": [
                    {"type": "CARD", "id": "3900034455303300", "status": "ACTIVE", "channelVisibility": True,
                     "alfVisibility": True, "visibleAmount": {"amount": "0.00", "currency": "RUB"}},
                    {"type": "CT_ACCOUNT", "id": "3900008975103250", "status": "ACTIVE", "channelVisibility": True,
                     "alfVisibility": True, "visibleAmount": {"amount": "30.00", "currency": "RUB"}}]},
                {"from": "2024-10-01T00:00:00+04:00", "to": "2024-10-31T23:59:59+04:00", "incomeType": "outcome",
                 "nationalAmount": {"amount": transfer, "currency": "RUB"},
                 "visibleAmount": {"amount": total_spend, "currency": "RUB"}, "plan": {"status": "UNSET"},
                 "categoryAmounts": [
                     {"id": 202, "name": "Переводы людям", "externalId": "2", "hiddenCategoryFilter": False,
                      "nationalAmount": {"amount": transfer, "currency": "RUB"},
                      "visibleAmount": {"amount": transfer, "currency": "RUB"}, "countOperations": 1,
                      "countHiddenOperations": 0}], "productAmounts": [
                    {"type": "CARD", "id": "3900034455303300", "status": "ACTIVE", "channelVisibility": True,
                     "alfVisibility": True, "visibleAmount": {"amount": "0.00", "currency": "RUB"}},
                    {"type": "CT_ACCOUNT", "id": "3900008975103250", "status": "ACTIVE", "channelVisibility": True,
                     "alfVisibility": True, "visibleAmount": {"amount": transfer, "currency": "RUB"}}]}]}})

        if 'online.sberbank.ru:8543/transfer/partner-bank-phone/send/v1/workflow?cmd=EVENT' in url:
            if 'name=on-return' in url and self.name and self.amount:
                import random
                r = {"success": True,
                     "body": {"result": "SUCCESS", "pid": "122734de-8af3-11ef-8c7c-5b8d043b1323", "flow": "sendFlow",
                              "state": "statusScreen", "output": {"screens": [{"properties": {
                             "eventForAnalytic": "Status", "paramsForAnalytic": [
                                 "[{\"eventName\":\"Transfer PartnerPhone TransferBpPhone Status Show",
                                 "\",\"type\":\"UIEventShow\",\"properties\":{\"status\":\"OK\",\"bank\":\"54424",
                                 "3324385\",\"prod\":\"payAcc\",\"source\":\"pro\"}},{\"eventName\":\"Transfer",
                                 " PartnerPhone TransferBpPhone Status exit Click\",\"type\":\"exit\",\"",
                                 "properties\":{\"status\":\"OK\",\"bank\":\"544243324385\",\"prod\":\"payAcc\"",
                                 ",\"source\":\"pro\"}},{\"eventName\":\"Transfer PartnerPhone TransferBp",
                                 "Phone Status saveCheck Click\",\"type\":\"horizontalCards:saveCheck\"",
                                 ",\"properties\":{\"status\":\"OK\",\"bank\":\"544243324385\",\"prod\":\"payAc",
                                 "c\",\"source\":\"pro\"}},{\"eventName\":\"Transfer PartnerPhone Transfer",
                                 "BpPhone Status repeat Click\",\"type\":\"repeat\",\"properties\":{\"stat",
                                 "us\":\"OK\",\"bank\":\"544243324385\",\"prod\":\"payAcc\",\"source\":\"pro\"}}]"],
                             "status": "success", "disabledAnimation": False, "noneTransitionAnimation": True},
                             "type": "StatusScreen2021", "header": [
                                 {"type": "StatusNavBar", "title": "Перевод выполнен",
                                  "events": [{"cmd": "EXIT", "name": "exit", "type": "exit"}]},
                                 {"type": "StatusHeader2021", "title": f"{self.amount} ₽",
                                  "description": self.bank,
                                  "properties": {"style": "summary",
                                                 "accessibilityTitle": f"{self.amount} рублей 00 копеек",
                                                 "accessibilityDescription": self.bank}},
                                 {"type": "HorizontalCards", "fields": [
                                     {"id": "horizontalCards:saveCheck", "type": "text", "format": "string",
                                      "title": "Сохранить\nчек", "style": "ds_ic_36_receipt"},
                                     {"id": "repeat", "type": "text", "format": "string",
                                      "style": "ds_ic_36_arrow_clockwise", "title": "Повторить\nоперацию"}], "events": [
                                     {"uri": "click:horizontalcards.saveCheck", "name": "horizontalCards:saveCheck"},
                                     {"name": "repeat", "cmd": "EVENT"}]}], "widgets": [
                                 {"type": "CoreSavePDF", "title": "Сохранить или отправить чек",
                                  "visible": {"id": "requisite:fromResource", "regexp": "False"}, "properties": {
                                     "url": "/transfer/partner-bank-phone/send/v1/receipt?documentId=" + str(
                                         random.randint(int(1e6), int(1e7)))},
                                  "strategies": [{"fieldLookupId": "horizontalCards:saveCheck",
                                                  "type": "horizontalCardsStrategy"}]},
                                 {"type": "StatusWhatNext", "title": "Подробности"}, {"type": "CoreResource",
                                                                                      "fields": [{
                                                                                          "id": "requisite:fromResource",
                                                                                          "type": "select",
                                                                                          "style": "noIcon",
                                                                                          "readonly": True,
                                                                                          "format": "resource",
                                                                                          "title": "Откуда",
                                                                                          "referenceId": "resourceList",
                                                                                          "value": "transactionAccount:3900008975103250"}]},
                                 {"type": "CustomThemeWithRemoteIcon",
                                  "properties": {"iconUrl": "https://cms-res.online.sberbank.ru/uts_p2p/TinkoFF.png",
                                                 "customTheme": False, "isAutoTransferWidget": False}, "fields": [
                                     {"id": "id:CustomThemeWithRemoteIcon", "type": "text", "title": "Куда",
                                      "value": self.phone, "description": self.bank,
                                      "style": "ds_ic_36_building_fill"}]}, {"type": "CoreFieldSet", "fields": [
                                     {"id": "id:CoreFieldSet1", "type": "text", "title": "Получатель",
                                      "value": self.name, "readonly": True},
                                     {"id": "id:CoreFieldSet2", "type": "text", "style": "noIcon", "readonly": True,
                                      "format": "money", "formatConfig": "RUB", "title": "Сколько",
                                      "value": f"{self.amount} ₽"},
                                     {"id": "id:CoreFieldSet3", "type": "text", "style": "noIcon", "readonly": True,
                                      "format": "money", "formatConfig": "RUB", "title": "Комиссия", "value": "0 ₽"},
                                     {"id": "id:CoreFieldSet5", "type": "text", "title": "Номер документа",
                                      "value": "20241015154333bbbb1aa385ca54d3c93148", "readonly": True}]}], "footer": [
                                 {"type": "CoreButtons", "properties": {"nonBlocking": True}, "events": [
                                     {"cmd": "EXIT", "name": "exit", "title": "Вернуться на главный",
                                      "uri": "app:mainScreen"}]}]}], "references": {"resourceList": {"items": [
                             {"title": "", "value": "transactionAccount:3900008975103250",
                              "properties": {"type": "payAccount", "name": "Платёжный счёт", "style": "payAccountRuble",
                                             "maskedNumber": "•• " + self.api.get_card(1)['chet']}}]}}}, "history": [
                             {"id": "30090c19-8af3-11ef-8c7c-993017db4464", "flow": "sendFlow", "state": "statusScreen",
                              "title": "OnEnter:statusScreen", "value": "statusScreen", "status": "ACTIVE",
                              "flowId": 1}, {"id": "2ebfea66-8af3-11ef-b586-99880197865a", "flow": "confirmClientIb",
                                             "state": "rollback", "title": "Переход", "value": "", "status": "ACTIVE",
                                             "flowId": 3},
                             {"id": "17b4b723-8af3-11ef-8c7c-cb45be4eb13e", "flow": "sendFlow", "state": "confirmation",
                              "title": "OnEnter:confirmation", "value": "confirmation", "status": "ACTIVE",
                              "flowId": 1}, {"id": "1239f996-8af3-11ef-8c7c-51de3d6d62d0", "flow": "sendFlow",
                                             "state": "requisitesInput", "title": "OnEnter:requisitesInput",
                                             "value": "requisitesInput", "status": "ACTIVE", "flowId": 1}]}}
                flow.response = format_response(r)
                self.api.insert_operation({
                    'type': 'outcome',
                    'amount': self.amount,
                    'title': 'Перевод ' + self.name,
                    'receiver_name': self.name,
                    'receiver_number': self.phone,
                    'receiver_bank': self.bank,
                })
            elif 'name=next' in url and flow.request.data.content.decode('utf-8') == '{}':
                flow.response = format_response({
                    "body": {
                        "pid": flow.request.query.get('pid'),
                        "result": "EXTERNAL_ENTER",
                        "url": "/bh-confirmation/v3/workflow2"
                    },
                    "success": True
                })
            else:
                r = json.loads(flow.request.data.content)
                if r.get('fields'):
                    self.amount = float(r['fields']['requisite:transferAmount'])
                    r['fields']['requisite:transferAmount'] = '10.00'
                    flow.request = http.Request.make(flow.request.method, url, json.dumps(r), flow.request.headers)
                else:
                    flow.response = format_response({'success': True, "body": {
                        "pid": flow.request.query.get('pid'),
                        "result": "END"
                    }})

        if 'online.sberbank.ru:8543/transfer/enter/v1/workflow?cmd=EVENT' in url:
            flow.response = format_response({
                "body": {
                    "module": "ClTransfers",
                    "pid": flow.request.query.get('pid'),
                    "result": "EXTERNAL_ENTER",
                    "url": "/cltransfer/v1/workflow"
                },
                "success": True
            })
        if 'online.sberbank.ru:8543/cltransfer/v1/workflow?cmd=EVENT' in url:
            flow.response = format_response({
                "body": {
                    "pid": flow.request.query.get('pid'),
                    "result": "EXTERNAL_ENTER",
                    "url": "/bh-confirmation/v3/workflow2"
                },
                "success": True
            })
        if 'online.sberbank.ru:8543/transfer/partner-bank-phone/send/v1/workflow?cmd=EXIT' in url:
            pid = flow.request.query.get('pid')
            flow.response = format_response({
                "body": {
                    "pid": pid,
                    "result": "END"
                },
                "success": True
            })
        if 'online.sberbank.ru:8543/sbptransfer/v1/workflow?cmd=EXIT' in url:
            pid = flow.request.query.get('pid')
            flow.response = format_response({"success": True, "body": {"result": "EXTERNAL_RETURN",
                                                                       "pid": pid,
                                                                       "url": "/transfer/partner-bank-phone/send/v1/workflow"}})
        if 'online.sberbank.ru:8543/bh-confirmation/v3/workflow2?cmd=EVENT' in url:
            pid = flow.request.query.get('pid')
            flow.response = format_response({"success": True, "body": {"result": "EXTERNAL_RETURN",
                                                                       "pid": pid,
                                                                       "url": "/transfer/partner-bank-phone/send/v1/workflow"}})
        if 'online.sberbank.ru:8543/cltransfer/v1/receipt/' in url:
            flow.response = http.Response.make(200, self.api.get_check({
                'RECEIVER_NAME': self.name,
                'AMOUNT': self.amount,
                'RECEIVER_NUMBER': self.phone,
            }), {'content-type': 'application/pdf'})

        if 'online.sberbank.ru:8543/sbptransfer/v1/receipt/' in url and self.op:
            flow.response = http.Response.make(200, self.api.get_check({
                'RECEIVER_NAME': self.op['receiver_name'],
                'AMOUNT': self.op['amount'],
                'RECEIVER_NUMBER': self.op['receiver_number'],
            }), {'content-type': 'application/pdf'})

        if 'online.sberbank.ru:8543/transfer/partner-bank-phone/send/v1/receipt' in url:
            flow.response = http.Response.make(200, self.api.get_check({
                'RECEIVER_NAME': self.name,
                'AMOUNT': self.amount,
                'RECEIVER_NUMBER': self.phone,
            }), {'content-type': 'application/pdf'})

        if 'online.sberbank.ru:8543/p2ptransfer-xb-card/v1/getRecalculation' in url:
            req = json.loads(flow.request.content)
            self.amount = float(req['toAmount'])
            flow.response = format_response({
                "body": {
                    "commissionDescription": "Комиссия 30 ₽",
                    "currencyRateDescription": "",
                    "receiverCurrencyRateDescription": "",
                    "statusCode": "0",
                    "totalAmountDescription": f"Спишем {30 + self.amount} ₽"
                },
                "success": True
            })

        if 'online.sberbank.ru:8543/p2ptransfer-xb-card/v1/workflow?cmd=EVENT' in url:
            req = json.loads(flow.request.content)
            req['fields']['p2ptransfer:xbcard:amount'] = '10'
            flow.request = http.Request.make(flow.request.method, url, json.dumps(req), flow.request.headers)


# addons = [Sber('sber')]
