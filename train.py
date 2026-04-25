import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import xgboost as xgb


def train_model(file_path, name):

    df = pd.read_excel(file_path)

    # تنظيف
    df["area"] = df["area"].apply(lambda x: x if x > 0 else 1)
    df["price"] = df["price"].apply(lambda x: x if x > 0 else 1)

    # log
    df["log_area"] = np.log(df["area"])
    df["log_price"] = np.log(df["price"])

    # بحر
    df["distance_to_sea"] = df.get("distance_to_sea", 0).fillna(0)

    # rent
    rent_map = {"Monthly": 1, "6 Months": 6, "Yearly": 12}
    if "rent_period" in df.columns:
        df["rent_period_num"] = df["rent_period"].map(rent_map).fillna(0)
    else:
        df["rent_period_num"] = 0

    # features
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

    # encoding
    X = pd.get_dummies(X)

    # تنظيف
    X = X.replace([np.inf, -np.inf], np.nan)
    mask = X.notna().all(axis=1)

    X = X[mask]
    y = y[mask]

    # split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # model
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

    # 💾 حفظ النموذج + الأعمدة (🔥 أهم تعديل)
    safe = name.replace(" ", "_")

    joblib.dump(model, f"model_{safe.lower()}.pkl")
    joblib.dump(X.columns, f"{safe}_columns.pkl")


# تشغيل كل النماذج
train_model("Apartment_rent.xlsx", "Apartment Rent")
train_model("Apartment_sale.xlsx", "Apartment Sale")
train_model("House_rent.xlsx", "House Rent")
train_model("House_sale.xlsx", "House Sale")
train_model("Land_rent.xlsx", "Land Rent")
train_model("Land_sale.xlsx", "Land Sale")
