from math import ceil
from datetime import datetime
import pandas as pd
import robin_stocks.robinhood as rs
import yfinance as yf
import pytz

class optionPrice:
    def __init__(self, symbol = "spy"):
        self.login()
        self.symbol = symbol
        self.exps = self.getExpirationDate()
        self.strike = self.getCurrentPrice()
        self.ESTTime = self.ESTTime()

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
        price = int(float(price[0]))
        # print(self.symbol, price)
        return price
    
    def getExpirationDate(self):
        # return "2023-02-10"
        tk = yf.Ticker(self.symbol)
        exps = tk.options
#         print(exps)
        return exps       
        
    def getBestDebit(self, optionType, expirationDate):
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
        dic_debit = {"symbol": self.symbol,
                     "date": self.ESTTime.split()[0], 
                     "time": self.ESTTime.split()[1], 
                     "strike": self.strike, 
                     "expirationDate": expirationDate, 
                     "optionType": optionType, 
                     "premium": best_debit, "bid": best_bid, "ask": best_ask} 
        print(dic_debit)
        return dic_debit
    
    def get(self):
        call0 = self.getBestDebit("call", self.exps[0])
        put0 = self.getBestDebit("put", self.exps[0])

        call1 = self.getBestDebit("call", self.exps[1])
        put1 = self.getBestDebit("put", self.exps[1])
        dic =  {"call0": call0, "put0": put0, "call1": call1, "put1": put1}
        return dic
        
    def createDf(self):
        dic = self.get()
        df1 = pd.DataFrame({k: [v] for k, v in dic["call0"].items()})
        df2 = pd.DataFrame({k: [v] for k, v in dic["put0"].items()})
        df3 = pd.DataFrame({k: [v] for k, v in dic["call1"].items()})
        df4 = pd.DataFrame({k: [v] for k, v in dic["put1"].items()})

        df = pd.concat([df1, df2, df3, df4])
        return df



if __name__ == '__main__':
    optionPrice().record()