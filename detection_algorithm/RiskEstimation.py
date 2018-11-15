import numpy as np
import pandas as pd
from ETL.ETLRepository import ETLRepository


class RiskEstimator(object):
    etl = ETLRepository()

    def natioanlityRisk(self):
        signedUpCountries = self.etl.fetchDistinctUserCountries()
        users = self.etl.fetchUsers()
        totNumUsers = len(users.index)

        countryRisk = np.zeros([len(signedUpCountries.index),1])
        for idx, row in signedUpCountries.iterrows():
            usersFromCountry = self.etl.fetchUsersFromCountry(row['country'])
            fraudstersFromCountry = self.etl.fetchFraudstersFromCountry(row['country'])
            countryRisk[idx] = (len(fraudstersFromCountry)/len(usersFromCountry.index))/(len(usersFromCountry.index)/totNumUsers)

        signedUpCountries['country_risk'] = pd.DataFrame(countryRisk, index=signedUpCountries.index)

        return  signedUpCountries

