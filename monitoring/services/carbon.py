"""IPCC Tier-1 style carbon emission calculations.

Provides functions to compute emissions (CO2, CH4, N2O) and CO2-equivalent using EF and GWP.
"""

from typing import Dict, Tuple, List
from importlib import import_module


# Example emission factor table (Tier-1 defaults / placeholders). Units:
# - diesel: liters -> EF in kg gas per liter
# - coal: tonnes -> EF in kg gas per tonne
# - electricity: kWh -> EF in kg gas per kWh
EMISSION_FACTORS = {
    'diesel': {
        'unit': 'liter',
        'CO2': 2.68,   # kg CO2 / liter
        'CH4': 0.003,  # kg CH4 / liter
        'N2O': 0.0005, # kg N2O / liter
    },
    'coal': {
        'unit': 'tonne',
        'CO2': 2410.0,  # kg CO2 / tonne (approximate)
        'CH4': 0.1,     # kg CH4 / tonne
        'N2O': 0.01,    # kg N2O / tonne
    },
    'electricity': {
        'unit': 'kwh',
        'CO2': 0.5,     # kg CO2 / kWh (grid-average placeholder)
        'CH4': 0.0001,
        'N2O': 0.00002,
    },
}

# Global Warming Potentials (100-year, IPCC AR5-like approximations)
GWP = {
    'CO2': 1,
    'CH4': 28,
    'N2O': 265,
}


def compute_from_activity(fuel_type: str, activity: float) -> Dict[str, float]:
    """Compute gas emissions and CO2e for given fuel/activity.

    fuel_type: 'diesel'|'coal'|'electricity'
    activity: numeric activity data in units defined by EMISSION_FACTORS[fuel_type]['unit']

    Returns dict: { 'CO2': kg, 'CH4': kg, 'N2O': kg, 'CO2e': kg }
    """
    ft = fuel_type.lower()

    # Try to load emission factor overrides from DB (if Django is available)
    try:
        models_mod = import_module('monitoring.models')
        EmissionFactor = getattr(models_mod, 'EmissionFactor')
        try:
            ef_obj = EmissionFactor.objects.filter(fuel_type__iexact=ft).first()
        except Exception:
            ef_obj = None
        if ef_obj:
            ef = {
                'unit': ef_obj.unit,
                'CO2': ef_obj.co2_kg_per_unit,
                'CH4': ef_obj.ch4_kg_per_unit,
                'N2O': ef_obj.n2o_kg_per_unit,
            }
        else:
            ef = EMISSION_FACTORS.get(ft)
    except Exception:
        ef = EMISSION_FACTORS.get(ft)

    if ef is None:
        raise KeyError(f"Unknown fuel_type: {fuel_type}")
    if activity is None:
        raise ValueError("activity is required")

    # ef now holds the emission factor dict from DB or defaults
    co2 = (ef.get('CO2') or 0) * activity
    ch4 = (ef.get('CH4') or 0) * activity
    n2o = (ef.get('N2O') or 0) * activity

    co2e = (co2 * GWP['CO2']) + (ch4 * GWP['CH4']) + (n2o * GWP['N2O'])

    return {
        'CO2': round(co2, 6),
        'CH4': round(ch4, 6),
        'N2O': round(n2o, 6),
        'CO2e': round(co2e, 6),
    }


def compute_bulk(items: List[Dict]) -> List[Dict]:
    """Compute emissions for a list of items. Each item should include 'fuel_type' and 'activity'.
    Returns list of dicts with computation results preserved.
    """
    out = []
    for it in items:
        try:
            res = compute_from_activity(it.get('fuel_type'), float(it.get('activity')))
            out.append({**it, 'computed': res})
        except Exception as e:
            out.append({**it, 'error': str(e)})
    return out
