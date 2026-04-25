import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import xgboost as xgb


def train_model(file_path, name):

    df = pd.read_excel(file_path)

    # 🧹 تنظيف
    df["area"] = df["area"].apply(lambda x: x if x > 0 else 1)
    df["price"] = df["price"].apply(lambda x: x if x > 0 else 1)

    # 📊 log
    df["log_area"] = np.log(df["area"])
    df["log_price"] = np.log(df["price"])

    # 🌊 distance to sea
    if "distance_to_sea" in df.columns:
        df["distance_to_sea"] = df["distance_to_sea"].fillna(0)
    else:
        df["distance_to_sea"] = 0

    # 🏠 rent period
    rent_map = {
        "Monthly": 1,
        "6 Months": 6,
        "Yearly": 12
    }

    if "rent_period" in df.columns:
        df["rent_period_num"] = df["rent_period"].map(rent_map)
        df["rent_period_num"] = df["rent_period_num"].fillna(0)
    else:
        df["rent_period_num"] = 0

    # 🎯 features
    features = ["log_area", "city"]

    extra = [
        "beds",
        "livings",
        "wc",
        "street_width",
        "furnished",
        "distance_to_sea",
        "rent_period_num"
    ]

    for col in extra:
        if col in df.columns:
            df[col] = df[col].fillna(0)
            features.append(col)

    X = df[features]
    y = df["log_price"]

    # 🔥 encoding
    X = pd.get_dummies(X)

    # 🧹 تنظيف
    X = X.replace([np.inf, -np.inf], np.nan)
    mask = X.notna().all(axis=1)

    X = X[mask]
    y = y[mask]

    # ✂️ split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 🚀 model
    model = xgb.XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    r2 = r2_score(y_test, pred)
    print(name, "R2 =", r2)

    return model


# 🏠 تشغيل
model_ar = train_model("Apartment_rent.xlsx", "Apartment Rent")
model_as = train_model("Apartment_sale.xlsx", "Apartment Sale")

model_hr = train_model("House_rent.xlsx", "House Rent")
model_hs = train_model("House_sale.xlsx", "House Sale")

model_lr = train_model("Land_rent.xlsx", "Land Rent")
model_ls = train_model("Land_sale.xlsx", "Land Sale")


# 💾 حفظ
joblib.dump(model_ar, "model_apartment_rent.pkl")
joblib.dump(model_as, "model_apartment_sale.pkl")

joblib.dump(model_hr, "model_house_rent.pkl")
joblib.dump(model_hs, "model_house_sale.pkl")

joblib.dump(model_lr, "model_land_rent.pkl")
joblib.dump(model_ls, "model_land_sale.pkl")
