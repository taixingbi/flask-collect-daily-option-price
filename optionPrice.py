from math import ceil
from datetime import datetime
import robin_stocks.robinhood as rs
import yfinance as yf
import pytz
from dynamo import dynamo

class optionPrice:
    def __init__(self, symbol = "spy"):
        self.login()
        self.symbol = symbol
        self.exps = self.getExpirationDate()
        self.ESTTime = self.ESTTime()
        self.price = self.getCurrentPrice()

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
    
    def optionStart(self):
        print(self.ESTTime)
        time = self.ESTTime.split(" ")[1]
        return True if time[:2] == "15" else False # 15:30 
   
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
        
    def getOptionPremium(self, optionType, strike, expirationDate):
        print("--------", optionType, strike, expirationDate)
        best_bid = rs.options.find_options_by_expiration_and_strike(self.symbol,
                                                 expirationDate,
                                                 strike,
                                                 optionType= optionType,
                                                 info='bid_price')
        best_ask = rs.options.find_options_by_expiration_and_strike(self.symbol,
                                                 expirationDate,
                                                 strike,
                                                 optionType= optionType,
                                                 info='ask_price')
        best_bid, best_ask = float(best_bid[0]), float(best_ask[0])
        best_debit = float((best_bid + best_ask)/2)
        best_debit = ceil(best_debit * 100) / 100.0
        print(self.symbol, expirationDate, optionType, best_debit, "(",best_bid,best_ask,")")

        option = self.symbol.upper() + expirationDate.replace("-", "") + optionType[:1].upper() + str(strike) # SPY20230215C411

        dic_option = {"id": option,
                    "symbol": self.symbol,  
                    "expirationDate": expirationDate, 
                    "optionType": optionType, 
                    "premium": str(best_debit), 
                    "strike": strike,
                    "date": self.ESTTime, 
                    "price": str(self.price), 
                    "active": "True", 
                    "note": ""
        }
        print(dic_option)
        return dic_option

    def get(self, key = "record"):
        print("get")
        records =[]
        if self.optionStart():
        # if True:
            print("open an new option ....")
            call = self.getOptionPremium("call", str(int(self.price)), self.exps[1])
            put = self.getOptionPremium("put", str(int(self.price)), self.exps[1])
            records.append(call)
            records.append(put)

            if key == "record":
                for item in records: dynamo().put(item)
        else:
            itemsActive = dynamo().query(self.ESTTime.split(" ")[0])
            print("itemsActive", itemsActive)
            for item in itemsActive:
                optionPremium = self.getOptionPremium(item["optionType"], item["strike"], item["expirationDate"],)
                print("optionPremium", optionPremium)
                records.append(optionPremium)
            
            if key == "record":
                for item in records: dynamo().update(item)
        return records
        
if __name__ == '__main__':
    optionPrice().get("record")