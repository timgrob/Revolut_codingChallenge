from ETL.ETLRepository import ETLRepository
import pandas as pd


class FeatureSelector(object):
    features = ['birth_year', 'country', 'has_email', 'failed_sign_in_attempts']

    etl = ETLRepository()

    def selectFeaturesForUser(self, uuid):
        users = self.etl.fetchUsers()
        user = self.etl.fetchSingleUser(uuid)
        X = users[self.features]
        Y = users['is_fraudster']
        u = user[self.features]
        X_dummy = pd.get_dummies(X)
        usr = u.reindex(columns=X_dummy.columns, fill_value=0)

        return usr, X_dummy, Y
