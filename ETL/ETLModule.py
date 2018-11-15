import pandas as pd
import os

from base import engine


class ETLModule(object):
    tableInformation = {
        'usr': {
            'tableName': 'users',
            'columns': ['id', 'created_date', 'has_email', 'phone_country', 'terms_version', 'country', 'state',
                            'birth_year', 'kyc', 'failed_sign_in_attempts'],
            'indexCol': 0
        },
        'trans': {
            'tableName': 'transactions',
            'columns': ['id', 'user_id', 'type', 'source', 'entry_method', 'merchant_country', 'merchant_category',
                            'created_date', 'state', 'amount', 'currency'],
            'indexCol': 0
        },
        'fx': {
            'tableName': 'fx_rates',
            'columns': ['id', 'ts', 'base_ccy', 'ccy', 'rate'],
            'indexCol': 0
        },
        'ccy': {
            'tableName': 'currency_details',
            'columns': ['ccy', 'iso_code', 'exponent', 'is_crypto'],
            'indexCol': False
        }
    }

    def __determineTableFromFilename(self,filename):
        filePathArr = filename.split('.')
        filePath = filePathArr[-2] if (filePathArr[-1].lower() == 'csv') else filePathArr[-1]
        file = filePath.split('/')[-1]

        if file == 'train_users':
            key = 'usr'
        elif file == 'train_transactions':
            key = 'trans'
        elif file == 'fx_rates':
            key = 'fx'
        elif file == 'currency_details':
            key = 'ccy'
        else:
            Exception('No csv file found')

        return self.tableInformation[key]

    def __executeTransformationFunction(self,df,tableInfo):
        if tableInfo['tableName'] == 'users':
            df_trans = self.__transformUser(df,tableInfo)
        elif tableInfo['tableName'] == 'transactions':
            df_trans = self.__transformTransaction(df,tableInfo)
        elif tableInfo['tableName'] == 'fx_rates':
            df_trans = self.__transformFxRates(df,tableInfo)
        elif tableInfo['tableName'] == 'currency_details':
            df_trans = self.__transformCurrencyDetails(df,tableInfo)
        else:
            print('key not found in table')
            df_trans = None

        return df_trans

    def __transformUser(self,df,tableInfo):
        try:
            df_fraud = pd.read_csv(os.path.join(os.getcwd(), 'data', 'train_fraudsters.csv'), index_col=0)
        except Exception as e:
            print(e)

        df.rename(str.lower, axis='columns', inplace=True)
        df_trans = df[tableInfo['columns']]
        isFraudster = df["id"].isin(df_fraud['user_id'])
        df_trans.insert(len(df_trans.columns), 'is_fraudster',isFraudster)
        return df_trans


    def __transformTransaction(self,df,tableInfo):
            df.rename(str.lower, axis='columns', inplace=True)
            df_trans = df[tableInfo['columns']]
            return df_trans


    def __transformFxRates(self,df,tableInfo):
        df_trans = pd.DataFrame(columns=tableInfo['columns'])

        for key, column in df.iteritems():
            base_ccy = key[:3]
            ccy = key[3:]
            df_temp = pd.DataFrame(columns=tableInfo['columns'])
            df_temp['id'] = ['{}-{}-{}'.format(i, base_ccy, ccy) for i in column.index]
            df_temp['ts'] = df.index.get_values()
            df_temp['base_ccy'] = base_ccy
            df_temp['ccy'] = ccy
            df_temp['rate'] = column.values
            df_trans = df_trans.append(df_temp, ignore_index=True, sort=False)

        return df_trans


    def __transformCurrencyDetails(self,df,tableInfo):
        df.columns = tableInfo['columns']
        return df


    def extract(self,filename,indexCol=0):
        try:
            df = pd.read_csv(os.path.join(os.getcwd(),'data',filename), index_col=indexCol)
        except Exception as e:
            print(e)
        return df


    def persist(self,df,tableName):
        try:
            df.to_sql(tableName, engine, if_exists='append', index=False)
        except Exception as e:
            print(e)


    def storeDataToTable(self,filename):
        tableInfo = self.__determineTableFromFilename(filename)
        df = self.extract(filename,tableInfo['indexCol'])
        df_trans = self.__executeTransformationFunction(df,tableInfo)
        self.persist(df_trans,tableInfo['tableName'])
