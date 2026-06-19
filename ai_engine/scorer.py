from .analyzer import DataAnalyzer
from .predictor import SustainabilityPredictor
from datetime import datetime, timedelta

class SustainabilityScorer:
    """Calculate sustainability scores based on various metrics"""

    def __init__(self):
        self.analyzer = DataAnalyzer()
        self.predictor = SustainabilityPredictor()

    def calculate_energy_score(self, insights):
        """Calculate energy efficiency score (0-100)"""
        if 'energy' not in insights:
            return 50  # Neutral score if no data

        energy = insights['energy']
        score = 100

        # Penalize high electricity consumption
        avg_electricity = energy.get('avg_electricity', 0)
        if avg_electricity > 2000:
            score -= 40
        elif avg_electricity > 1500:
            score -= 25
        elif avg_electricity > 1000:
            score -= 15

        # Reward renewable energy usage
        renewable_ratio = energy.get('renewable_ratio', 0)
        if renewable_ratio > 0.8:
            score += 20
        elif renewable_ratio > 0.6:
            score += 15
        elif renewable_ratio > 0.4:
            score += 10
        elif renewable_ratio > 0.2:
            score += 5

        # Check for problems
        problems = energy.get('problems', [])
        if 'high_energy_consumption' in problems:
            score -= 20
        if 'low_renewable_usage' in problems:
            score -= 15

        return max(0, min(100, score))

    def calculate_fuel_score(self, insights):
        """Calculate fuel efficiency score (0-100)"""
        if 'fuel' not in insights:
            return 50

        fuel = insights['fuel']
        score = 100

        # Penalize high fuel consumption
        total_quantity = fuel.get('total_quantity', 0)
        if total_quantity > 50000:
            score -= 40
        elif total_quantity > 25000:
            score -= 25
        elif total_quantity > 10000:
            score -= 15

        # Penalize dirty fuel usage
        fuel_types = fuel.get('fuel_types', [])
        dirty_fuels = ['Coal', 'Diesel']
        clean_fuels = ['Natural Gas', 'Electricity', 'Solar']

        dirty_count = sum(1 for fuel in fuel_types if fuel in dirty_fuels)
        clean_count = sum(1 for fuel in fuel_types if fuel in clean_fuels)

        if dirty_count > 0:
            score -= dirty_count * 15
        if clean_count > 0:
            score += clean_count * 10

        # Check for problems
        problems = fuel.get('problems', [])
        if 'high_fuel_consumption' in problems:
            score -= 20
        if 'dirty_fuel_usage' in problems:
            score -= 25

        return max(0, min(100, score))

    def calculate_air_quality_score(self, insights):
        """Calculate air quality score (0-100)"""
        if 'air_quality' not in insights:
            return 50

        air = insights['air_quality']
        score = 100

        # Penalize poor air quality
        avg_aqi = air.get('avg_aqi', 0)
        if avg_aqi > 300:
            score -= 50
        elif avg_aqi > 200:
            score -= 40
        elif avg_aqi > 150:
            score -= 30
        elif avg_aqi > 100:
            score -= 20
        elif avg_aqi > 50:
            score -= 10

        # Penalize high pollutant levels
        avg_co2 = air.get('avg_co2', 0)
        if avg_co2 > 1500:
            score -= 25
        elif avg_co2 > 1000:
            score -= 15

        avg_pm25 = air.get('avg_pm25', 0)
        if avg_pm25 > 50:
            score -= 20
        elif avg_pm25 > 35:
            score -= 15
        elif avg_pm25 > 25:
            score -= 10

        # Check for problems
        problems = air.get('problems', [])
        if 'poor_air_quality' in problems:
            score -= 20
        if 'high_co2_levels' in problems:
            score -= 15
        if 'high_pm25' in problems:
            score -= 10

        return max(0, min(100, score))

    def calculate_carbon_score(self, insights):
        """Calculate carbon emission score (0-100)"""
        # This would need carbon emission data
        # For now, return neutral score
        return 50

    def calculate_overall_score(self, days=30):
        """Calculate overall sustainability score"""
        insights = self.analyzer.get_all_insights(days)

        energy_score = self.calculate_energy_score(insights)
        fuel_score = self.calculate_fuel_score(insights)
        air_score = self.calculate_air_quality_score(insights)
        carbon_score = self.calculate_carbon_score(insights)

        # Weighted average (can be adjusted based on importance)
        weights = {
            'energy': 0.3,
            'fuel': 0.25,
            'air_quality': 0.25,
            'carbon': 0.2
        }

        overall_score = (
            energy_score * weights['energy'] +
            fuel_score * weights['fuel'] +
            air_score * weights['air_quality'] +
            carbon_score * weights['carbon']
        )

        # Get score category
        if overall_score >= 80:
            category = "Excellent"
            color = "green"
        elif overall_score >= 60:
            category = "Good"
            color = "blue"
        elif overall_score >= 40:
            category = "Moderate"
            color = "yellow"
        else:
            category = "High Risk"
            color = "red"

        return {
            'overall_score': round(overall_score, 1),
            'category': category,
            'color': color,
            'breakdown': {
                'energy': {
                    'score': energy_score,
                    'weight': weights['energy']
                },
                'fuel': {
                    'score': fuel_score,
                    'weight': weights['fuel']
                },
                'air_quality': {
                    'score': air_score,
                    'weight': weights['air_quality']
                },
                'carbon': {
                    'score': carbon_score,
                    'weight': weights['carbon']
                }
            },
            'insights': insights
        }

    def get_score_interpretation(self, score):
        """Get detailed interpretation of the score"""
        if score >= 80:
            return {
                'level': 'Excellent',
                'description': 'Your facility demonstrates outstanding sustainability practices with minimal environmental impact.',
                'recommendations': [
                    'Maintain current excellent practices',
                    'Consider sharing best practices with other facilities',
                    'Explore advanced green technologies'
                ]
            }
        elif score >= 60:
            return {
                'level': 'Good',
                'description': 'Your facility has good sustainability practices but there are opportunities for improvement.',
                'recommendations': [
                    'Focus on areas with lower scores',
                    'Implement energy efficiency measures',
                    'Consider renewable energy sources'
                ]
            }
        elif score >= 40:
            return {
                'level': 'Moderate',
                'description': 'Your facility needs significant improvements in sustainability practices.',
                'recommendations': [
                    'Conduct comprehensive energy audit',
                    'Switch to cleaner fuel alternatives',
                    'Implement air quality monitoring systems',
                    'Develop sustainability action plan'
                ]
            }
        else:
            return {
                'level': 'High Risk',
                'description': 'Your facility has serious environmental impact that requires immediate attention.',
                'recommendations': [
                    'Immediate implementation of pollution control measures',
                    'Complete transition to renewable energy',
                    'Install advanced emission control systems',
                    'Seek environmental consulting services',
                    'Develop comprehensive sustainability strategy'
                ]
            }

    def get_improvement_plan(self, score_data):
        """Generate detailed improvement plan based on scores"""
        plan = {
            'priority_actions': [],
            'medium_term_goals': [],
            'long_term_vision': [],
            'estimated_timeline': '6-12 months',
            'potential_savings': {}
        }

        breakdown = score_data['breakdown']

        # Energy improvement actions
        if breakdown['energy']['score'] < 70:
            plan['priority_actions'].extend([
                'Install LED lighting systems',
                'Implement smart energy monitoring',
                'Conduct energy audit'
            ])
            plan['potential_savings']['energy'] = '15-30% cost reduction'

        # Fuel improvement actions
        if breakdown['fuel']['score'] < 70:
            plan['priority_actions'].extend([
                'Switch to cleaner fuel alternatives',
                'Optimize fuel usage patterns',
                'Implement fuel efficiency programs'
            ])
            plan['potential_savings']['fuel'] = '20-40% cost reduction'

        # Air quality improvement actions
        if breakdown['air_quality']['score'] < 70:
            plan['priority_actions'].extend([
                'Install air filtration systems',
                'Implement emission control technologies',
                'Regular air quality monitoring'
            ])

        return plan


