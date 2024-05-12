import ccxt as ct
from ccxt.base.errors import BadSymbol
import pandas as pd
import ta

from keys import okexkey,okexsecret,phrase

class CrossOverBot:
    def __init__(self,api_key,secret_key,phrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.phrase = phrase
        self.okex = ct.okx({
                 'apikey': f'{self.api_key}',
                 'secret' :f'{self.secret_key}',
                 'password':f'{self.phrase}'
                 }
            )
    def data(self,market,tf,limit=1000):
        try:
            df = self.okex.fetch_ohlcv(symbol=market,timeframe=tf,limit=limit)
            if df:
                df = pd.DataFrame(df)
                df.columns = ['time','high','low','close','volume']
                df['time'] = pd.to_datetime(df['time'], unit='ms')
                df['EMA_20'] =                           ta.EMA(df['close'], timeperiod=20)
                df['EMA_10'] =                           ta.EMA(df['close'], timeperiod=10)

                df["h_t"] = df['high'].rolling(window=7).max()
                df['crossover'] = (df['EMA_10'] > df['EMA_20']) & (df['EMA_10'].shift(1) <= df['EMA_20'].shift(1))
                df['crossover'] = (df['EMA_10'] <  df['EMA_20']) & (df['EMA_10'].shift(1) >= df['EMA_20'].shift(1))
        except BadSymbol:
            print("plaese check your market")
    def cross_over(self,market,tf):
        df = self.data(market,tf,1000)
        if any(df['crossover']):
            crossover_index = df['crossover'].idxmax()
            if any(df["crossover"].loc[crossover_index:]):
                 print(f"the direction is over ................{market},{tf}")
            else:
                print("the {market }has positive direction")
if __name__  == "__main__":
    CrossOverBot(okexkye , okexsecret , phrase).cross_over("BTC/USDT","1h")