from ETL.ETLRepository import ETLRepository
from detection_algorithm.RiskEstimation import RiskEstimator
from detection_algorithm.FeatureSelection import FeatureSelector
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class FraudDetector(object):

    action = {
        'LOCK': 'LOCK_USER',
        'ALERT': 'ALERT_AGENT',
        'BOTH': 'BOTH',
        'SAVE': 'SAVE'
    }

    riskTreshold = 0.5
    accuracyTreshold = 0.95
    etl = ETLRepository()
    re = RiskEstimator()
    fs = FeatureSelector()

    def execute(self,uuid):
        actionBlock = self.checkBlocked(uuid)
        if actionBlock != self.action['SAVE']:
            finalAction = actionBlock
        else:
            actionNationality = self.checkNationality(uuid)
            if actionNationality != self.action['SAVE']:
                finalAction = actionNationality
            else:
                finalAction = self.checkUserFeatures(uuid)

        return finalAction

    def checkBlocked(self, uuid):
        user = self.etl.fetchSingleUser(uuid)
        userState = user['state'].item()
        userKyc = user['kyc'].item()

        if userState != 'LOCKED':
            return self.action['SAVE']

        if userKyc.upper == 'FAILED':
            action = self.action['LOCK']
        else:
            action = self.action['BOTH']

        return action


    def checkNationality(self,uuid):
        user = self.etl.fetchSingleUser(uuid)
        userNationality = user['country']
        countryRisk = self.re.natioanlityRisk()
        riskyCountry = countryRisk[countryRisk['country_risk']>self.riskTreshold]

        if userNationality.isin(riskyCountry['country']).any():
            action = self.action['ALERT`']
        else:
            action = self.action['SAVE']

        return action


    def checkUserFeatures(self,uuid):
        usr, users_X, users_Y = self.fs.selectFeaturesForUser(uuid)
        x_train, x_test, y_train, y_test = train_test_split(users_X, users_Y, test_size=0.2)

        clf = RandomForestClassifier(n_estimators=100, random_state=0)
        clf.fit(x_train, y_train)
        pred = clf.predict(x_test)
        acc = accuracy_score(y_test, pred)

        if acc<self.accuracyTreshold:
            print('Model for User: {} lacks accuracy -> please check'.format(uuid))
            action = self.action['ALERT']
        else:
            predFraud = clf.predict(usr)
            if predFraud:
                action = self.action['ALERT']
            else:
                action = self.action['SAVE']

        return action
