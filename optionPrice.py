from math import ceil
from datetime import datetime
import robin_stocks.robinhood as rs
import yfinance as yf
import pytz
import boto3

dynamodb  =  boto3.client(
    service_name = 'dynamodb',
    region_name = 'us-east-1',
    aws_access_key_id = 'AKIAXK4PJGUM3GB54YID',
    aws_secret_access_key = '')

class optionPrice:
    def __init__(self, symbol = "spy"):
        self.login()
        self.symbol = symbol
        self.exps = self.getExpirationDate()
        self.ESTTime = self.ESTTime()
        self.price = self.getCurrentPrice()
        self.strike = int(self.price)

    def login(self):
        robin_user = ""
        robin_pass = ""
        res= rs.login(username=robin_user,
                password=robin_pass,
                expiresIn=31540000, # 365 days
                by_sms=True)
#         print(res)

    def ESTTime(self):
        newYorkTz = pytz.timezone("America/New_York") 
        timeInNewYork = datetime.now(newYorkTz)
        return timeInNewYork.strftime("%Y-%m-%d %H:%M:%S")
    
    def getCurrentPrice(self):
        price = rs.stocks.get_latest_price(self.symbol, includeExtendedHours=True)
        price = float(price[0])
        # print(self.symbol, price)
        return price
    
    def getExpirationDate(self):
        # return "2023-02-10"
        tk = yf.Ticker(self.symbol)
        exps = tk.options
#         print(exps)
        return exps       
        
    def getBestDebit(self, optionType, day):
        expirationDate = self.exps[day]
        # print(self.symbol, self.expirationDate,self.strike, optionType)
        best_bid = rs.options.find_options_by_expiration_and_strike(self.symbol,
                                                 expirationDate,
                                                 self.strike,
                                                 optionType= optionType,
                                                 info='bid_price')
        best_ask = rs.options.find_options_by_expiration_and_strike(self.symbol,
                                                 expirationDate,
                                                 self.strike,
                                                 optionType= optionType,
                                                 info='ask_price')
        best_bid, best_ask = float(best_bid[0]), float(best_ask[0])
        best_debit = float((best_bid + best_ask)/2)
        best_debit = ceil(best_debit * 100) / 100.0
        print(self.symbol, expirationDate, optionType, best_debit, "(",best_bid,best_ask,")")

        option = self.symbol.upper() + expirationDate.replace("-", "") + optionType[:1].upper() + str(self.strike) # SPY20230215C411
        dic_option = {"date": self.ESTTime, "option" : option, "premium": best_debit, "price" : str(self.price)} # 2023-02-15 08:57:23 0 SPY20230215C411 2.58 411.34
        print(dic_option)

        dic_option = {"id": self.ESTTime + " " + str(day) + " " + option + " " + str(best_debit) + " " + str(self.price),
                    "symbol": self.symbol,  
                    "expirationDate": expirationDate, 
                    "optionType": optionType, 
                    "premium": str(best_debit), 
                    "date": self.ESTTime, 
        }
        return dic_option
    
    def get(self, key = "record"):
        call = self.getBestDebit("call", 1)
        put = self.getBestDebit("put", 1)
        list= [call, put]
        if key == "record":
            for l in list:
                self.record(l)
        return list
        
    def record(self, dic_option):
        print("--------------record------------------")

        newItem = { 'id': {}, 
            'symbol': {},
            'expirationDate': {},
            'optionType': {},
            'premium': {},
            'date': {},
        }
        newItem['id']['S'] = dic_option["id"]
        newItem['symbol']['S'] = dic_option["symbol"]
        newItem['expirationDate']['S'] = dic_option["expirationDate"]
        newItem['optionType']['S'] = dic_option["optionType"]
        newItem['premium']['S'] = dic_option["premium"]
        newItem['date']['S'] = dic_option["date"]
        dynamodb.put_item(TableName="option-price", Item=newItem)

if __name__ == '__main__':
    optionPrice().record()