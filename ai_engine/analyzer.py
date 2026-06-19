from energy.models import EnergyUsage
from fuel.models import FuelConsumption
from air_quality.models import AirQuality
from django.db.models import Avg, Sum
from datetime import datetime, timedelta

class DataAnalyzer:
    def __init__(self):
        self.insights = {}

    def analyze_energy_usage(self, days=30):
        """Analyze energy usage data for the last N days"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        energy_data = EnergyUsage.objects.filter(date__range=[start_date, end_date])

        if not energy_data.exists():
            return {"status": "no_data", "message": "No energy usage data available"}

        avg_electricity = energy_data.aggregate(avg=Avg('electricity_consumption'))['avg'] or 0
        total_energy = energy_data.aggregate(total=Sum('total_energy'))['total'] or 0
        renewable_ratio = energy_data.aggregate(avg=Avg('renewable_energy'))['avg'] or 0

        problems = []
        if avg_electricity > 1000:  # Threshold for high consumption
            problems.append("high_energy_consumption")
        if renewable_ratio < 0.3:  # Less than 30% renewable
            problems.append("low_renewable_usage")

        self.insights['energy'] = {
            'avg_electricity': avg_electricity,
            'total_energy': total_energy,
            'renewable_ratio': renewable_ratio,
            'problems': problems
        }

        return self.insights['energy']

    def analyze_fuel_consumption(self, days=30):
        """Analyze fuel consumption data"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        fuel_data = FuelConsumption.objects.filter(date__range=[start_date, end_date])

        if not fuel_data.exists():
            return {"status": "no_data", "message": "No fuel consumption data available"}

        total_quantity = fuel_data.aggregate(total=Sum('quantity'))['total'] or 0
        total_emissions = fuel_data.aggregate(total=Sum('total_emission'))['total'] or 0
        fuel_types = fuel_data.values_list('fuel_type', flat=True).distinct()

        problems = []
        if total_quantity > 10000:  # Arbitrary threshold
            problems.append("high_fuel_consumption")
        if 'Coal' in fuel_types or 'Diesel' in fuel_types:
            problems.append("dirty_fuel_usage")

        self.insights['fuel'] = {
            'total_quantity': total_quantity,
            'total_emissions': total_emissions,
            'fuel_types': list(fuel_types),
            'problems': problems
        }

        return self.insights['fuel']

    def analyze_air_quality(self, days=30):
        """Analyze air quality data"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        air_data = AirQuality.objects.filter(date__range=[start_date, end_date])

        if not air_data.exists():
            return {"status": "no_data", "message": "No air quality data available"}

        avg_aqi = air_data.aggregate(avg=Avg('aqi'))['avg'] or 0
        avg_co2 = air_data.aggregate(avg=Avg('co2'))['avg'] or 0
        avg_pm25 = air_data.aggregate(avg=Avg('pm25'))['avg'] or 0

        problems = []
        if avg_aqi > 150:  # Poor air quality
            problems.append("poor_air_quality")
        if avg_co2 > 1000:  # High CO2
            problems.append("high_co2_levels")
        if avg_pm25 > 35:  # High PM2.5
            problems.append("high_pm25")

        self.insights['air_quality'] = {
            'avg_aqi': avg_aqi,
            'avg_co2': avg_co2,
            'avg_pm25': avg_pm25,
            'problems': problems
        }

        return self.insights['air_quality']

    def get_all_insights(self, days=30):
        """Get comprehensive analysis"""
        self.analyze_energy_usage(days)
        self.analyze_fuel_consumption(days)
        self.analyze_air_quality(days)
        return self.insights