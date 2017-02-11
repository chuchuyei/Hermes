import os
import time
import pandas as pd


class PreprocessedData:
    def __init__(self, file_path, currency_source):
        self.file_path = file_path
        self.currency_source = os.path.join(self.file_path, currency_source)

    def current_transfer_file(self, kind_of_currency):
        current_cols = ['資料日期', '幣別',
                        '買入匯率', '買入-現金', '買入-即期', '買入-遠期10天', '買入-遠期30天', '買入-遠期60天',
                        '買入-遠期90天', '買入-遠期120天', '買入-遠期150天', '買入-遠期180天',
                        '賣出匯率', '賣出-現金', '賣出-即期', '賣出-遠期10天', '賣出-遠期30天', '賣出-遠期60天',
                        '賣出-遠期90天', '賣出-遠期120天', '賣出-遠期150天', '賣入-遠期180天']
        # open original data
        try:
            origin_data = pd.read_excel(self.currency_source)  # data/current_data.xlsx
            origin_data.columns = current_cols
        except Exception:
            origin_data = pd.DataFrame(columns=current_cols)

        while True:
            try:
                filename = \
                    [f for f in os.listdir(self.file_path) if
                     'ExchangeRate@' in f and os.path.splitext(f)[-1] == '.csv'][0]
                break
            except Exception:
                time.sleep(0.1)
        df = pd.read_csv(os.path.join(self.file_path, filename))
        df.reset_index(level=0, inplace=True)
        df.dropna(axis=1, inplace=True)
        df.columns = current_cols
        df['資料日期'] = pd.to_datetime(df['資料日期'], format='%Y%m%d')
        origin_data = pd.concat([origin_data, df])
        origin_data.index = range(len(origin_data))
        origin_data.drop_duplicates(inplace=True)
        origin_data.to_excel(self.currency_source, index=False)
        os.remove(os.path.join(self.file_path, filename))
