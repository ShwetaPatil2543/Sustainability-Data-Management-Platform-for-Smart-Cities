"""AQI computation utilities (CPCB-style breakpoints and linear interpolation).

Provides compute_aqi that returns sub-indices and overall AQI + category.
"""

from typing import Dict, Tuple, Optional, List


# Breakpoint tables (approximate CPCB 24-hr breakpoints)
BP = {
    'pm25': [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 350, 401, 450),
        (351, 500, 451, 500),
    ],
    'pm10': [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (431, 500, 401, 500),
    ],
    'no2': [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, 500, 401, 500),
    ],
    'so2': [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 380, 101, 200),
        (381, 800, 201, 300),
        (801, 1600, 301, 400),
        (1601, 2040, 401, 500),
    ],
    'co': [
        # CO breakpoints in mg/m3 (approximate)
        (0.0, 1.0, 0, 50),
        (1.1, 2.0, 51, 100),
        (2.1, 10.0, 101, 200),
        (10.1, 17.0, 201, 300),
        (17.1, 34.0, 301, 400),
        (34.1, 50.0, 401, 500),
    ],
}


def _interpolate(C: float, BP_low: float, BP_high: float, I_low: float, I_high: float) -> float:
    if BP_high == BP_low:
        return I_high
    return ((I_high - I_low) / (BP_high - BP_low)) * (C - BP_low) + I_low


def _find_breakpoint(pollutant: str, C: float) -> Optional[Tuple[float, float, float, float]]:
    table = BP.get(pollutant.lower())
    if not table:
        return None
    for (bp_low, bp_high, i_low, i_high) in table:
        if bp_low <= C <= bp_high:
            return (bp_low, bp_high, i_low, i_high)
    # if above highest breakpoint, return last interval for extrapolation
    return table[-1]


def compute_subindex(pollutant: str, value: float) -> Optional[float]:
    if value is None:
        return None
    bp = _find_breakpoint(pollutant, value)
    if not bp:
        return None
    bp_low, bp_high, i_low, i_high = bp
    return round(_interpolate(value, bp_low, bp_high, i_low, i_high))


def category_from_aqi(aqi: int) -> str:
    if aqi <= 50:
        return 'Good'
    if aqi <= 100:
        return 'Satisfactory'
    if aqi <= 200:
        return 'Moderate'
    if aqi <= 300:
        return 'Poor'
    if aqi <= 400:
        return 'Very Poor'
    return 'Severe'


def compute_aqi(reading: Dict[str, float]) -> Dict[str, object]:
    """Compute AQI for a single reading dict with keys: pm25, pm10, no2, so2, co

    Returns: {
      'sub_indices': { 'pm25': int, ... },
      'aqi': int,
      'dominant_pollutant': str,
      'category': str
    }
    """
    sub = {}
    for p in ['pm25', 'pm10', 'no2', 'so2', 'co']:
        v = reading.get(p)
        try:
            if v is None:
                sub[p] = None
            else:
                sub[p] = compute_subindex(p, float(v))
        except Exception:
            sub[p] = None

    # AQI is max of available sub-indices
    available = {k: v for k, v in sub.items() if v is not None}
    if not available:
        return {'sub_indices': sub, 'aqi': None, 'dominant_pollutant': None, 'category': None}

    dominant = max(available.items(), key=lambda x: x[1])
    aqi_val = dominant[1]
    cat = category_from_aqi(aqi_val)
    return {'sub_indices': sub, 'aqi': int(aqi_val), 'dominant_pollutant': dominant[0], 'category': cat}


def compute_bulk(readings: List[Dict[str, float]]) -> List[Dict[str, object]]:
    return [compute_aqi(r) for r in readings]
