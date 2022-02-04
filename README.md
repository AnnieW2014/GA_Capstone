# Income optmizer with price elasticity - Help Airbnb Hosts Improve Income with Optimal Price-Booking Tradeoff 

## Problem Statement

Goal: 
Help Airbnb hosts maximize their total income (i.e., the product listing price and booking rate) of by identifying their best listing price and price elasticity of demand

Audience: Airbnb hosts

## Methods

### Data
Airbnb listing and review data from [Inside Airbnb](http://insideairbnb.com/get-the-data.html). 

The listing data includes 
- Features of the house/room: number of bedrooms and bathrooms, amenities, etc
- Host services: communication, response time, etc
- availability
- Features of the listing itself: title, description
- review scores: overall and on different categories 



### Models
#### Stage 1. Predict listing price with basic listing features (location, room type, size, listing text) 
- 
- Random forest
- Gradient Boosting regression

##### Stage 2. Predict listing availability with 
- CountVectorizer / TfidfVectorizer + regression models

3. Understand how the review texts are related to the review scores
- CountVectorizer / TfidfVectorizer + regression models
- Sentiment analysis of reviews + regression

### Model selection
1. performance metrics: mse, R2
2. grid search