# ---------------------------
# Simple alert classification helpers
# ---------------------------
def classify_metric(value: float, warning_threshold: float, critical_threshold: float) -> str:
    """Classify a numeric metric into Safe / Warning / Critical.

    - Safe: value <= warning_threshold
    - Warning: warning_threshold < value <= critical_threshold
    - Critical: value > critical_threshold
    """
    try:
        val = float(value)
    except Exception:
        return 'Safe'

    if val <= warning_threshold:
        return 'Safe'
    if val <= critical_threshold:
        return 'Warning'
    return 'Critical'


def classify_alerts(emission: float = None, aqi: float = None, energy: float = None, thresholds: dict = None) -> dict:
    """Return alert classifications for emission, aqi and energy using provided thresholds.

    thresholds default values are tuned for general facility-level monitoring.
    """
    defaults = {
        'emission': {'warning': 1000.0, 'critical': 5000.0},
        'aqi': {'warning': 100.0, 'critical': 200.0},
        'energy': {'warning': 2000.0, 'critical': 5000.0},
    }
    if thresholds:
        for k in defaults:
            if k in thresholds:
                defaults[k].update(thresholds[k])

    result = {}

    if emission is not None:
        level = classify_metric(emission, defaults['emission']['warning'], defaults['emission']['critical'])
        result['emission'] = {
            'level': level,
            'value': emission,
            'thresholds': defaults['emission']
        }

    if aqi is not None:
        level = classify_metric(aqi, defaults['aqi']['warning'], defaults['aqi']['critical'])
        result['aqi'] = {
            'level': level,
            'value': aqi,
            'thresholds': defaults['aqi']
        }

    if energy is not None:
        level = classify_metric(energy, defaults['energy']['warning'], defaults['energy']['critical'])
        result['energy'] = {
            'level': level,
            'value': energy,
            'thresholds': defaults['energy']
        }

    return result