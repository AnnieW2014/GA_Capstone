# 1. Model 1: predict price

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import metrics

from xgboost import XGBRegressor
import category_encoders as ce
import datetime
import joblib



## 1.1 prepare data
df = pd.read_csv('Listings_combined_cleaned.csv')

## create X_train, y_train, X_test, y_test
X = df.drop(columns=['price','availability_30', 'availability_60','availability_90'])
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
X_train.shape, y_train.shape, X_test.shape, y_test.shape

## create train for EDA
train = df.loc[df.index.isin(X.index), :]

## 1.2 RandomForest + GridSearchCV

### build the model
m1_pipe_rf = Pipeline([
    ('ohe', ce.one_hot.OneHotEncoder(use_cat_names=True, handle_unknown='value')),
    ('rf', RandomForestRegressor(random_state=42, n_jobs=-1))
])

m1_pipe_rf_params = {
    'rf__n_estimators': [400, 500, 600, 700, 800],
    'rf__max_depth': [6, 8, 10, 12, 14, 16, 18, 20],
    'rf__min_samples_split': [10, 20],
    'rf__min_samples_leaf': [5],
    #'rf__ccp_alpha': [0.0, 0.05, 0.1],
    'rf__max_features': [15, 30, 60, 90]
}

m1_gs_rf = GridSearchCV(m1_pipe_rf,
                        m1_pipe_rf_params,
                        cv=5)

### train the model
print(datetime.datetime.now())
m1_gs_rf.fit(X_train, y_train)
print(datetime.datetime.now())

import joblib

# save m1_gs_rf
m1_gs_rf_joblib_filename = 'm1_gs_rf_joblib.pkl'

joblib.dump(m1_gs_rf, m1_gs_rf_joblib_filename)

### predict
m1_gs_rf_pred_train = m1_gs_rf.predict(X_train)
m1_gs_rf_pred_test = m1_gs_rf.predict(X_test)

### evaluate
m1_gs_rf_R2_train = m1_gs_rf.score(X_train, y_train)
m1_gs_rf_R2_test = m1_gs_rf.score(X_test, y_test)
print('m1_gs_rf_R2_train: ', round(m1_gs_rf_R2_train, 4))
print('m1_gs_rf_R2_test:  ', round(m1_gs_rf_R2_test, 4))

m1_gs_rf_mse_train = metrics.mean_squared_error(y_train, m1_gs_rf_pred_train)
m1_gs_rf_mse_test = metrics.mean_squared_error(y_test, m1_gs_rf_pred_test)
print('m1_gs_rf_mse_train: ', round(m1_gs_rf_mse_train, 4))
print('m1_gs_rf_mse_test:  ', round(m1_gs_rf_mse_test, 4))

print(m1_gs_rf.best_estimator_)

### Feature importance
m1_gs_rf_feature_importance = pd.DataFrame({'feature': m1_gs_rf.best_estimator_['ohe'].get_feature_names(),
                                         'importance': m1_gs_rf.best_estimator_['rf'].feature_importances_})

print(m1_gs_rf_feature_importance.sort_values('importance', ascending=False).head(30))
m1_gs_rf_feature_importance.sort_values('importance', ascending=False)

## 2. Model 2: predict availability_30

# Random Forest + GridSearchCV

# build the model
m21_pipe_rf = Pipeline([
    ('ohe', ce.one_hot.OneHotEncoder(use_cat_names=True, handle_unknown='value')),
    ('rf', RandomForestRegressor(random_state=42, n_jobs=-1))
                     ])

m21_pipe_rf_params = {
    'rf__n_estimators': [400, 800, 900, 1000],
    'rf__max_depth': [4, 8, 12, 16, 20],
    'rf__min_samples_split': [10, 20],
    'rf__min_samples_leaf': [5,10],
    'rf__ccp_alpha': [0.0, 0.05, 0.1],
    'rf__max_features': [20,60, 80, 90]
}

m21_gs_rf = GridSearchCV(m21_pipe_rf,
                        m21_pipe_rf_params,
                        cv=5
                       )
