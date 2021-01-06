# https://datascienceplus.com/linear-regression-in-python-predict-the-bay-areas-home-prices/
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.tools.plotting import scatter_matrix
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingRegressor
import time
import numpy as np


pd.set_option('display.expand_frame_repr', False)       # display entire tables

# import the dataset
sf = pd.read_csv('final_data.csv')
sf.head()

# remove the columns that are not applicable
sf.drop(sf.columns[[0, 2, 3, 15, 17, 18]], axis=1, inplace=True)
'''sf.info()'''   # outputs information about the data, including the data type

# change zindex from string / object to numeric value it's of the form 123,123
sf['zindexvalue'] = sf['zindexvalue'].str.replace(',', '')
sf['zindexvalue'] = sf['zindexvalue'].convert_objects(convert_numeric=True)

# max and min of the sale dates
sf.lastsolddate.min(), sf.lastsolddate.max()

# summary statistics of the data, not displaying correctly columns are truncated
# std standard deviation, and 25%, 50%, 75% show percentiles
print(sf.describe())

# plot a histogram for each numeric variable
sf.hist(bins=50, figsize=(20,15))
plt.savefig("attribute_histogram_plots")
'''plt.show()'''

# scatter plot
sf.plot(kind="scatter", x="longitude", y="latitude", alpha=0.2)
'''plt.savefig('map1.png')'''

# colour the scatter plot (note can be interpreted as most expensive properties are north in the
# city
sf.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4, figsize=(10,7), c="lastsoldprice", cmap=plt.get_cmap("jet"), colorbar=True, sharex=False)
'''plt.savefig('map2.png')'''

# variable we are trying to predict is last sold price
# we look at how much each independent variable corresponds with }}}this{{{ dependent variable
'''corr_matrix = sf.corr()
print(corr_matrix["lastsoldprice"].sort_values(ascending=False))'''

# vizualization of the correlation between the variables, that seem the most correlated with the
# last sold price
attributes = ["lastsoldprice", "finishedsqft", "bathrooms", "zindexvalue"]
scatter_matrix(sf[attributes], figsize=(12, 8))
# plt.savefig('matrix.png')

# picture indicates that the most promising variable for predicting the last sold price is the
# finished sqft, so we zoom in on that one
sf.plot(kind="scatter", x="finishedsqft", y="lastsoldprice", alpha=0.5)
# plt.savefig('scatter.png')

# the correlation is very strong -- clear upward trend and the points are not too dispersed

# we need to add a variable for price per square foot to normalize and form comparisons
sf['price_per_sqft'] = sf['lastsoldprice']/sf['finishedsqft']
corr_matrix =sf.corr()
corr_matrix["lastsoldprice"].sort_values(ascending=False)

# psf variable not very strongly correlated, still needed to create groups

len(sf['neighborhood'].value_counts())      #number of distinct neighbourhoods

# we cluster the neighbourhoods into three groups: 1. low price; 2. high price low frequency;
# high price high frequency
freq = sf.groupby('neighborhood').count()['address']
mean = sf.groupby('neighborhood').mean()['price_per_sqft']
cluster = pd.concat([freq, mean], axis=1)
cluster['neighborhood'] = cluster.index
cluster.columns = ['freq', 'price_per_sqft','neighborhood']
print(cluster.describe())

# the low price neighbourhoods
cluster1 =cluster[cluster.price_per_sqft < 756]
# print(cluster1.index)

# high price and low frequency neighbourhoods
cluster_temp = cluster[cluster.price_per_sqft >= 756]
cluster2 = cluster_temp[cluster_temp.freq <123]
# print(cluster2.index)

# high price high frequency
cluster3 = cluster_temp[cluster_temp.freq >=123]
# print(cluster3.index)


# add a group column based on the clusters
def get_group(x):
    if x in cluster1.index:
        return 'low_price'
    elif x in cluster2.index:
        return 'high_price_low_freq'
    else:
        return 'high_price_high_freq'


sf['group'] = sf.neighborhood.apply(get_group)

# we can now get rid of the following columns
# “address, lastsolddate, latitude, longitude, neighborhood, price_per_sqft”

sf.drop(sf.columns[[0, 4, 6, 7, 8, 13]], axis=1, inplace=True)
sf = sf[['bathrooms', 'bedrooms', 'finishedsqft', 'totalrooms', 'usecode', 'yearbuilt','zindexvalue', 'group',
         'lastsoldprice']]
print(sf.head())

# data is good, just need to create dummy variables for the categorical varibales: "usecode", "group"
X = sf[['bathrooms', 'bedrooms', 'finishedsqft', 'totalrooms', 'usecode', 'yearbuilt', 'zindexvalue', 'group']]
Y = sf['lastsoldprice']

n = pd.get_dummies(sf.group)
X = pd.concat([X, n], axis=1)
m = pd.get_dummies(sf.usecode)
X = pd.concat([X, m], axis=1)
drops = ['group', 'usecode']
X.drop(drops, inplace=True, axis=1)
print(X.head())

# now we train and build the linear regression model
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

regressor = LinearRegression()
print(regressor.fit(X_train, y_train))

# calculate the R squared
y_pred = regressor.predict(X_test)
print('Liner Regression R squared: %.4f' % regressor.score(X_test, y_test))
# in our model, 56.19% of the variability in Y can be explained by using X (Not that exciting)

# calculate root-mean-square-error (RMSE)
lin_mse = mean_squared_error(y_pred, y_test)
lin_rmse = np.sqrt(lin_mse)
print('Liner Regression RMSE: %.4f' % lin_rmse)
# this tells us that our model was able to predict the value of every house in the test set within
# $616071 of the real price

# calculate the mean absolute error (MAE)
lin_mae = mean_absolute_error(y_pred, y_test)
print('Liner Regression MAE: %.4f' % lin_mae)

# we try a more complex model to see whether the results can be imporved
# RANDOM FOREST
forest_reg = RandomForestRegressor(random_state=42)
print(forest_reg.fit(X_train, y_train))

print('Random Forest R squared": %.4f' % forest_reg.score(X_test, y_test))

y_pred = forest_reg.predict(X_test)
forest_mse = mean_squared_error(y_pred, y_test)
forest_rmse = np.sqrt(forest_mse)
print('Random Forest RMSE: %.4f' % forest_rmse)

# much better!

# We try one more
# GRADIENT BOOSTING

model = ensemble.GradientBoostingRegressor()


print('Gradient Boosting R squared": %.4f' % model.score(X_test, y_test))

y_pred = model.predict(X_test)
model_mse = mean_squared_error(y_pred, y_test)
model_rmse = np.sqrt(model_mse)
print('Gradient Boosting RMSE: %.4f' % model_rmse)

# best results so far

# We have used 19 features (variables) in our model, we find out which ones are important
feature_labels = np.array(['bathrooms', 'bedrooms', 'finishedsqft', 'totalrooms', 'yearbuilt', 'zindexvalue',
                           'high_price_high_freq', 'high_price_low_freq', 'low_price', 'Apartment', 'Condominium',
                           'Cooperative', 'Duplex', 'Miscellaneous', 'Mobile', 'MultiFamily2To4', 'MultiFamily5Plus',
                           'SingleFamily', 'Townhouse'])
importance = model.feature_importances_
feature_indexes_by_importance = importance.argsort()
for index in feature_indexes_by_importance:
    print('{}-{:.2f}%'.format(feature_labels[index], (importance[index] *100.0)))



























