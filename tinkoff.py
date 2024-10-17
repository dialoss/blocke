import json
import time
from datetime import datetime
from mitmproxy import http
from tools import format_response
from base import Base


def transform(op):
    op['timestamp'] = int(datetime.strptime(op['timestamp'], "%a, %d %b %Y %H:%M:%S GMT").timestamp() * 1000)
    base_structure = {
        "loyaltyBonusSummary": {"amount": 0.0},
        "isOffline": False, "isInner": False, "isAuto": False, "isDispute": False,
        "analyticsStatus": "NotSpecified", "hasStatement": False, "isSuspicious": False,
        "status": "OK", "operationTransferred": False, "idSourceType": "Prime",
        "loyaltyBonus": [], "isTemplatable": False, "mcc": 0,
        "category": {"id": "45", "name": "Другое"},
        "ucid": "1181910199", "mccString": "0000", "locations": [],
        "cashback": 0.0, "offers": [], "isHce": False, "additionalInfo": [],
        "virtualPaymentType": 0, "account": "5696387777", "loyaltyPayment": [],
        "trancheCreationAllowed": False, "cardPresent": True, "isExternalCard": False,
        "cardNumber": "553691******7297",
        "cashbackAmount": {
            "currency": {"code": 643, "name": "RUB", "strCode": "643"},
            "value": 0.0000
        }
    }

    common_structure = {
        **base_structure,
        "description": op['description'],
        "debitingTime": {"milliseconds": op['timestamp']},
        "subcategory": op['description'],
        "operationTime": {"milliseconds": op['timestamp']},
        "spendingCategory": {
            "name": "Переводы", "icon": "transfers-c1",
            "id": "24", "baseColor": "4FC5DF"
        },
        "amount": {
            "currency": {"code": 643, "name": "RUB", "strCode": "643"},
            "value": op['amount']
        },
        "accountAmount": {
            "currency": {"code": 643, "name": "RUB", "strCode": "643"},
            "value": op['amount']
        }
    }

    if op['type'] == 'income':
        return {
            **common_structure,
            "icon": "https://brands-prod.cdn-tinkoff.ru/general_logo/atm-transfer-1.png",
            "type": "Credit",
            "subgroup": {"id": "C4", "name": "Пополнения"},
            "typeSerno": 500, "hasStatement": True,
            "authorizationId": "190055930121", "id": "92560131360",
            "group": "INCOME", "senderDetails": op['description'],
            "brand": {
                "name": "Входящий перевод", "baseTextColor": "333333",
                "fileLink": "https://brands-prod.cdn-tinkoff.ru/general_logo/atm-transfer-1.png",
                "baseColor": "ffdd2d", "logoFile": "atm-transfer-1.png",
                "logo": "https://static.tinkoff.ru/providers/logotypes/brands/atm-transfer-1.png",
                "id": "tcs", "roundedLogo": False
            },
            "operationId": {"value": "190055930121", "source": "PrimeAuth"},
            "posId": "979",
            "merchant": {"name": "Входящий перевод"},
            "card": "179761560", "senderAgreement": "8140636389",
        }
    else:
        return {
            **common_structure,
            "icon": "https://brands-prod.cdn-tinkoff.ru/general_logo/bankspb.png",
            "type": "Debit",
            "subgroup": {"id": "F1", "name": "Переводы"},
            "typeSerno": 727, "authorizationId": "190056134199",
            "payment": {
                "paymentId": "18702009596", "providerGroupId": "Переводы",
                "paymentType": "Transfer", "providerId": "p2p-anybank",
                "hasPaymentOrder": False, "comment": "", "repeatable": True,
                "cardNumber": "553691******7297", "sourceIsQr": False,
                "bankAccountId": "5696387777", "isQrPayment": False,
                "feeAmount": {
                    "currency": {"code": 643, "name": "RUB", "strCode": "643"},
                    "value": 0.0000
                },
                "fieldsValues": {
                    "pointerType": "Телефон", "workflowType": "SBPTransfer",
                    "pointerLinkId": "24277155411", "bankMemberId": "100000000029",
                    "receiverBankName": "Банк Санкт-Петербург",
                    "maskedFIO": "Алексей Ф.", "pointer": "+79124531782"
                }
            },
            "id": "92565939234", "operationPaymentType": "NORMAL",
            "isTemplatable": True, "mcc": 1, "group": "INCOME", "mccString": "0001",
            "brand": {
                "name": "Банк Санкт-Петербург", "baseTextColor": "ffffff",
                "fileLink": "https://brands-prod.cdn-tinkoff.ru/general_logo/bankspb.png",
                "link": "", "baseColor": "c4112f", "logoFile": "bankspb.png",
                "logo": "https://brands-prod.cdn-tinkoff.ru/general_logo/bankspb.png",
                "id": "11336", "roundedLogo": False
            },
            "operationId": {"value": "190056134199", "source": "PrimeAuth"},
            "posId": "627",
            "merchant": {"name": "Банк Санкт-Петербург"}
        }


