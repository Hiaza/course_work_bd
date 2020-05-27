import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import make_pipeline

import db_utils
from math import radians, cos, sin, asin, sqrt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

client = db_utils.get_connection('mongodb://localhost:27117')
db = client.Course_Work
collection = db.Checks


def sum_per_day():
    df = pd.DataFrame(collection.find())
    print(df['day_of_week'])
    df2 = df[['day_of_week', 'sum']]
    df2 = df2.groupby('day_of_week')["sum"].apply(lambda x : x.astype(int).sum())

    #sorting values for actual day order
    x = df2[1]
    df2[1] = df2[0]
    df2[0] = x

    x = df2[2]
    df2[2]=df2[6]
    df2[6]=x

    x = df2[3]
    df2[3] = df2[5]
    df2[5] = x

    plt.stem(["Monday", "Tuesday","Wednesday","Thursday","Friday", "Saturday", "Sunday"],df2, use_line_collection=True)

    plt.show()


def sum_per_check():
    df = pd.DataFrame(collection.find())
    # Make default histogram of sepal length
    sns.distplot(df["sum"])
    plt.show()


def num_of_purchases_per_check():
    df = pd.DataFrame(collection.find())
    # Make default histogram of sepal length
    sns.distplot(df["num_of_purchases"])
    plt.show()


def get_united_df():
    df = pd.DataFrame(collection.find())
    df_users = pd.DataFrame(db.Users.find())

    df2 = pd.merge(df, df_users, how="left", left_on='owner', right_on='_id')
    df2['distance'] = df2[['latitude','longitude']].apply(f, axis=1)
    return df2



def sum_per_distance():

    df2 = get_united_df()
    print(df2)
    np_df = df2.to_numpy()
    x = np_df[:, 11].reshape(-1, 1)
    y = np_df[:, 2].reshape(-1, 1)
    model = create_polynomial_model(x,y)

    plt.figure(figsize=(8, 6), dpi=140)

    plt.ylabel("sum")
    plt.xlabel("distance")
    # plot training data
    plt.scatter(x, y, s=1, label='Training points')
    # plot predicted values
    x_plot = np.linspace(0, max(x)).reshape(-1, 1)
    plt.plot(x_plot, model.predict(x_plot), color='red', label='Predicted values')
    plt.legend(loc='upper left')

    window_title = "Регресія тип 2"
    plt.draw()
    plt.gcf().canvas.set_window_title(window_title)
    plt.show()
    plt.close()


def num_of_purchases_per_distance():
    df2 = get_united_df()
    sns.regplot(x=df2["distance"][:500], y=df2["num_of_purchases"][:500],
                line_kws={"color": "r", "alpha": 0.7, "lw": 5})
    plt.show()


def haversine(lat1, lon1, lat2, lon2):

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def f(x):
    firstMag = [50.445357, 30.523378]
    secondMag = [50.453509, 30.614799]
    nearMag = []
    if x[0]-firstMag[0] + x[1]-firstMag[1] > x[0]-secondMag[0] + x[1]-secondMag[1]:
        nearMag = secondMag
    else:
        nearMag = firstMag

    distance = haversine(x[0], x[1], nearMag[0], nearMag[1])
    return distance


def create_linear_model(x, y):
    model = LinearRegression()
    model.fit(x, y)
    return model


def create_polynomial_model(x, y):
    degree = 5
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(x, y)
    return model
