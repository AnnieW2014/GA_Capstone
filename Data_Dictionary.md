
# Income optmizer for Airbnb Hosts  

### Data Dictionary

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