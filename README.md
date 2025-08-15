# Bengaluru Real Estate Price Prediction

Predict apartment prices in Bengaluru from a clean web UI backed by a scikit-learn model and a Flask API.

- Live site: https://bhprediction.netlify.app/
- Dataset: [Bengaluru House Price Data (Kaggle)](https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data?resource=download)

---

## What this app does

You enter area in square feet, BHK, bathrooms, and location. The browser calls a Flask API that loads a trained regression model and returns an estimated price. The front end is a simple HTML, CSS, and JavaScript page with radio toggles for BHK and Bath, a text input for square feet, and a location dropdown, plus a button that triggers estimation. 

---

## About the data

**Source**  
Bengaluru housing listings with columns like `area_type`, `availability`, `location`, `size`, `society`, `total_sqft`, `bath`, `balcony`, and `price`. The target is `price`.

**Context and mix**  
For buyers, the critical question is price, but it is shaped by location, size, and amenities. The dataset reflects Bengaluru’s market patterns and the complexity of pricing decisions in a large, fast-growing city. The mix is dominated by apartments, with many neighborhoods and a long tail of locations. Example distributions seen in the dataset: Super built-up area about two-thirds, Built-up area around one-fifth, Ready to move listings are the majority, 2 BHK and 3 BHK are the most common configurations, and localities like Whitefield and Sarjapur Road appear frequently among thousands of other locations.

---

## Data cleaning

1. **Standardized text fields**  
   Normalized `location` strings and trimmed whitespace.
2. **Parsed square footage**  
   Converted `total_sqft` to numeric, handling ranges and non-standard entries.
3. **Derived features**  
   Extracted `bhk` from the `size` text field when needed.
4. **Price per square foot**  
   Computed `price_per_sqft` to analyze neighborhood-level variation and to assist with outlier detection.
5. **Removed unusable rows**  
   Dropped rows with irrecoverable values after inspecting fields like `society`, `balcony`, and malformed `total_sqft`.

---

## Outlier handling

A single global cutoff is not ideal since neighborhoods differ. I filtered outliers using `price_per_sqft` within each location, and removed records with unrealistic room to area ratios, for example tiny homes marked with very high BHK counts. This stabilized validation and reduced variance.

---

## Feature selection and encoding

- Kept numeric features: `total_sqft`, `bath`, `bhk`
- One hot encoded `location` to capture neighborhood effects
- Grouped very rare locations into an `other` bucket to keep the feature space compact without losing signal

---

## Modeling

Started with an interpretable baseline using `LinearRegression`, then evaluated regularized models like Ridge and Lasso. Hyperparameters were tuned with `GridSearchCV`. The final model choice balanced bias and variance while keeping the pipeline simple to serve in production.

---

## Training and validation

- Train and test split to measure generalization
- K-fold cross-validation to reduce variance in estimates
- Tracked `R²` and `RMSE` on folds and a held-out test set
- Saved model artifacts and the exact column order so inference matches training

---

## Serving predictions

A lightweight Flask app loads the saved model at startup, constructs the feature vector from request inputs, and returns the predicted price.

**Key endpoints**

- `GET /get_location_names` returns the list of locations used by the model, which the UI uses to populate the dropdown. :contentReference[oaicite:2]{index=2}  
- `POST /predict_home_price` accepts `total_sqft`, `bhk`, `bath`, and `location`, then returns `{ "estimated_price": <number> }`. The client posts form data to this path and renders the result in the UI. :contentReference[oaicite:3]{index=3}

