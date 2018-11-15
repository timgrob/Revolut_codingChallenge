import base
import os
from ETL.ETLModule import ETLModule
from ETL.ETLRepository import ETLRepository
from detection_algorithm.FraudDetector import FraudDetector


if __name__ == "__main__":
    # 1. Generate database schemas
    base.generateDatabaseSchema()

    # 2. Populate database
    ROOT_DIR = os.getcwd()
    etl = ETLModule()
    etl.storeDataToTable(os.path.join(ROOT_DIR, 'data','train_users.csv'))
    etl.storeDataToTable(os.path.join(ROOT_DIR, 'data','train_transactions.csv'))
    etl.storeDataToTable(os.path.join(ROOT_DIR, 'data','fx_rates.csv'))
    etl.storeDataToTable(os.path.join(ROOT_DIR, 'data','currency_details.csv'))

    # 3. Find users whose first transaction was a successful card payment over 10 USD
    etlRepo = ETLRepository()
    userAbove10USD = etlRepo.findTransactionsAboveTenUSD()
    for u in userAbove10USD:
        print('User: {} spent {} USD on his first card payment transaction'.format(u[0],round(u[1],2)))

    # 4. Determine whether a user (uuid) might be fraudulent
    uuid = ['dc5c8c34-ca06-48a0-aa7e-4597dfce0051'] # PLEASE CHANGE FOR DIFFERENT USER
    fd = FraudDetector()
    for uid in uuid:
        action = fd.execute(uid)
        print(action)