class Tinkoff(Base):

    def get_accounts(self):
        balance = self.api.get_card_balance(1)
        return {
            "resultCode": "OK",
            "payload": {
                "accounts": {
                    "payload": [
                        {
                            "id": "5696387777",
                            "name": "Black",
                            "accountType": "Current",
                            "currency": {
                                "code": 643,
                                "name": "RUB",
                                "strCode": "643"
                            },
                            "moneyAmount": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": balance
                            },
                            "totalIncome": {
                                "currency": {
                                    "code": 999,
                                    "name": "XXX",
                                    "strCode": "999"
                                },
                                "value": 0.0000
                            },
                            "totalExpense": {
                                "currency": {
                                    "code": 999,
                                    "name": "XXX",
                                    "strCode": "999"
                                },
                                "value": 0.0000
                            },
                            "accountIconType": "MC_ACCOUNT_RUB",
                            "partNumber": "TFPLCU3.12",
                            "creationDate": {
                                "milliseconds": 1650931200000
                            },
                            "marketingName": "Расчетная карта. ТПС 3.12 RUB",
                            "sumPurchases": 31937.19,
                            "rate": 0.0,
                            "hidden": False,
                            "loyalty": [
                                {
                                    "programId": "Cashback",
                                    "amount": 3544.0,
                                    "bonusLimitReached": False,
                                    "amountPartial": 3544.0,
                                    "creditLimit": 0.0,
                                    "usedCreditLimit": 0.0,
                                    "currentAmount": 0.0,
                                    "pendingBalance": 0.0,
                                    "currentAmountPartial": 0.0,
                                    "pendingBalancePartial": 0.0,
                                    "yearRedeemSum": 0.0,
                                    "loyalty": "Tinkoff Black",
                                    "name": "Tinkoff Black",
                                    "loyaltySteps": 1,
                                    "loyaltyPointsId": 3,
                                    "loyaltyPointsName": "Rubles",
                                    "loyaltyImagine": True,
                                    "partialCompensation": False,
                                    "primeLoyaltyId": "33",
                                    "primeLoyaltyGroupId": 0,
                                    "bonusLimit": 5000.0
                                }
                            ],
                            "externalAccountNumber": "40817810500060787149",
                            "tariffFileHash": "656fa3e6-5e60-4531-85d1-9cd448385b1d",
                            "tariffInfo": {
                                "interestRate": 0.0,
                                "lowRate": 0.0,
                                "highRateAmount": {
                                    "currency": {
                                        "code": 643,
                                        "name": "RUB",
                                        "strCode": "643"
                                    },
                                    "value": 300000.0000
                                },
                                "purchaseSumForInterest": {
                                    "currency": {
                                        "code": 643,
                                        "name": "RUB",
                                        "strCode": "643"
                                    },
                                    "value": 3000.0000
                                },
                                "purchaseSumForHighInterest": {
                                    "currency": {
                                        "code": 643,
                                        "name": "RUB",
                                        "strCode": "643"
                                    },
                                    "value": 3000.0000
                                }
                            },
                            "clientUnverifiedFlag": "ClientVerified",
                            "accountBalance": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 1299.4500
                            },
                            "creditLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 0.0000
                            },
                            "lastStatementDate": {
                                "milliseconds": 1727222400000
                            },
                            "dueDate": {
                                "milliseconds": 1729209600000
                            },
                            "currentMinimalPayment": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 0.0000
                            },
                            "pastDueDebt": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 0.0000
                            },
                            "overdraftFee": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 0.0000
                            },
                            "cardNumbers": [
                                {
                                    "id": "179761560",
                                    "name": "Дебетовая карта",
                                    "value": self.api.get_card(1)['card_number'],
                                    "primary": True,
                                    "canBeRemoved": False,
                                    "hasWrongPins": False,
                                    "frozenCard": False,
                                    "statusCode": "NORM",
                                    "status": "Активна",
                                    "availableBalance": {
                                        "currency": {
                                            "code": 643,
                                            "name": "RUB",
                                            "strCode": "643"
                                        },
                                        "value": self.api.get_card_balance(1)
                                    },
                                    "activated": True,
                                    "reissued": False,
                                    "pinSet": True,
                                    "expiration": {
                                        "milliseconds": 1914354000000
                                    },
                                    "expirationStatus": "normal",
                                    "position": 1,
                                    "hce": False,
                                    "paymentSystem": "MC",
                                    "cardDesign": "dcb82623ba80ba50235ecc7ca2ae1ca2",
                                    "creationDate": {
                                        "milliseconds": 1661461200000
                                    },
                                    "ucid": "1181910199",
                                    "multiCardCluster": {
                                        "id": "24065855"
                                    },
                                    "isEmbossed": True,
                                    "isVirtual": False,
                                    "isPaymentDevice": False
                                },
                            ],
                            "status": "NORM",
                            "lastStatementDebtAmount": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 0.0000
                            },
                            "renewalAmountLeft": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 150000.0000
                            },
                            "defaultRenewalAmountLeft": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 150000.0000
                            },
                            "monthlyCashLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 100000.0000
                            },
                            "defaultMonthlyCashLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 100000.0000
                            },
                            "defaultMonthlyTinkoffCashLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 500000.0000
                            },
                            "monthlyTinkoffCashLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 500000.0000
                            },
                            "defaultMonthlyTinkoffCashInsertionLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 10000000.0000
                            },
                            "monthlyTinkoffCashInsertionLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 10000000.0000
                            },
                            "accountGroup": "Дебетовые карты",
                            "authorizationsAmount": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 0.0000
                            },
                            "c2cOutLimitBorder": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 50000.0000
                            },
                            "c2cOutLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 50000.0000
                            },
                            "debtBalance": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 0.0000
                            },
                            "feeAndFinesBalance": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 0.0000
                            },
                            "imported": False,
                            "multiCardCluster": {
                                "id": "24065855"
                            },
                            "feeNextChargeText": "не взимается",
                            "emoneyFlag": False,
                            "nextStatementDate": {
                                "milliseconds": 1729717200000
                            },
                            "afterNextStatementDate": {
                                "milliseconds": 1732395600000
                            },
                            "lastPaymentDate": {
                                "milliseconds": 1728901100320
                            }
                        },
                        {
                            "id": "5366395807",
                            "name": "Black USD",
                            "accountType": "Current",
                            "currency": {
                                "code": 840,
                                "name": "USD",
                                "strCode": "840"
                            },
                            "moneyAmount": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "totalIncome": {
                                "currency": {
                                    "code": 999,
                                    "name": "XXX",
                                    "strCode": "999"
                                },
                                "value": 0.0000
                            },
                            "totalExpense": {
                                "currency": {
                                    "code": 999,
                                    "name": "XXX",
                                    "strCode": "999"
                                },
                                "value": 0.0000
                            },
                            "accountIconType": "MC_ACCOUNT_USD",
                            "partNumber": "TFPLCU3.0U",
                            "creationDate": {
                                "milliseconds": 1703980800000
                            },
                            "marketingName": "Расчетная карта. ТПС 3.0 USD",
                            "sumPurchases": 0.0,
                            "rate": 0.0,
                            "hidden": True,
                            "loyalty": [
                                {
                                    "programId": "Cashback",
                                    "amount": 0.0,
                                    "bonusLimitReached": False,
                                    "amountPartial": 0.0,
                                    "creditLimit": 0.0,
                                    "usedCreditLimit": 0.0,
                                    "currentAmount": 0.0,
                                    "pendingBalance": 0.0,
                                    "currentAmountPartial": 0.0,
                                    "pendingBalancePartial": 0.0,
                                    "yearRedeemSum": 0.0,
                                    "loyalty": "Tinkoff Black USD",
                                    "name": "Tinkoff Black",
                                    "loyaltySteps": 1,
                                    "loyaltyPointsId": 10,
                                    "loyaltyPointsName": "Иностранная валюта",
                                    "loyaltyImagine": True,
                                    "partialCompensation": False,
                                    "primeLoyaltyId": "104",
                                    "primeLoyaltyGroupId": 0,
                                    "bonusLimit": 100.0
                                }
                            ],
                            "externalAccountNumber": "40817840900007211251",
                            "tariffFileHash": "b0d1fc54-03dd-4561-967a-5baaba067fae",
                            "tariffInfo": {
                                "interestRate": 0.0,
                                "lowRate": 0.0,
                                "highRateAmount": {
                                    "currency": {
                                        "code": 840,
                                        "name": "USD",
                                        "strCode": "840"
                                    },
                                    "value": 0.0000
                                },
                                "purchaseSumForInterest": {
                                    "currency": {
                                        "code": 840,
                                        "name": "USD",
                                        "strCode": "840"
                                    },
                                    "value": 0.0000
                                },
                                "purchaseSumForHighInterest": {
                                    "currency": {
                                        "code": 840,
                                        "name": "USD",
                                        "strCode": "840"
                                    },
                                    "value": 0.0000
                                }
                            },
                            "clientUnverifiedFlag": "ClientVerified",
                            "accountBalance": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "creditLimit": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "lastStatementDate": {
                                "milliseconds": 1727222400000
                            },
                            "dueDate": {
                                "milliseconds": 1729209600000
                            },
                            "currentMinimalPayment": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "pastDueDebt": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "overdraftFee": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "cardNumbers": [],
                            "status": "NORM",
                            "lastStatementDebtAmount": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "renewalAmountLeft": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 10000.0000
                            },
                            "defaultRenewalAmountLeft": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 10000.0000
                            },
                            "monthlyCashLimit": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 5000.0000
                            },
                            "defaultMonthlyCashLimit": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 5000.0000
                            },
                            "defaultMonthlyTinkoffCashLimit": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 5000.0000
                            },
                            "monthlyTinkoffCashLimit": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 5000.0000
                            },
                            "defaultMonthlyTinkoffCashInsertionLimit": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 10000000.0000
                            },
                            "monthlyTinkoffCashInsertionLimit": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 10000000.0000
                            },
                            "accountGroup": "Дебетовые карты",
                            "authorizationsAmount": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "c2cOutLimitBorder": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 50000.0000
                            },
                            "c2cOutLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 50000.0000
                            },
                            "debtBalance": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "feeAndFinesBalance": {
                                "currency": {
                                    "code": 840,
                                    "name": "USD",
                                    "strCode": "840"
                                },
                                "value": 0.0000
                            },
                            "imported": False,
                            "multiCardCluster": {
                                "id": "24065855"
                            },
                            "feeNextChargeText": "не взимается",
                            "emoneyFlag": False,
                            "identificationState": "0",
                            "nextStatementDate": {
                                "milliseconds": 1729717200000
                            },
                            "afterNextStatementDate": {
                                "milliseconds": 1732395600000
                            },
                            "lastPaymentDate": {
                                "milliseconds": 1728901100319
                            }
                        },
                        {
                            "id": "5474303479",
                            "name": "Black CNY",
                            "accountType": "Current",
                            "currency": {
                                "code": 156,
                                "name": "CNY",
                                "strCode": "156"
                            },
                            "moneyAmount": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 12321.0
                            },
                            "totalIncome": {
                                "currency": {
                                    "code": 999,
                                    "name": "XXX",
                                    "strCode": "999"
                                },
                                "value": 0.0000
                            },
                            "totalExpense": {
                                "currency": {
                                    "code": 999,
                                    "name": "XXX",
                                    "strCode": "999"
                                },
                                "value": 0.0000
                            },
                            "accountIconType": "MC_ACCOUNT_XXX",
                            "partNumber": "TFPLCU3.0CNY",
                            "creationDate": {
                                "milliseconds": 1716422400000
                            },
                            "marketingName": "Расчетная карта. ТПС 3.0 CNY",
                            "sumPurchases": 0.0,
                            "rate": 0.0,
                            "hidden": False,
                            "loyalty": [
                                {
                                    "programId": "Cashback",
                                    "amount": 0.0,
                                    "bonusLimitReached": False,
                                    "amountPartial": 0.0,
                                    "creditLimit": 0.0,
                                    "usedCreditLimit": 0.0,
                                    "currentAmount": 0.0,
                                    "pendingBalance": 0.0,
                                    "currentAmountPartial": 0.0,
                                    "pendingBalancePartial": 0.0,
                                    "yearRedeemSum": 0.0,
                                    "loyalty": "Tinkoff Black CNY",
                                    "name": "Tinkoff Black",
                                    "loyaltySteps": 1,
                                    "loyaltyPointsId": 10,
                                    "loyaltyPointsName": "Иностранная валюта",
                                    "loyaltyImagine": True,
                                    "partialCompensation": False,
                                    "primeLoyaltyId": "84",
                                    "primeLoyaltyGroupId": 0,
                                    "bonusLimit": 300.0
                                }
                            ],
                            "externalAccountNumber": "40817156800000582535",
                            "tariffFileHash": "37dd4646-d770-4c24-9712-0b92baddc3f2",
                            "clientUnverifiedFlag": "ClientVerified",
                            "accountBalance": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "creditLimit": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "lastStatementDate": {
                                "milliseconds": 1727222400000
                            },
                            "dueDate": {
                                "milliseconds": 1729209600000
                            },
                            "currentMinimalPayment": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "pastDueDebt": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "overdraftFee": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "cardNumbers": [],
                            "status": "NORM",
                            "lastStatementDebtAmount": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "renewalAmountLeft": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "defaultRenewalAmountLeft": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "monthlyCashLimit": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 20000.0000
                            },
                            "defaultMonthlyCashLimit": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 20000.0000
                            },
                            "monthlyTinkoffCashLimit": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "defaultMonthlyTinkoffCashInsertionLimit": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 10000000.0000
                            },
                            "monthlyTinkoffCashInsertionLimit": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 10000000.0000
                            },
                            "accountGroup": "Дебетовые карты",
                            "authorizationsAmount": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "c2cOutLimitBorder": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 50000.0000
                            },
                            "c2cOutLimit": {
                                "currency": {
                                    "code": 643,
                                    "name": "RUB",
                                    "strCode": "643"
                                },
                                "value": 50000.0000
                            },
                            "debtBalance": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "feeAndFinesBalance": {
                                "currency": {
                                    "code": 156,
                                    "name": "CNY",
                                    "strCode": "156"
                                },
                                "value": 0.0000
                            },
                            "imported": False,
                            "multiCardCluster": {
                                "id": "24065855"
                            },
                            "feeNextChargeText": "не взимается",
                            "emoneyFlag": False,
                            "identificationState": "0",
                            "nextStatementDate": {
                                "milliseconds": 1729717200000
                            },
                            "afterNextStatementDate": {
                                "milliseconds": 1732395600000
                            },
                            "lastPaymentDate": {
                                "milliseconds": 1728901100320
                            }
                        },
                    ],
                    "details": {
                        "hasNext": False
                    },
                    "resultCode": "OK"
                },
                "list_owner_shared_resources": {
                    "payload": [],
                    "details": {
                        "hasNext": False
                    },
                    "resultCode": "OK"
                }
            },
            "trackingId": "5T5JCG6KR"
        }

    def response(self, flow: http.HTTPFlow):
        url = flow.request.pretty_url
        if url.startswith('https://api.tinkoff.ru/v1/grouped_requests'):
            form = dict(flow.request._get_urlencoded_form())
            l = json.loads(form.get('requestsData'))
            if isinstance(l, list):
                if l[0]['key'] == 'operations':
                    ops = list(map(transform, self.api.get_history()))
                    r = json.loads(flow.response.content)
                    r['payload']['operations']['payload'] += ops
                    flow.response = format_response(r)

    def request(self, flow: http.HTTPFlow):
        url = flow.request.pretty_url
        if url.startswith('https://api.tinkoff.ru/v1/grouped_requests'):
            form = dict(flow.request._get_urlencoded_form())
            l = json.loads(form.get('requestsData'))
            if isinstance(l, list):
                if len(l) == 2 and l[0]['key'] == 'accounts':
                    flow.response = format_response(self.get_accounts())

        if url.startswith('https://api.tinkoff.ru/v1/payment_commission'):
            form = dict(flow.request._get_urlencoded_form())
            pay = json.loads(form.get('payParameters'))
            self.amount = float(pay['moneyAmount'])
            self.phone = pay['providerFields']['pointer']
            self.name = pay['providerFields']['maskedFIO']
            flow.response = format_response({"resultCode": "OK", "payload": {
                "shortDescription": "Комиссия не взимается банком",
                "total": {"currency": {"code": 643, "name": "RUB", "strCode": "643"}, "value": self.amount},
                "providerId": "p2p-anybank", "minAmount": 10.0, "limit": 1000000.0,
                "value": {"currency": {"code": 643, "name": "RUB", "strCode": "643"}, "value": 0.0000},
                "maxAmount": 1000000.0, "unfinishedFlag": False, "externalFees": [],
                "description": "Комиссия не взимается банком"}, "trackingId": "LC8ZHDA95"})
        if url.startswith('https://api.tinkoff.ru/v1/pay?'):
            time.sleep(2)
            flow.response = format_response({"resultCode": "OK", "payload": {"paymentId": "18702009596",
                                                                             "commissionInfo": {
                                                                                 "amount": {"currency": {
                                                                                     "code": 643,
                                                                                     "name": "RUB",
                                                                                     "strCode": "643"},
                                                                                     "value": self.amount},
                                                                                 "commission": {
                                                                                     "currency": {
                                                                                         "code": 643,
                                                                                         "name": "RUB",
                                                                                         "strCode": "643"},
                                                                                     "value": 0.0000},
                                                                                 "amountWithCommission": {
                                                                                     "currency": {
                                                                                         "code": 643,
                                                                                         "name": "RUB",
                                                                                         "strCode": "643"},
                                                                                     "value": self.amount}},
                                                                             "extraFields": {}},
                                             "trackingId": "3UF8A5L6Y"})
            self.api.insert_operation({"type": "outcome",
                                       "title": "Перевод",
                                       "description": "Monthly salary",
                                       "amount": self.amount,
                                       "currency": "RUB",
                                       "card_number": "1234567890123456"})
        if url.startswith('https://api.tinkoff.ru/v1/payment_receipt_pdf'):
            flow.response = http.Response.make(200, self.api.get_check(
                {'RECEIVER_NUMBER': self.phone, 'RECEIVER_NAME': self.name, 'AMOUNT': self.amount,
                 'TIME': datetime.now().strftime('%d.%m.%Y %H:%M')}),
                                               {'content-type': 'application/pdf'})

        if url.startswith('https://api.tinkoff.ru/v1/operations_piechart'):
            settings = self.api.get_settings()
            transfer = settings['transfer']
            total_spend = settings['spending']
            flow.response = format_response({"resultCode": "OK", "payload": {
                "summary": {"currency": {"code": 643, "name": "RUB", "strCode": "643"}, "value": total_spend},
                "aggregated": [{"groupBy": "Образование",
                                "amount": {"currency": {"code": 643, "name": "RUB", "strCode": "643"},
                                           "value": 60200.0000}, "amountPercent": 54.0,
                                "spendingCategory": {"name": "Образование", "icon": "education-c1", "id": "21",
                                                     "baseColor": "FE9797"}}, {"groupBy": "Переводы", "amount": {
                    "currency": {"code": 643, "name": "RUB", "strCode": "643"}, "value": transfer},
                                                                               "amountPercent": 19.59,
                                                                               "spendingCategory": {"name": "Переводы",
                                                                                                    "icon": "transfers-c1",
                                                                                                    "id": "24",
                                                                                                    "baseColor": "4FC5DF"}},
                               {"groupBy": "Отели",
                                "amount": {"currency": {"code": 643, "name": "RUB", "strCode": "643"},
                                           "value": 14500.0000}, "amountPercent": 13.01,
                                "spendingCategory": {"name": "Отели", "icon": "hotels-c1", "id": "23",
                                                     "baseColor": "1FE5F1"}}, {"groupBy": "Транспорт", "amount": {
                        "currency": {"code": 643, "name": "RUB", "strCode": "643"}, "value": 4673.0100},
                                                                               "amountPercent": 4.19,
                                                                               "spendingCategory": {"name": "Транспорт",
                                                                                                    "icon": "transport-c",
                                                                                                    "id": "37",
                                                                                                    "baseColor": "6489F1"}},
                               {"groupBy": "Сервис",
                                "amount": {"currency": {"code": 643, "name": "RUB", "strCode": "643"},
                                           "value": 3602.0000}, "amountPercent": 3.23,
                                "spendingCategory": {"name": "Сервис", "icon": "services-c1", "id": "30",
                                                     "baseColor": "BAA2EC"}}, {"groupBy": "Супермаркеты", "amount": {
                        "currency": {"code": 643, "name": "RUB", "strCode": "643"}, "value": 2254.9200},
                                                                               "amountPercent": 2.02,
                                                                               "spendingCategory": {
                                                                                   "name": "Супермаркеты",
                                                                                   "icon": "supermarkets-c1",
                                                                                   "id": "33", "baseColor": "FE788B"}},
                               {"groupBy": "Спорттовары",
                                "amount": {"currency": {"code": 643, "name": "RUB", "strCode": "643"},
                                           "value": 1500.0000}, "amountPercent": 1.35,
                                "spendingCategory": {"name": "Спорттовары", "icon": "sports_goods-c1", "id": "31",
                                                     "baseColor": "1766FF"}}, {"groupBy": "Фастфуд", "amount": {
                        "currency": {"code": 643, "name": "RUB", "strCode": "643"}, "value": 1192.0000},
                                                                               "amountPercent": 1.07,
                                                                               "spendingCategory": {"name": "Фастфуд",
                                                                                                    "icon": "fastfood-c1",
                                                                                                    "id": "44",
                                                                                                    "baseColor": "FF9675"}},
                               {"groupBy": "Такси",
                                "amount": {"currency": {"code": 643, "name": "RUB", "strCode": "643"},
                                           "value": 1049.0000}, "amountPercent": 0.94,
                                "spendingCategory": {"name": "Такси", "icon": "taxi-c", "id": "47",
                                                     "baseColor": "FFC62B"}}, {"groupBy": "Мобильная связь", "amount": {
                        "currency": {"code": 643, "name": "RUB", "strCode": "643"}, "value": 520.0000},
                                                                               "amountPercent": 0.47,
                                                                               "spendingCategory": {
                                                                                   "name": "Мобильная связь",
                                                                                   "icon": "mobile-c1", "id": "17",
                                                                                   "baseColor": "6966F8"}},
                               {"groupBy": "Другое",
                                "amount": {"currency": {"code": 643, "name": "RUB", "strCode": "643"},
                                           "value": 149.0000}, "amountPercent": 0.13,
                                "spendingCategory": {"name": "Другое", "icon": "other-2", "id": "45",
                                                     "baseColor": "9ED3DE"}}]}, "trackingId": "5UALMRXEL"})


addons = [Tinkoff('tinkoff')]
