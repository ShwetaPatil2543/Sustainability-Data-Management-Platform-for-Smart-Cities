import os
from .recommender import Recommender
from .predictor import SustainabilityPredictor
from .scorer import SustainabilityScorer

class SustainabilityAdvisor:
    def __init__(self):
        self.recommender = Recommender()
        self.predictor = SustainabilityPredictor()
        self.scorer = SustainabilityScorer()
        self.openai_available = self._check_openai()

    def _check_openai(self):
        """Check if OpenAI API is available"""
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
                return True
        except ImportError:
            pass
        return False

    def generate_response(self, question, days=30):
        """Generate a response to a sustainability question"""
        insights_summary = self.recommender.get_insights_summary(days)
        recommendations = self.recommender.get_recommendations(days)
        sustainability_score = self.scorer.calculate_overall_score(days)

        if self.openai_available:
            return self._generate_openai_response(question, insights_summary, recommendations, sustainability_score)
        else:
            return self._generate_basic_response(question, insights_summary, recommendations, sustainability_score)

    def _generate_openai_response(self, question, insights, recommendations, score_data):
        """Generate response using OpenAI"""
        try:
            prompt = f"""You are an AI Sustainability Advisor for an industrial facility. Based on the following data analysis:

Current Insights: {insights}

Sustainability Score: {score_data['overall_score']}/100 ({score_data['category']})

Key Recommendations:
{self._format_recommendations_for_ai(recommendations)}

User Question: {question}

Provide a helpful, actionable response that addresses the user's question using the data insights, recommendations, and sustainability score.
Keep the response professional and focused on sustainability improvements.
If the question is about improving sustainability, provide specific, prioritized actions."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            # Fallback to basic response if OpenAI fails
            return self._generate_basic_response(question, insights, recommendations, score_data)

    def _generate_basic_response(self, question, insights, recommendations, score_data):
        """Generate basic response without OpenAI"""
        question_lower = question.lower()

        response_parts = []

        # Add sustainability score
        score = score_data['overall_score']
        category = score_data['category']
        response_parts.append(f"Your current sustainability score is {score}/100 ({category}).")

        # Add insights summary
        if insights and insights != "No data available for analysis":
            response_parts.append(f"Data analysis: {insights}")

        # Handle specific question types
        if "score" in question_lower or "rating" in question_lower:
            interpretation = self.scorer.get_score_interpretation(score)
            response_parts.append(f"Score interpretation: {interpretation['description']}")
            if "improve" in question_lower:
                plan = self.scorer.get_improvement_plan(score_data)
                response_parts.append("Priority actions:")
                for action in plan['priority_actions'][:3]:
                    response_parts.append(f"- {action}")

        elif "energy" in question_lower or "electricity" in question_lower:
            energy_recs = [r for r in recommendations if r['category'] == 'Energy Optimization']
            if energy_recs:
                response_parts.append("Energy optimization recommendations:")
                for rec in energy_recs[:2]:
                    response_parts.append(f"- {rec['recommendation']}")

        elif "fuel" in question_lower or "consumption" in question_lower:
            fuel_recs = [r for r in recommendations if 'Fuel' in r['category']]
            if fuel_recs:
                response_parts.append("Fuel efficiency recommendations:")
                for rec in fuel_recs[:2]:
                    response_parts.append(f"- {rec['recommendation']}")

        elif "air" in question_lower or "quality" in question_lower or "pollution" in question_lower:
            air_recs = [r for r in recommendations if 'Air' in r['category'] or 'Emission' in r['category']]
            if air_recs:
                response_parts.append("Air quality improvement recommendations:")
                for rec in air_recs[:2]:
                    response_parts.append(f"- {rec['recommendation']}")

        elif "help" in question_lower and "improve" in question_lower:
            plan = self.scorer.get_improvement_plan(score_data)
            response_parts.append("Here's your personalized improvement plan:")
            response_parts.append("Priority actions:")
            for action in plan['priority_actions'][:5]:
                response_parts.append(f"- {action}")
            if plan.get('potential_savings'):
                response_parts.append(f"Potential savings: {plan['potential_savings']}")

        elif "predict" in question_lower or "future" in question_lower:
            predictions = self.predictor.get_prediction_summary()
            if predictions['energy_predictions']:
                response_parts.append("Energy consumption predictions for next 7 days:")
                for pred in predictions['energy_predictions'][:3]:
                    response_parts.append(f"- {pred['date']}: {pred['prediction']} kWh")

        else:
            # General response with top recommendations
            response_parts.append("Here are your top sustainability recommendations:")
            for rec in recommendations[:3]:
                response_parts.append(f"- {rec['recommendation']}")

        return " ".join(response_parts)

    def _format_recommendations_for_ai(self, recommendations):
        """Format recommendations for AI prompt"""
        formatted = []
        for rec in recommendations[:5]:  # Limit to 5
            formatted.append("- " + rec['category'] + ": " + rec['recommendation'] + " (Impact: " + rec['impact'] + ")")
        return "\n".join(formatted)

    def get_sustainability_score(self, days=30):
        """Get detailed sustainability score"""
        return self.scorer.calculate_overall_score(days)

    def get_predictions(self):
        """Get ML predictions"""
        return self.predictor.get_prediction_summary()