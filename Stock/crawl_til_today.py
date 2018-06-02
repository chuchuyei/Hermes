import pandas as pd
from datetime import datetime, date
from Stock.finlab.crawler import (
    update_table,
    crawl_price,
    crawl_monthly_report,
    crawl_finance_statement_by_date,

    date_range, month_range, season_range
)
from Stock.finlab.data import Connect

connect = Connect()

end_date = date.today()

# crawler 每日股價
sql = "SELECT DATE(MAX(DATE)) FROM price"
start_date = datetime.strptime(pd.read_sql(sql, connect.conn).iloc[0, 0], '%Y-%m-%d').date()
update_table(connect.conn, 'price', crawl_price, date_range(start_date, end_date))

# crawler 每月營收
sql = "SELECT DATE(MAX(DATE)) FROM monthly_revenue"
start_date = datetime.strptime(pd.read_sql(sql, connect.conn).iloc[0, 0], '%Y-%m-%d').date()
update_table(connect.conn, 'monthly_revenue', crawl_monthly_report, month_range(start_date, end_date))

# crawler 每季財報
sql = """
SELECT MIN(DATE) FROM (
    SELECT MAX(DATE) AS DATE FROM balance_sheet
    UNION ALL 
    SELECT MAX(DATE) AS DATE FROM cash_flows
    UNION ALL
    SELECT MAX(DATE) AS DATE FROM income_sheet
    UNION ALL
    SELECT MAX(DATE) AS DATE FROM income_sheet_cumulate
)
"""
start_date = datetime.strptime(pd.read_sql(sql, connect.conn).iloc[0, 0], '%Y-%m-%d').date()
update_table(connect.conn, 'finance_statement', crawl_finance_statement_by_date, season_range(start_date, end_date))
