# agents/forecaster.py
from typing import List, Dict, Any
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

# 🧠 Predict next week's churn or cycle time
def forecast_next_week(churn_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Takes churn history (list of {week_start, total_churn}) and returns forecast for next week.
    """
    if len(churn_history) < 2:
        return {"forecast": "Not enough data to forecast."}

    # Convert weekly churn data into regression-ready format
    dates = [datetime.datetime.strptime(week['week_start'], "%Y-%m-%d") for week in churn_history]
    X = np.array([(d - dates[0]).days for d in dates]).reshape(-1, 1)  # days since first week
    y = np.array([week['total_churn'] for week in churn_history])

    # Train linear model
    model = LinearRegression().fit(X, y)
    next_week = np.array([[X[-1][0] + 7]])
    forecast = model.predict(next_week)[0]

    return {
        "forecast_week": (dates[-1] + datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
        "forecast_churn": round(forecast, 2)
    }