# train the model
print(datetime.datetime.now())
m21_gs_rf.fit(X_train, y_train)
print(datetime.datetime.now())

# predict
m21_gs_rf_pred_train = m21_gs_rf.predict(X_train)
m21_gs_rf_pred_test = m21_gs_rf.predict(X_test)

# evaluate
m21_gs_rf_R2_train = m21_gs_rf.score(X_train, y_train)
m21_gs_rf_R2_test = m21_gs_rf.score(X_test, y_test)
print('m21_gs_rf_R2_train: ' + f'{round(m21_gs_rf_R2_train, 4)}')
print('m21_gs_rf_R2_test:  ' + f'{round(m21_gs_rf_R2_test, 4)}')

m21_gs_rf_mse_train = metrics.mean_squared_error(y_train, m21_gs_rf_pred_train)
m21_gs_rf_mse_test = metrics.mean_squared_error(y_test, m21_gs_rf_pred_test)
print('m21_gs_rf_mse_train: ' + f'{round(m21_gs_rf_mse_train, 4)}')
print('m21_gs_rf_mse_test:  ' + f'{round(m21_gs_rf_mse_test, 4)}')

print(m21_gs_rf.best_estimator_)

# feature importance
m21_gs_rf_feature_importance = pd.DataFrame({'feature': m21_gs_rf.best_estimator_['ohe'].get_feature_names(),
                                             'importance': m21_gs_rf.best_estimator_['rf'].feature_importances_})

m21_gs_rf_feature_importance.to_csv('m21_gs_rf_feature_importance.csv')
m21_gs_rf_feature_importance.sort_values('importance', ascending=False).head(20)

# build the model
m21_pipe_xgb = Pipeline([
    ('ohe', ce.one_hot.OneHotEncoder(use_cat_names=True, handle_unknown='value')),
    ('xgb', XGBRegressor(random_state=42, n_jobs=-1))
])

m21_pipe_xgb_params = {
    #'xgb__booster': ['gbtree','gblinear'],
    'xgb__n_estimators': [400, 600, 800],
    'xgb__eta': [0.01, 0.03, 0.05, 0.1, 0.2, 0.3, 0.4],
    'xgb__reg_alpha': [0, 5],
    'xgb__reg_lambda': [0, 5],
    'xgb__max_depth': [4,6,8],
}

m21_gs_xgb = GridSearchCV(m21_pipe_xgb,
                         m21_pipe_xgb_params,
                         cv = 5)
# train the model
print(datetime.datetime.now())

m21_gs_xgb.fit(X_train, y_train)

print(datetime.datetime.now())

# predict
m21_gs_xgb_pred_train = m21_gs_xgb.predict(X_train)
m21_gs_xgb_pred_test = m21_gs_xgb.predict(X_test)

# evaluate
m21_gs_xgb_R2_train = m21_gs_xgb.score(X_train, y_train)
m21_gs_xgb_R2_test = m21_gs_xgb.score(X_test, y_test)
print(f'm21_gs_xgb_R2_train: {m21_gs_xgb_R2_train}')
print(f'm21_gs_xgb_R2_test: {m21_gs_xgb_R2_test}')

m21_gs_xgb_mse_train = metrics.mean_squared_error(y_train, m21_gs_xgb_pred_train)
m21_gs_xgb_mse_test = metrics.mean_squared_error(y_test, m21_gs_xgb_pred_test)
print(f'm21_gs_xgb_mse_train: {m21_gs_xgb_mse_train}')
print(f'm21_gs_xgb_mse_test: {m21_gs_xgb_mse_test}')

print(m21_gs_xgb.best_estimator_)

# feature importance
m21_gs_xgb_feature_importance = pd.DataFrame({'feature': m21_gs_xgb.best_estimator_['ohe'].get_feature_names(),
                                         'importance': m21_gs_xgb.best_estimator_['xgb'].feature_importances_})

m21_gs_xgb_feature_importance.sort_values('importance', ascending=False).head(20)
