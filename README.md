# Bengaluru Real Estate Price Prediction

A simple end-to-end app that estimates prices for residential properties in Bengaluru. It trains a regression model on a cleaned Kaggle housing dataset, serves predictions through a Python Flask API, and includes a minimal web page where users enter square footage, BHK, bathrooms, and location to get an instant estimate.

---

## Overview

This project walks from raw data to a usable prediction tool:
- Clean and prepare the Bengaluru housing dataset
- Train and validate a regression model with scikit-learn
- Save model artifacts for reliable inference
- Serve predictions via a lightweight Flask API
- Call the API from a small HTML, CSS, and JavaScript front end

---

## Dataset

**Source:** Bengaluru House Price dataset on Kaggle  
**Features:** `area_type`, `availability`, `location`, `size`, `total_sqft`, `bath`, `balcony`, `price`  
The raw data includes many unique neighborhoods and some messy entries, such as inconsistent location names, non numeric values in `total_sqft`, and missing values in fields like `society` and `balcony`.  
**Target:** `price` (sale price)

---

## Data Cleaning and Preparation

- Standardized location strings and trimmed whitespace
- Parsed `total_sqft` to numeric values, handling ranges and non standard formats
- Derived `BHK` from the `size` field when needed
- Computed `price_per_sqft` to capture neighborhood level variation
- Removed unusable records after inspecting missing fields

---

## Outlier Detection and Removal

Outliers vary by neighborhood, so a single global cutoff is not ideal. I filtered out extreme values using `price_per_sqft` within each location, and dropped entries with unrealistic room to area ratios, such as tiny homes claiming very high BHK counts. This improved validation stability and reduced variance.

---

## Feature Engineering

- Kept numeric features: `total_sqft`, `bath`, `bhk`
- One hot encoded `location` to capture neighborhood effects
- Grouped very rare locations into an `other` bucket to control dimensionality without losing signal

---

## Modeling Approach

I started with `LinearRegression` from scikit-learn as an interpretable baseline, then evaluated regularized models such as `Ridge` and `Lasso`. Hyperparameters were tuned with `GridSearchCV`. The final choice balances bias and variance while keeping the pipeline simple to serve.

---

## Training and Validation

- Split the dataset into train and test sets
- Used K-Fold cross validation to estimate generalization error
- Monitored `R²` and `RMSE` on validation folds and on the held out test set
- Saved model artifacts after training, including the fitted estimator and the exact feature column order, to ensure inference uses the same preprocessing as training

---

## How Predictions Are Served

A lightweight Flask service loads the saved model and column metadata once at startup. The API accepts `location`, `total_sqft`, `bhk`, and `bath`, transforms them into the training feature vector, and returns a predicted price. The UI is a small HTML, CSS, and JavaScript page that calls this API and displays the estimate.
