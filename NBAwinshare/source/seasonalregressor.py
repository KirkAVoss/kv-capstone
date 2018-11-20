import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
#from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import precision_score, recall_score, confusion_matrix
#import seaborn as sn
#from scipy import stats
#import pickle

class SeasonalRegressor():


    def __init__(self, regressor_type='RF'):
        '''
        Instantiates a model
        Input: regressor_type -- type of regressor used in the prediction algo, defaults to random forest (only option operative)
        '''
        self.years_to_predict = [5, 6, 7, 8, 9]
        self.regressor_dict = {}
        for year in self.years_to_predict:
            self.regressor_dict[year] = RandomForestRegressor(n_jobs=-1)


    def fit(self, X, y):
        '''
        Fit X and Y to the regressor'
        Returns self
        '''

        #need to fit the regressor for each year, which means I either need to break up the train data in acceptable year windows, or handle that here
        #Also need to make sure test / train split has various
        #Random Forest Fit


        return self


    def predict(self, X):
        '''
        Predict class for X.
        Returns y (predictions)

        '''
        #run the model for each classifier
        pass

    def predict_proba(self, X):
        '''
        Predict probabilities for class for X.
        Returns y (prediction probabilities) for the predicted class

        '''

        #get the probabilities for each classifier
        pass


    #this probably doesn't make sense, but don't want to delete it yet
    def confusion_matrix(self, ytest, ypred):
        '''Function prints the precision score, recall score, and plots the confusion matrix.'''
        tn, fp, fn, tp = confusion_matrix(ytest, ypred).ravel()
        cf= [[tp, fp],[fn, tn]]
        sn.set(font_scale=1.4) #for label size
        print(sn.heatmap(cf, annot=True,annot_kws={'size': 20}, fmt='d'))
        print('Precision Score: {}'.format(precision_score(ytest, ypred)))
        print('Recall Score: {}'.format(recall_score(ytest, ypred)))
