Bengaluru Real Estate Price Prediction
Overview
This project builds an end to end price prediction application for residential properties in Bengaluru. It trains a regression model on a cleaned Kaggle housing dataset, serves predictions through a Python Flask API, and provides a simple web page where users can enter square footage, BHK, bathrooms, and location to get an instant estimate.

Dataset
I used the Bengaluru House Price dataset from Kaggle. It includes features such as area_type, availability, location, size, total_sqft, bath, balcony, and price. The raw data contains many unique neighborhoods and several messy entries, for example inconsistent location names, non numeric values in total_sqft, and missing values in fields like society and balcony. The target variable is the sale price.

Data Cleaning and Preparation
Standardized location strings and trimmed whitespace

Parsed total_sqft to numeric values, handling ranges and non-standard formats

Derived BHK from the size field when needed

Built price_per_sqft to help understand neighborhood level variation

Removed unusable records after careful inspection of missing fields

Outlier Detection and Removal
Outliers vary by neighborhood, so a single global cutoff is not ideal. I removed extreme values using price_per_sqft within each location, and filtered entries with unrealistic room to area ratios, for example tiny homes claiming high BHK counts. This step improved validation stability and reduced variance.

Feature Engineering
Kept numeric features: total_sqft, bath, bhk

One hot encoded location to capture neighborhood effects

Grouped very rare locations into an other bucket to control dimensionality without losing signal

Modeling Approach
I started with scikit learn LinearRegression as a strong, interpretable baseline. I also evaluated regularized models such as Ridge and Lasso. Hyperparameters were tuned using GridSearchCV. The final choice balanced bias and variance and kept the pipeline simple to serve.

Training and Validation
Split the dataset into train and test sets

Used K Fold cross validation to estimate generalization error

Monitored metrics such as R² and RMSE on the validation folds and on the held out test set

Saved model artifacts after training, including the fitted estimator and the exact feature column order, to guarantee that inference uses the same preprocessing as training

How Predictions Are Served
A lightweight Flask service loads the saved model and column metadata once at startup. The API accepts user inputs for location, square footage, BHK, and bathrooms, transforms them into the feature vector used during training, and returns a predicted price. The UI is a minimal HTML, CSS, and JavaScript page that calls this API and displays the estimate.

What to Expect from the Model
Predictions are estimates based on historical data and engineered features. They reflect typical market patterns at the neighborhood level rather than exact quotes for any specific property. The goal is to provide a fast, transparent baseline that is easy to understand and extend.

Possible Extensions
Compare additional models such as Random Forest or Gradient Boosting

Add richer geospatial features or external signals like proximity to transit or schools

Track experiments and model versions, and add simple monitoring for prediction drift

