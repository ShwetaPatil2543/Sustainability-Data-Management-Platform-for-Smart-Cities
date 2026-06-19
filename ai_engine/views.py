from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .agent import SustainabilityAdvisor

class AIAdvisorView(APIView):
    """AI Sustainability Advisor API endpoint"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get("question", "").strip()

        if not question:
            return Response(
                {"error": "Question is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            advisor = SustainabilityAdvisor()
            answer = advisor.generate_response(question)

            return Response({
                "question": question,
                "answer": answer
            })

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SustainabilityScoreView(APIView):
    """Get sustainability score"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            advisor = SustainabilityAdvisor()
            score_data = advisor.get_sustainability_score()

            return Response(score_data)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PredictionsView(APIView):
    """Get ML predictions"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            advisor = SustainabilityAdvisor()
            predictions = advisor.get_predictions()

            return Response(predictions)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Keep the old view for backward compatibility
class AIRecommendationView(APIView):
    """Legacy recommendation endpoint"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get("query", "").lower()

        recommendations = []

        if "aqi" in query or "air" in query:
            recommendations.append({
                "module": "Air Quality",
                "problem": "AQI levels are high",
                "action": "Install air filtration systems",
                "impact": "Improved workplace air quality"
            })

        if "energy" in query:
            recommendations.append({
                "module": "Energy",
                "problem": "High electricity consumption",
                "action": "Implement smart energy monitoring",
                "impact": "Reduced energy cost"
            })

        if not recommendations:
            recommendations.append({
                "module": "System",
                "problem": "No issues detected",
                "action": "Maintain current sustainability practices",
                "impact": "Stable environmental performance"
            })

        return Response({"recommendations": recommendations})