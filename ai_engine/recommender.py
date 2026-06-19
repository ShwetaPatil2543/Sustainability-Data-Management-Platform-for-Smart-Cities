from .analyzer import DataAnalyzer

class Recommender:
    def __init__(self):
        self.analyzer = DataAnalyzer()

    def get_recommendations(self, days=30):
        """Generate recommendations based on data analysis"""
        insights = self.analyzer.get_all_insights(days)
        recommendations = []

        # Energy recommendations
        if 'energy' in insights:
            energy = insights['energy']
            if 'high_energy_consumption' in energy.get('problems', []):
                recommendations.append({
                    "category": "Energy Optimization",
                    "problem": "High electricity consumption detected",
                    "recommendation": "Install solar panels or wind turbines to reduce reliance on grid electricity",
                    "impact": "Reduce energy costs by up to 50% and carbon footprint"
                })
                recommendations.append({
                    "category": "Energy Optimization",
                    "problem": "High electricity consumption detected",
                    "recommendation": "Implement smart energy monitoring systems to identify idle equipment",
                    "impact": "Optimize machine runtime and reduce unnecessary energy usage"
                })

            if 'low_renewable_usage' in energy.get('problems', []):
                recommendations.append({
                    "category": "Renewable Energy",
                    "problem": "Low renewable energy usage",
                    "recommendation": "Increase renewable energy sources to at least 50% of total consumption",
                    "impact": "Lower carbon emissions and improve sustainability rating"
                })

        # Fuel recommendations
        if 'fuel' in insights:
            fuel = insights['fuel']
            if 'high_fuel_consumption' in fuel.get('problems', []):
                recommendations.append({
                    "category": "Fuel Efficiency",
                    "problem": "High fuel consumption detected",
                    "recommendation": "Switch to more efficient machinery or implement fuel optimization programs",
                    "impact": "Reduce fuel costs and emissions"
                })

            if 'dirty_fuel_usage' in fuel.get('problems', []):
                recommendations.append({
                    "category": "Clean Fuel Transition",
                    "problem": "Usage of high-emission fuels like coal or diesel",
                    "recommendation": "Transition to cleaner fuels such as natural gas or electric alternatives",
                    "impact": "Significantly reduce carbon emissions and improve air quality"
                })

        # Air Quality recommendations
        if 'air_quality' in insights:
            air = insights['air_quality']
            if 'poor_air_quality' in air.get('problems', []):
                recommendations.append({
                    "category": "Air Quality Improvement",
                    "problem": "Poor air quality with high AQI",
                    "recommendation": "Install advanced air filtration and ventilation systems",
                    "impact": "Improve workplace air quality and employee health"
                })

            if 'high_co2_levels' in air.get('problems', []):
                recommendations.append({
                    "category": "Emission Control",
                    "problem": "High CO2 levels detected",
                    "recommendation": "Implement carbon capture technologies or improve ventilation",
                    "impact": "Reduce greenhouse gas emissions"
                })

            if 'high_pm25' in air.get('problems', []):
                recommendations.append({
                    "category": "Particulate Control",
                    "problem": "High PM2.5 levels",
                    "recommendation": "Install electrostatic precipitators or baghouse filters",
                    "impact": "Reduce particulate emissions and improve air quality"
                })

        if not recommendations:
            recommendations.append({
                "category": "General",
                "problem": "No major issues detected",
                "recommendation": "Continue monitoring and maintain current sustainability practices",
                "impact": "Ensure ongoing environmental compliance"
            })

        return recommendations

    def get_insights_summary(self, days=30):
        """Get a text summary of insights"""
        insights = self.analyzer.get_all_insights(days)
        summary = []

        if 'energy' in insights:
            energy = insights['energy']
            summary.append(f"Energy: Average consumption {energy.get('avg_electricity', 0):.1f} kWh")
            if energy.get('problems'):
                summary.append(f"Energy issues: {', '.join(energy['problems'])}")

        if 'fuel' in insights:
            fuel = insights['fuel']
            summary.append(f"Fuel: Total consumption {fuel.get('total_quantity', 0):.1f} units")
            if fuel.get('problems'):
                summary.append(f"Fuel issues: {', '.join(fuel['problems'])}")

        if 'air_quality' in insights:
            air = insights['air_quality']
            summary.append(f"Air Quality: Average AQI {air.get('avg_aqi', 0):.1f}")
            if air.get('problems'):
                summary.append(f"Air quality issues: {', '.join(air['problems'])}")

        return " ".join(summary) if summary else "No data available for analysis"


def generate_recommendations_from_alerts(alerts: dict) -> list:
    """Generate short actionable recommendations based on alert levels."""
    recs = []
    if not alerts:
        return [{
            'category': 'General',
            'problem': 'No alerts',
            'recommendation': 'Continue monitoring and maintain current practices',
            'impact': 'Maintain compliance and stability'
        }]

    # Emission recommendations
    em = alerts.get('emission')
    if em:
        if em['level'] == 'Critical':
            recs.append({
                'category': 'Carbon Reduction',
                'problem': 'Critical emissions',
                'recommendation': 'Urgent: engage carbon reduction program, switch to renewables and install carbon capture where feasible',
                'impact': 'Rapid decrease in CO₂-equivalent emissions'
            })
        elif em['level'] == 'Warning':
            recs.append({
                'category': 'Carbon Reduction',
                'problem': 'Elevated emissions',
                'recommendation': 'Audit fuel use, optimize processes and increase renewable sourcing',
                'impact': 'Reduce emissions over next quarter'
            })

    # AQI recommendations
    aq = alerts.get('aqi')
    if aq:
        if aq['level'] == 'Critical':
            recs.append({
                'category': 'Air Quality',
                'problem': 'Hazardous AQI',
                'recommendation': 'Immediate pollution controls, suspend high-emission processes and notify stakeholders',
                'impact': 'Protect worker health and reduce public exposure'
            })
        elif aq['level'] == 'Warning':
            recs.append({
                'category': 'Air Quality',
                'problem': 'High AQI',
                'recommendation': 'Increase filtration/ventilation and monitor pollutant sources',
                'impact': 'Lower particulate and gaseous pollutants'
            })

    # Energy recommendations
    en = alerts.get('energy')
    if en:
        if en['level'] == 'Critical':
            recs.append({
                'category': 'Energy',
                'problem': 'Critical energy consumption',
                'recommendation': 'Immediate demand reduction program, schedule load shedding and accelerate renewable deployment',
                'impact': 'Reduce peak load and costs'
            })
        elif en['level'] == 'Warning':
            recs.append({
                'category': 'Energy',
                'problem': 'High energy use',
                'recommendation': 'Implement efficiency measures and smart controls',
                'impact': 'Lower energy use and costs'
            })

    if not recs:
        recs.append({
            'category': 'General',
            'problem': 'No significant issues',
            'recommendation': 'Maintain monitoring and continue optimization',
            'impact': 'Sustained performance'
        })

    return recs