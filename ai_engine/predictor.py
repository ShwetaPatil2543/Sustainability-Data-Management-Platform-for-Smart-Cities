import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
from typing import List, Dict, Any

warnings.filterwarnings('ignore')

from django.db.models import Sum

from energy.models import EnergyUsage
from fuel.models import FuelConsumption
from emissions.models import CarbonEmission


def _make_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_year'] = df['date'].dt.dayofyear
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['lag_1'] = df['value'].shift(1)
    df['lag_7'] = df['value'].shift(7)
    df = df.dropna()
    return df


def _train_and_predict(df: pd.DataFrame, days: int = 7) -> List[Dict[str, Any]]:
    if df is None or len(df) < 10:
        today = datetime.now().date()
        mean_val = float(df['value'].mean()) if (df is not None and not df.empty) else 0.0
        return [
            {'date': (today + timedelta(days=i + 1)).isoformat(), 'prediction': round(mean_val, 2)}
            for i in range(days)
        ]

    X_df = _make_features(df)
    features = ['day_of_year', 'month', 'year', 'lag_1', 'lag_7']
    X = X_df[features].values
    y = X_df['value'].values

    try:
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(X, y)
    except Exception:
        # If sklearn is not available or import is slow, fallback to rolling mean predictor
        mean_val = float(np.mean(y)) if len(y) else 0.0
        today = datetime.now().date()
        return [
            {'date': (today + timedelta(days=i + 1)).isoformat(), 'prediction': round(mean_val, 2)}
            for i in range(days)
        ]

    last = X_df.iloc[-1]
    lag_1 = last['value']
    lag_7 = last['lag_7'] if 'lag_7' in last else last['value']
    base_date = X_df['date'].iloc[-1].date()

    preds: List[Dict[str, Any]] = []
    for i in range(days):
        pred_date = base_date + timedelta(days=i + 1)
        row = np.array([
            pred_date.timetuple().tm_yday,
            pred_date.month,
            pred_date.year,
            lag_1,
            lag_7,
        ]).reshape(1, -1)
        pred = float(model.predict(row)[0])
        preds.append({'date': pred_date.isoformat(), 'prediction': round(pred, 2)})
        lag_7 = lag_1
        lag_1 = pred

    return preds


class SustainabilityPredictor:
    """LinearRegression-based predictors for carbon, energy and fuel usage."""

    def predict_carbon_emissions(self, days: int = 7) -> List[Dict[str, Any]]:
        qs = (
            CarbonEmission.objects
            .values('date')
            .annotate(co2_sum=Sum('co2_emission'), methane_sum=Sum('methane_emission'), nitro_sum=Sum('nitrous_oxide'))
            .order_by('date')
        )
        if not qs:
            return []

        rows = []
        for r in qs:
            total = (r.get('co2_sum') or 0) + (r.get('methane_sum') or 0) + (r.get('nitro_sum') or 0)
            rows.append({'date': r['date'], 'value': float(total)})

        df = pd.DataFrame(rows)
        return _train_and_predict(df, days)

    def predict_energy_consumption(self, days: int = 7) -> List[Dict[str, Any]]:
        qs = (
            EnergyUsage.objects
            .values('date')
            .annotate(total=Sum('total_energy'))
            .order_by('date')
        )
        if not qs:
            return []

        rows = [{'date': r['date'], 'value': float(r.get('total') or 0.0)} for r in qs]
        df = pd.DataFrame(rows)
        return _train_and_predict(df, days)

    def predict_fuel_usage(self, days: int = 7) -> List[Dict[str, Any]]:
        qs = (
            FuelConsumption.objects
            .values('date')
            .annotate(total_qty=Sum('quantity'))
            .order_by('date')
        )
        if not qs:
            return []

        rows = [{'date': r['date'], 'value': float(r.get('total_qty') or 0.0)} for r in qs]
        df = pd.DataFrame(rows)
        return _train_and_predict(df, days)

    def get_predictions(self, days: int = 7) -> Dict[str, Any]:
        return {
            'carbon_emissions': self.predict_carbon_emissions(days),
            'energy_consumption': self.predict_energy_consumption(days),
            'fuel_usage': self.predict_fuel_usage(days),
        }
