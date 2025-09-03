import json
import math
from typing import Dict, List, Tuple, Any
from llm_client import LLMClient


class RecommendationEngine:
    def __init__(
        self, data_path: str = "hotel_data.json", config_path: str = "config.json"
    ):
        """Initialize recommendation engine with hotel data."""
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.hotels = self.data["hotels"]
        self.llm_client = LLMClient(config_path)

    def get_basic_recommendations(self, user_preferences: str) -> str:
        """Generate basic recommendations based on user preferences."""
        # Prepare context for LLM
        hotel_summaries = []
        for hotel in self.hotels:
            # Summarize hotel information
            tags = hotel.get("tags", {})
            review_count = len(hotel.get("reviews", []))

            # Extract key themes from reviews
            review_themes = self._extract_review_themes(hotel["reviews"])

            summary = {
                "name": hotel["name"],
                "location": hotel["address"],
                "star_rating": tags.get("star_rating", "N/A"),
                "price_range": tags.get("price_range", "N/A"),
                "amenities": tags.get("amenities", []),
                "review_count": review_count,
                "key_themes": review_themes,
                "tags": tags,
            }
            hotel_summaries.append(summary)

        # Create prompt for LLM
        system_prompt = """You are a professional travel recommendation assistant. Based on user preferences and hotel review information, recommend the most suitable hotels for the user.

Please analyze the match between each hotel's review themes and user preferences, then provide a sorted recommendation list.

For each recommended hotel, please provide:
1. Hotel name and rating
2. Recommendation reason (based on specific information from reviews)
3. Special highlights

Please reply in English."""

        user_message = f"""User preferences: {user_preferences}

Hotel information:
{json.dumps(hotel_summaries, ensure_ascii=False, indent=2)}

Please recommend the most suitable hotels based on user preferences."""

        messages = [{"role": "user", "content": user_message}]

        return self.llm_client.chat_completion(messages, system_prompt)

    def get_enhanced_recommendations(
        self, user_preferences: str, basic_recommendations: str
    ) -> str:
        """Generate enhanced recommendations with information completion."""
        # Perform information completion
        completed_info = self._complete_missing_information()

        # Create enhanced prompt
        system_prompt = """You are an advanced travel recommendation assistant. Now you need to optimize the recommendation list based on completed information.

Rules for information completion:
1. Infer similar features based on geographic location
2. Infer missing tags based on similar hotels
3. Provide confidence scores for inferred information

Please provide more accurate recommendations and indicate which information is inferred."""

        user_message = f"""User preferences: {user_preferences}

Initial recommendations:
{basic_recommendations}

Completed information:
{json.dumps(completed_info, ensure_ascii=False, indent=2)}

Please provide optimized recommendations based on completed information."""

        messages = [{"role": "user", "content": user_message}]

        return self.llm_client.chat_completion(messages, system_prompt)

    def _extract_review_themes(self, reviews: List[Dict]) -> List[str]:
        """Extract key themes from hotel reviews."""
        themes = []
        theme_keywords = {
            "mountain": ["mountain", "mountains", "hiking", "view", "peak", "trail"],
            "river": ["river", "water", "fishing", "stream", "waterfront", "riverside"],
            "downtown": [
                "downtown",
                "city center",
                "business",
                "transportation",
                "metro",
                "urban",
            ],
            "lake": ["lake", "swimming", "boat", "lakeside", "waterfront", "shore"],
            "airport": [
                "airport",
                "shuttle",
                "flight",
                "terminal",
                "transit",
                "layover",
            ],
            "historic": [
                "historic",
                "heritage",
                "culture",
                "traditional",
                "ancient",
                "classic",
            ],
            "beach": ["beach", "ocean", "surf", "sea", "coastal", "sand"],
            "countryside": [
                "countryside",
                "rural",
                "farm",
                "nature",
                "peaceful",
                "quiet",
            ],
        }

        for theme, keywords in theme_keywords.items():
            theme_count = 0
            for review in reviews:
                review_text = review["text"].lower()
                for keyword in keywords:
                    if keyword.lower() in review_text:
                        theme_count += 1
                        break

            if theme_count >= 3:  # If at least 3 reviews mention this theme
                themes.append(theme)

        return themes

    def _complete_missing_information(self) -> Dict[str, Any]:
        """Complete missing information using geographic and similarity analysis."""
        completed_info = {}

        for hotel in self.hotels:
            hotel_id = hotel["id"]
            completed_info[hotel_id] = {
                "name": hotel["name"],
                "inferred_features": [],
                "confidence_scores": {},
            }

            # Analyze geographic proximity
            coords = hotel["coordinates"]
            similar_hotels = self._find_similar_hotels(hotel, coords)

            # Infer missing features based on similar hotels
            inferred_features = self._infer_features(hotel, similar_hotels)

            completed_info[hotel_id]["inferred_features"] = inferred_features[
                "features"
            ]
            completed_info[hotel_id]["confidence_scores"] = inferred_features[
                "confidence"
            ]

        return completed_info

    def _find_similar_hotels(
        self, target_hotel: Dict, target_coords: Dict
    ) -> List[Dict]:
        """Find hotels with similar characteristics."""
        similar_hotels = []

        for hotel in self.hotels:
            if hotel["id"] == target_hotel["id"]:
                continue

            # Calculate geographic distance
            distance = self._calculate_distance(
                target_coords["lat"],
                target_coords["lng"],
                hotel["coordinates"]["lat"],
                hotel["coordinates"]["lng"],
            )

            # Consider hotels within 100km as potentially similar
            if distance < 100:
                similarity_score = self._calculate_similarity(target_hotel, hotel)
                if similarity_score > 0.3:
                    similar_hotels.append(
                        {
                            "hotel": hotel,
                            "distance": distance,
                            "similarity": similarity_score,
                        }
                    )

        return sorted(similar_hotels, key=lambda x: x["similarity"], reverse=True)[:3]

    def _calculate_distance(
        self, lat1: float, lng1: float, lat2: float, lng2: float
    ) -> float:
        """Calculate distance between two coordinates in kilometers."""
        R = 6371  # Earth's radius in kilometers

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)

        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def _calculate_similarity(self, hotel1: Dict, hotel2: Dict) -> float:
        """Calculate similarity score between two hotels."""
        score = 0.0

        # Compare star ratings
        rating1 = hotel1.get("tags", {}).get("star_rating", 0)
        rating2 = hotel2.get("tags", {}).get("star_rating", 0)
        if rating1 and rating2:
            score += 0.3 * (1 - abs(rating1 - rating2) / 5)

        # Compare price ranges
        price1 = hotel1.get("tags", {}).get("price_range", "")
        price2 = hotel2.get("tags", {}).get("price_range", "")
        if price1 == price2 and price1:
            score += 0.2

        # Compare amenities
        amenities1 = set(hotel1.get("tags", {}).get("amenities", []))
        amenities2 = set(hotel2.get("tags", {}).get("amenities", []))
        if amenities1 and amenities2:
            intersection = len(amenities1.intersection(amenities2))
            union = len(amenities1.union(amenities2))
            score += 0.3 * (intersection / union if union > 0 else 0)

        # Compare review themes
        themes1 = set(self._extract_review_themes(hotel1.get("reviews", [])))
        themes2 = set(self._extract_review_themes(hotel2.get("reviews", [])))
        if themes1 and themes2:
            intersection = len(themes1.intersection(themes2))
            union = len(themes1.union(themes2))
            score += 0.2 * (intersection / union if union > 0 else 0)

        return score

    def _infer_features(self, target_hotel: Dict, similar_hotels: List[Dict]) -> Dict:
        """Infer missing features based on similar hotels."""
        inferred = {"features": [], "confidence": {}}

        if not similar_hotels:
            return inferred

        # Collect features from similar hotels
        feature_votes = {}
        total_weight = 0

        for similar in similar_hotels:
            hotel = similar["hotel"]
            weight = similar["similarity"]
            total_weight += weight

            # Check for location-based features
            tags = hotel.get("tags", {})
            for key, value in tags.items():
                if key not in ["star_rating", "price_range", "amenities"]:
                    if key not in feature_votes:
                        feature_votes[key] = 0
                    feature_votes[key] += weight

        # Determine inferred features with confidence scores
        for feature, vote_weight in feature_votes.items():
            confidence = vote_weight / total_weight if total_weight > 0 else 0
            if confidence > 0.5:  # Only include features with >50% confidence
                inferred["features"].append(feature)
                inferred["confidence"][feature] = round(confidence * 100, 1)

        return inferred
