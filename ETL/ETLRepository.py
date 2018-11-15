from sqlalchemy import text
from base import Session, engine
import pandas as pd


conn = engine.connect()

class ETLRepository(object):

    def fetchUsers(self):
        df = pd.read_sql_table('users',conn)
        return df

    def fetchSingleUser(self,uuid):
        sql = text("select * from users where id = :uuid")
        df = pd.read_sql_query(sql, conn, params={'uuid': uuid})
        return df

    def fetchUsersFromCountry(self,country):
        sql = text("select * from users where country = :country")
        df = pd.read_sql_query(sql, conn, params={'country':country})
        return df

    def fetchFraudstersFromCountry(self,country):
        sql = text("select * from users where country = :country and is_fraudster=TRUE")
        df = pd.read_sql_query(sql,conn,params={'country':country})
        return df

    def fetchTransactions(self):
        df = pd.read_sql_table('transactions',conn)
        return df

    def fetchFxRates(self):
        df = pd.read_sql_table('fx_rates',conn)
        return df

    def fetchCurrencyDetails(self):
        df = pd.read_sql_table('currency_details',conn)
        return df

    def fetchRelevantTransactions(self):
        sql = text("select * from "
                   "(select user_id, min(created_date) as first_created from transactions group by user_id) as first_transaction "
                   "inner join transactions on transactions.user_id = first_transaction.user_id "
                   "and transactions.created_date = first_transaction.first_created "
                   "where transactions.type = 'CARD_PAYMENT' and transactions.state = 'COMPLETED'")
        df = pd.read_sql_query(sql,conn)
        return df

    def fetchDistinctUserCountries(self):
        sql = text("select distinct country from users")
        df = pd.read_sql_query(sql,conn)
        return df

    def findTransactionsAboveTenUSD(self):
        transactions = self.fetchRelevantTransactions()
        ccyDetails = self.fetchCurrencyDetails()
        fxRates = self.fetchFxRates()
        result = []

        for index, row in transactions.iterrows():
            ccyExp = ccyDetails.loc[ccyDetails['ccy'] == row['currency']]['exponent'].values[0]

            if row['currency'] != 'USD':
                df = fxRates.loc[(fxRates['ccy'] == row['currency']) & (fxRates['base_ccy'] == 'USD')]
                df.set_index('ts', inplace=True)
                idx = df.index.get_loc(row['created_date'], method='nearest')
                fxConvRate = df.iloc[idx]['rate']
                amount = row['amount']*fxConvRate/(10**ccyExp)
            else:
                amount = row['amount']/(10**ccyExp)

            if amount > 10:
                result.append((row['user_id'].values[0], amount))

        return result
