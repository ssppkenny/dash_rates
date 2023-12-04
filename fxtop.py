import asyncio
import time
import pandas as pd
import aiohttp
from aiohttp import ClientSession
from html_table_parser import HTMLTableParser
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

async def run_request(dt, cur_from = 'CHF', cur_to = 'RUB'):
    year_to = f"{dt.year:04}"
    month_to = f"{dt.month:02}"
    day_to = f"{dt.day:02}"
    from_dt = dt - relativedelta(years=1)
    year_from = f"{from_dt.year:04}"
    month_from = f"{from_dt.month:02}"
    day_from = f"{from_dt.day:02}"

    async with aiohttp.ClientSession() as session:
        url = f"https://fxtop.com/en/historical-exchange-rates.php?A=1&C1={cur_from}&C2={cur_to}&TR=1&DD1={day_from}&MM1={month_from}&YYYY1={year_from}&B=1&P=&I=1&DD2={day_to}&MM2={month_to}&YYYY2={year_to}&btnOK=Go%21"
        response = await session.get(url)
        text = await response.text()
        p = HTMLTableParser()
        ##print(text)
        p.feed(text)
        df = pd.DataFrame.from_records(p.tables[26][6:])
        df[0] = pd.to_datetime(df[0])
        df[1] = pd.to_numeric(df[1])
        df.rename(columns={0:"Date", 1:"Rate", 2:"Min", 3:"Average",4:"Max",5:"First",6:"Last"}, inplace=True)
        return df


async def get_rates(years, cur_from='CHF', cur_to='RUB'):
    dt = datetime.now()
    from_dts = [dt - relativedelta(years=y) for y in range(years)]
    tasks = [asyncio.create_task(run_request(dt, cur_from, cur_to)) for dt in from_dts]
    return [await task for task in tasks]


if __name__ == '__main__':
    st = time.time()
    dfs = asyncio.run(get_rates(2))
    print(time.time() - st)
    df = pd.concat(dfs)
    plt.plot(df["Date"], df["Rate"])
    plt.show()
