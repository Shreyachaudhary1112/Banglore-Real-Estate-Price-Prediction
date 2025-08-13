import os
import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ART_DIR = os.path.join(BASE_DIR, "artifacts")

def load_saved_artifacts():
    global __data_columns, __locations, __model

    # columns.json may be either a dict with key "data_columns" or a raw list
    with open(os.path.join(ART_DIR, "columns.json"), "r") as f:
        cols = json.load(f)
        if isinstance(cols, dict) and "data_columns" in cols:
            __data_columns = cols["data_columns"]
        else:
            __data_columns = cols

    # compute locations as everything except the numeric base features
    base_feats = {"total_sqft", "sqft", "bath", "bhk"}
    __locations = [c for c in __data_columns if c not in base_feats]

    with open(os.path.join(ART_DIR, "banglore_home_prices_model.pickle"), "rb") as f:
        __model = pickle.load(f)

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

def _safe_index(name, default_idx=None):
    try:
        return __data_columns.index(name)
    except ValueError:
        return default_idx

def get_estimated_price(location, sqft, bhk, bath):
    # build feature vector in the order of __data_columns
    x = np.zeros(len(__data_columns))

    # set numeric features wherever they appear, with fallbacks
    idx_sqft = _safe_index("total_sqft", _safe_index("sqft", 0))
    idx_bath = _safe_index("bath", 1 if 1 < len(x) else None)
    idx_bhk  = _safe_index("bhk",  2 if 2 < len(x) else None)

    if idx_sqft is not None: x[idx_sqft] = sqft
    if idx_bath is not None: x[idx_bath] = bath
    if idx_bhk  is not None: x[idx_bhk]  = bhk

    # one hot for location if present
    loc = (location or "").strip().lower()
    try:
        loc_index = __data_columns.index(loc)
        x[loc_index] = 1
    except ValueError:
        pass  # unknown location, leave zeros

    pred = float(__model.predict([x])[0])
    # round to 2 decimals for clean UI
    return round(pred, 2)

if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names()[:5])
