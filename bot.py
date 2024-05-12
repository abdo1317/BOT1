import ccxt
import talib
import pandas as pd
import numpy
import pytz
class BBbot:
    def __init__(self):
        self.binance=ccxt.binance()
        self.timeframe=["1m","5m","15m","30m","1h","4h"]

    def tickers(self):
        tickers =self.binance.load_markets()
        usdt_markets = [symbol for symbol in tickers if symbol.endswith('/USDT')]
        return usdt_markets
    
    def ohlc(self,market,tf,limit=None):
        can=self.binance.fetch_ohlcv(market,tf)
        df = pd.DataFrame(can, columns=['time', 'open', 'high','low', 'close', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['time'] = df['time'].dt.tz_localize(pytz.timezone('UTC'))
        df['time'] = df['time'].dt.tz_convert(pytz.timezone('Etc/GMT-3'))
        df['upper'], df['middle'], df['lower'] = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        return df
    def obv_str(self,market,tf):
        df=self.ohlc(market,tf,100)
        df['condition'] = numpy.where((df['low'] <= df['lower']) &(df['close'] > df['lower']) & (df['close'] > df['open']), True, False)
        signal_detected = []
        for index,row in df.iterrows():
            if index >= len(df) - 1:
                continue
            if row['obv'] < df.loc[index+1, 'obv'] :
                if df.loc[index, 'condition']:
                    signal_detected.append(row)
        if signal_detected:
            for row in signal_detected:
                print(row)
        else:
            print("no signal detected")
    def obv(self,market,tf):
        df=self.ohlc(market,tf,100)
        df['condition'] = numpy.where((df['low'] <= df['lower']) & (df['close'] > df['lower']) & (df['close'] > df['open'] ), True, False)
        if df['condition'].iloc[-2] == True and df['obv'].iloc[-1]>df['obv'].iloc[-2]:
            print(market,"=======================",tf,"signal detect")
    def search(self):
        lista=self.tickers()
        for ticker in lista:
            for tf in self.timeframe:
                self.obv(ticker,tf)

if __name__=="__main__":
    BBbot().search()

