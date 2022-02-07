# Income optmizer for Airbnb Hosts  

## Problem Statement

**Goal**: 
Help Airbnb hosts maximize their total income by optimizing their listing price and booking rate 
- What can a host do to improve the listing price of their unit?
- What can a host do to reduce the vacancy rate of their unit?

The primary goal is prediction. Some inferences would be drawn from feature importance if possible.

The audience for this project are the Airbnb hosts.

## Data and Method

### Data
Airbnb listings data for three Bay Area counties (San Francisco, San Mateo, Santa Clara), collected between late October to early December 2021, from [Inside Airbnb](http://insideairbnb.com/get-the-data.html). 

The listings data include the following information: 
- Listing price
- Availability in the next 30 days
- Location and size of the unit
- Amenities
- Review scores and review counts
- Availability of more information about the unit and the host 

In the current analysis, 
1. Listings that charge over $1000/night were dropped, which is 1.3% of the data.
2. Neighborhoods and property types that have less than 100 listings were grouped under "Other", respectively.
3. The goal is to maximize the total income in the next 30 days. Therefore, listings that have zero availability in the next 30 days were dropped.

See [here](https://github.com/AnnieW2014/GA_Capstone/blob/main/Data_Dictionary.md) for a detailed data dictionary.

<br>

### Modeling
#### Stage 1. Predict listing price
The predictors include all kinds of unit features. 
The following models were trained and evaluated.
- Baseline model
- Random forest
- XGBoost 

#### Stage 2. Predict 30 day vacancy 
The predictors include unit features, listing price and the predicted price from Stage 1. 
The following models were trained and evaluated.
- Baseline model
- Random forest
- XGBoost

#### Model selection
- The performance metrics include R2 and mse. R2 was used to select models.
- Grid Search CV was used to tune hyperparameters.
- At both stages, XGBoost models were selected as the final ones.

#### Improving model performance
The intial models for both price and 30-day vacancy were seriously overfitted. The following approaches were taken to improve on this issue.
1. Reduce the number of dummy variables by dropping very small categories in neighborhood and property type. 
2. Tune the hyperparameters:
- the shape of the trees: max depth, minimum size of a leaf, minimum size of a node for splitting 
- the max number of features
- learning rate: XGBoost eta
- lambda for L2 regularization 
3. Further trim the feature list based on feature importance. Both final models used the top ~50 features out of the original 100. 

In the end, the overfitting was greatly reduced (see the Model Summary section).

<br>

## Findings

### Explortary Data Analysis

#### Price

1. The overall average price is \$178. Most listings are below $300.
2. The average price is highest in San Francisco and lowest in Santa Clara.

![price in histogram](/Plots/price_hist.png)

![price by county in histogram](/Plots/price_bycounty_hist2.png)

<br>

#### Price and numeric features

1. Price is most correlated with size related features, such as the number of bedrooms , the bathrooms, and the number of people the unit can accommodate. 
2. Some amenities are positively correlated with price: indoor fireplace, private entrance, BBQ grill and patio or balcony, etc.
3. Review scores on overall rating, cleanliness and location are weakly correlated with price.

<br>

![correlation between price and all features in heatmap](/Plots/corr_price_features_heat.png)

![correlation between price and size features in regplot](/Plots/corr_price_sizes_regplot.png)

![correlation between price and review scores in regplot](/Plots/corr_price_reviewscores_regplot.png)

<br>

#### Price and property type and neighborhood

1. The entire units (residential homes, townhouses, condo/apartment), have higher prices than private rooms in a unit. The hotel rooms ranked between the two.
2. The most expensive neighborhoods are Russian Hill, Pacific Heights and Marina, all in San Francisco.

![price by property type in barh](/Plots/price_propertytype_barh.png)

![top 10 neighborhoods by price in barh](/Plots/price_neighborhood_top10_barh.png)

<br>

#### 30-Day vacancy

<br>

1. The overall 30-day vacancy is 17 days. 
2. On average, Santa Clara's 30-day vacancy is the highest (18.1) and that of San Francisco (15.6) is the lowest.

![avail30 in hist](/Plots/avail30_hist.png)

![avail30 by county in hist](/Plots/avail30_bycounty_hist2.png)

<br>

#### 30-Day vacancy and features

<br>

30-day vacancy is negatively related to all review scores and counts.
> - The overall rating has the highest correlaton with the 30-day vacancy among all review related features.

![correlation between avail30 and review scores and counts in one column](/Plots/corr_avail30_reviewfeatures_heat.png)

<br>

Listings that provide host acceptance rate and and response time have lower 30-day vacancy. 

![correlation between avail30 and flag columns in heatmap](/Plots/corr_avail30_flagcols_heat.png)

<br>

Among reviews on specific aspects, 
- listing info accuracy and perceived value are most correlated to the overall rating
- location is least correlated to the overall rating.

![correlation between avail30 and review scores and counts in triangle](/Plots/corr_avail30_reviewfeatures_heat_triagle.png)

<br>

### Model Summary

<br>

#### Stage 1: Predict listing price

The XGBoost model with grid search using the top 50 features was selected as the final model and was used to create the predicted price, which was used in the Stage 2 model.

| **Model**                                     | **R2 train** | **R2 test** | **MSE train** | **MSE test** |
|-----------------------------------------------|--------------|-------------|---------------|--------------|
| Baseline                                      |              |             | 21698         | 23040        |
| Random Forest                                 | 0.9497       | 0.6574      | 1090          | 7894         |
| Random Forest + Grid Search + all features    | 0.8152       | 0.6465      | 4010          | 8145         |
| Random Forest + Grid Search + top 50 features | 0.8126       | 0.646       | 4066          | 8156         |
| XGBoost                                       | 0.9448       | 0.6569      | 1197          | 7905         |
| XGBoost + Grid Search + all features          | 0.8449       | 0.6907      | 3364          | 7125         |
| **XGBoost + Grid Search + top 50 features**   | **0.8001**   | **0.6849**  | **4336**      | **7259**     |

<br>

#### Stage 2: Predict 30-day vacancy

The XGBoost model with grid search using the top 50 features was selected as the final model and was used to predict 30-day vacancy.

| **Model**                                     | **R2 train** | **R2 test** | **MSE train** | **MSE test** |
|-----------------------------------------------|--------------|-------------|---------------|--------------|
| Baseline                                      |              |             | 94.7495       | 94.14        |
| Random Forest                                 | 0.8934       | 0.2142      | 10.1046       | 73.98        |
| Random Forest + Grid Search + all features    | 0.5866       | 0.2212      | 39.1741       | 73.31        |
| Random Forest + Grid Search + top 20 features | 0.5954       | 0.1943      | 38.336        | 75.85        |
| XGBoost                                       | 0.8724       | 0.1896      | 12.0858       | 76.29        |
| XGBoost + Grid Search + all features          | 0.5992       | 0.2286      | 37.9753       | 72.61        |
| **XGBoost + Grid Search + top 50 features**   | **0.4759**   | **0.2184**  | **49.6594**   | **73.58**    |

<br>

#### Feature importance
Price and 30-day vacancy share some important predictors (e.g., bathroom type, county, min number of nights), and have their unique ones.

1. The most important features predicting **pricing** are:
>- size: number of bedrooms and bathrooms, how many people to accommodate
>- location: county, some neighborhoods
>- property type (entire unit vs one room) and bathrooms type (private or shared)
>- amenities: Pool, Wifi

2. The most important features predicting **30-day vacancy** are: 
>- activity level: review count in last 12 months and last 30 days
>- availablity of some info: host acceptance rate
>- property type (entire unit vs one room) and bathrooms type (private or shared)
>- location: county and some neighborhoods 
>- predicted price

See the table below for the top 15 important features for predicting price and 30-day vacancy. 

<table>
<tr><th>Price Prediction </th><th>30-day Vacancy Prediction</th></tr>
<tr><td>

|    | Feature                                                | Importance |
|----|:------------------------------------------------------:|:----------:|
| 1  |                                               bedrooms | 0.3559     |
| 2  |                                   county_San Francisco |     0.0381 |
| 3  |                                           accommodates |     0.0354 |
| 4  |                                   bathroom_type_shared |     0.0332 |
| 5  |                                              bathrooms |     0.0281 |
| 6  |                                     county_Santa Clara |     0.0223 |
| 7  |         property_type_Private room in residential home |     0.0167 |
| 8  |                       neighborhood_Santa Clara         |     0.0147 |
| 9  |    neighborhood_San Mateo Unincorporated Areas         |     0.0134 |
| 10 |                                         minimum_nights |     0.0126 |
| 11 |                           neighborhood_Pacific Heights |     0.0126 |
| 12 |                                 neighborhood_Palo Alto |     0.0120 |
| 13 |                       neighborhood_Castro/Upper Market |     0.0115 |
| 14 |                                                   Pool |     0.0109 |
| 15 |                                                   Wifi |     0.0108 |

</td><td>

|    |                                 Feature | Importance |
|----|:---------------------------------------:|:----------:|
| 1  |                   number_of_reviews_ltm |     0.0375 |
| 2  |                  host_acceptance_rate_f |     0.0364 |
| 3  |                    bathroom_type_shared |     0.0288 |
| 4  |               neighborhood_Inner Sunset |     0.0266 |
| 5  |        property_type_Entire rental unit |     0.0238 |
| 6  |                    county_San Francisco |     0.0206 |
| 7  |        property_type_Entire guest suite |     0.0198 |
| 8  |                          minimum_nights |     0.0191 |
| 9  | property_type_Entire serviced apartment |     0.0169 |
| 10 |                 neighborhood_Noe Valley |     0.0161 |
| 11 |    property_type_Room in boutique hotel |     0.0158 |
| 12 |               neighborhood_Potrero Hill |     0.0157 |
| 13 |                  number_of_reviews_l30d |     0.0155 |
| 14 |               neighborhood_Outer Sunset |     0.0144 |
| 15 |                              price_pred |     0.0139 |

</td></tr> </table>

<br>

### streamlit app implementation

At [this webpage](http://localhost:8501/), an Airbnb host can predict their 30-day income by providing some info about their unit and the price they'd like to charge. 

<br>

## Conclusions
To maximize the total income, hosts should optimize both price and demand at the same time, and understand their interdependence and their drivers.

Location, bathroom type (private vs shared) and the minimum number of nights to book are important predictors shared by price and 30-day vacancy. 

Size features (number of bedrooms and bathrooms, total number of people to accommodate) are the most important predictors for price, and are less important for demand. This is probably because while bigger units are reasonably be more expensive, different sizes have their own share of the market.    

The number of reviews a unit received in last 12 months and whether the host acceptance rate is provided on the website are the most important predictors for 30-day vacancy, and are not as important for pricing. There are two potential reasons. 
- The number of reviews indicates how active the unit has been (how frequently it has been booked). So it could also predict how active it would be in the near future. 
- Listings with more reviews look more pouplar and reliable to guests, with other things comparable. In this way, they become more desirable and have lower vacancy.  

In terms of amenities, 
- Pool and wifi are important to pricing, indoor fireplace and BBQ grill to a lessor extent. 
- Patio or balcony, pool, backyard, outdoor furniture and private entrance are important for demand.   

<br>

## Recommendations
Use [the tool](http://localhost:8501/) to find the optimal combination of the unit features, Airbnb account management (information provision), and the listing price, to maximize the 30-day total income from a listing unit.   

<br>

## Next steps
1. Try to further reduce the overfitting issue. 
>- find or create a higher-level feature for neighborhood: currently, the county column is too high level and the neighborhood column is too detailed.
>- feature engineering: use composite features based on principal component analysis
2. The prediction model for 30-day vacancy has a lot of room for improvement. Some methods in the plan include:
>- Better understand the availability columns: further examine data quality, understand how voluntary unavailability works here
>- Use more data: collect data for more counties since the dataset was noticeably reduced when droppoing the listings that have zero 30-day vacancy.
>- Add more features: There are more data on the website, including review text. 
>- feature engineering
