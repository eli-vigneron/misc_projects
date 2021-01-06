# imports
import numpy as np
from sklearn import linear_model
import math
from sklearn.linear_model import LinearRegression

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# Plotting Libs
import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_style('whitegrid')
import sklearn
import scipy.stats as stats
import sklearn.cross_validation

def main():
    commercial = pd.read_excel('.../sales.xlsx')
    commercial = commercial[['Assessed Value', 'site area', 'time adjusted']]

    X = commercial.drop('Assessed Value', axis=1)

    # create a linear regression object
    lm = LinearRegression()
    lm.fit(X, commercial['Assessed Value'])
    print('Estimated intercept coefficient:', lm.intercept_)
    print('Number of Coefficients:', len(lm.coef_))

    # dataframe containing features and estimated coefficients
    print(pd.DataFrame(list(zip(X.columns, lm.coef_)), columns=['features', 'estimated coefficients']))

    # plot the highly correlated variable
    plt.scatter(commercial['Assessed Value'], commercial['site area'])
    plt.xlabel('site area')

    # predict and show the first 5 predicted assessments
    print(lm.predict(X))

    # plot predictions vs real
    plt.scatter(lm.predict(X), commercial['Assessed Value'])
    plt.xlabel("Assessed Value")
    plt.ylabel('Predicted')
    plt.show()

    mseFull = np.mean((commercial['Assessed Value'] - lm.predict(X))**2)
    print(mseFull)

    X_train, X_test, Y_train, Y_test = sklearn.cross_validation.train_test_split(
        X, commercial['Assessed Value'], test_size=0.33, random_state=5)
    lm2 = LinearRegression()
    lm2.fit(X_train, Y_train)
    pred_train = lm2.predict(X_train)
    pred_test = lm2.predict(X_test)

    print('Fit a model X_train, and calculate MSE with Y_train:', np.mean((Y_train - pred_train)**2))
    print('Fit a model X_train, and calculate MSE with X_test, Y_test:', np.mean((Y_test - pred_test) ** 2))

    plt.scatter(pred_train, pred_train - Y_train, c='b', s=40, alpha=0.5)
    plt.scatter(pred_test, pred_test - Y_test, c='g', s=40)

    plt.title('Residual Plot using training (blue) and test (green) data')
    plt.ylabel('Residuals')
    plt.show()


if __name__ == "__main__":
    main()