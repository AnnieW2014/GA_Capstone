# Income optmizer for Airbnb Hosts  

## Problem Statement

Goal: 
Help Airbnb hosts maximize their total income by optimizing their listing price and booking rate 
- What can a host do to improve the listing price of their unit?
- What can a host do to improve the booking rate of their unit?

Audience: Airbnb hosts

## Data and Method

### Data
Airbnb listings data for three counties (San Francisco, San Mateo, Santa Clara) from [Inside Airbnb](http://insideairbnb.com/get-the-data.html). 

The listings data include: 
- Lising price
- Availability in the next 30 days
- Location and size of the unit
- Available amenities
- Review scores and review counts
- Information provided about the unit or host on Airbnb

##### Data Dictionary

| **Feature**                 | **Type** | **Description**                                            |
|-----------------------------|----------|------------------------------------------------------------|
| county                      | object   | county                                                     |
| neighborhood_cleaned        | object   | neighborhood                                               |
| property type               | object   | property type                                              |
| accommodates                | integer  | the max number of people the listing unit can accommodate  |
| beds                        | integer  | the number of beds in the unit                             |
| bedrooms                    | integer  | the number of bedrooms in the unit                         |
| bathrooms                   | integer  | the number of bathrooms in the unit                        |
| bathroom type               | object   | the type of bathroom(s), i.e., private or shared           |
| minimum nights              | integer  | the minimum number of days a guest has to book             |
| maximum nights              | interger | the maximum number of days a guest can book                |
| Wifi                        | boolean  | whether the unit has Wifi                                  |
| Dedicated workspace         | boolean  | whether the unit has a dedicated workspace                 |
| private entrance            | boolean  | whether the unit has a private entrance                    |
| Backyard                    | boolean  | whether the unit has a backyard                            |
| BBQ_grill                   | boolean  | whether the unit has BBQ grill                             |
| Outdoor_furniture           | boolean  | whether the unit has outdoor furniture                     |
| Indoor_fireplace            | boolean  | whether the unit has indoor fireplace                      |
| Pool                        | boolean  | whether the unit has pool                                  |
| review_scores_rating        | float    | review score on the overall rating                         |
| review_scores_accuracy      | float    | review score on accuracy of the information on the unit    |
| review_scores_cleanliness   | float    | review score on cleanliness                                |
| review_scores_checkin       | float    | review score on the checkin process                        |
| review_scores_communication | float    | review score on communication with the host                |
| review_scores_location      | float    | review score on the location                               |
| review_scores_value         | float    | review score on value                                      |
| number_of_reviews           | integer  | total number of reviews the unit has                       |
| number_of_reviews_ltm       | integer  | the number of reviews in the last 12 months                |
| number_of_reviews_l30d      | integer  | the number of reviews in the last 30 days                  |
| neighborhood_overview_f     | boolean  | whether the information is provided: neighborhood overview |
| host_about_f                | boolean  | whether the information is provided: host's self-intro     |
| host_response_time_f        | boolean  | whether the information is provided: host response time    |
| host_response_rate_f        | boolean  | whether the information is provided: host response rate    |
| host_acceptance_rate_f      | boolean  | whether the information is provided: host acceptance rate  |
| host_neighbourhood_f        | boolean  | whether the information is provided: host neighborhood     |

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


## Findings

### Explortary Data Analysis



### Model Summary

#### Stage 1: Predict listing price

| **Model**                                     | **R2 train** | **R2 test** | **MSE train** | **MSE test** |
|-----------------------------------------------|--------------|-------------|---------------|--------------|
| Baseline                                      |              |             | 21698         | 23040        |
| Random Forest                                 | 0.9497       | 0.6574      | 1090          | 7894         |
| Random Forest + Grid Search + all features    | 0.8152       | 0.6465      | 4010          | 8145         |
| Random Forest + Grid Search + top 50 features | 0.8126       | 0.646       | 4066          | 8156         |
| XGBoost                                       | 0.9448       | 0.6569      | 1197          | 7905         |
| XGBoost + Grid Search + all features          | 0.8449       | 0.6907      | 3364          | 7125         |
| **XGBoost + Grid Search + top 50 features**   | **0.8001**   | **0.6849**  | **4336**      | **7259**     |

The XGBoost model with grid search using the top 50 features was selected as the final model and was used to create the predicted price, which was used in the Stage 2 model.

#### Stage 2: Predict 30-day vacancy


| **Model**                                     | **R2 train** | **R2 test** | **MSE train** | **MSE test** |
|-----------------------------------------------|--------------|-------------|---------------|--------------|
| Baseline                                      |              |             | 94.7495       | 94.14        |
| Random Forest                                 | 0.8934       | 0.2142      | 10.1046       | 73.98        |
| Random Forest + Grid Search + all features    | 0.5866       | 0.2212      | 39.1741       | 73.31        |
| Random Forest + Grid Search + top 20 features | 0.5954       | 0.1943      | 38.336        | 75.85        |
| XGBoost                                       | 0.8724       | 0.1896      | 12.0858       | 76.29        |
| XGBoost + Grid Search + all features          | 0.5992       | 0.2286      | 37.9753       | 72.61        |
| XGBoost + Grid Search + top 50 features       | 0.4759       | 0.2184      | 49.6594       | 73.58        |



#### Feature importance
[Have tables side by side in markdown](https://stackoverflow.com/questions/43232279/how-can-one-display-tables-side-by-side-in-github-markdown)

1. The most important features predicting **pricing** are:
>- size: number of bedrooms and bathrooms, how many people to accommodate
>- location: county, some neighborhoods
>- property type (entire unit vs one room) and bathrooms type (private or shared)
>- amenities: Pool, Wifi

2. The most important features predicting 30-day vacancy are: 
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

## Conclusions

## Recommendations

## Next steps