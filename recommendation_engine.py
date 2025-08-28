import json
import math
from typing import Dict, List, Tuple, Any
from llm_client import LLMClient

class RecommendationEngine:
    def __init__(self, data_path: str = "hotel_data.json", config_path: str = "config.json"):
        """Initialize recommendation engine with hotel data."""
        with open(data_path, 'r', encoding='utf-8') as f:
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
                "tags": tags
            }
            hotel_summaries.append(summary)
        
        # Create prompt for LLM
        system_prompt = """你是一个专业的旅游推荐助手。基于用户的偏好和酒店的评论信息，为用户推荐最合适的酒店。

请分析每个酒店的评论主题和用户偏好的匹配度，然后提供排序的推荐列表。

对于每个推荐的酒店，请提供：
1. 酒店名称和评分
2. 推荐理由（基于评论中的具体信息）
3. 特色亮点

请用中文回复。"""
        
        user_message = f"""用户偏好：{user_preferences}

酒店信息：
{json.dumps(hotel_summaries, ensure_ascii=False, indent=2)}

请根据用户偏好推荐最合适的酒店。"""
        
        messages = [{"role": "user", "content": user_message}]
        
        return self.llm_client.chat_completion(messages, system_prompt)
    
    def get_enhanced_recommendations(self, user_preferences: str, basic_recommendations: str) -> str:
        """Generate enhanced recommendations with information completion."""
        # Perform information completion
        completed_info = self._complete_missing_information()
        
        # Create enhanced prompt
        system_prompt = """你是一个高级旅游推荐助手。现在你需要基于补全的信息重新优化推荐列表。

补全信息的规则：
1. 基于地理位置推测相似特征
2. 基于相似酒店的标签推测缺失标签
3. 为推测信息提供置信度评分

请提供更准确的推荐列表，并说明哪些信息是推测的。"""
        
        user_message = f"""用户偏好：{user_preferences}

初始推荐：
{basic_recommendations}

补全的信息：
{json.dumps(completed_info, ensure_ascii=False, indent=2)}

请基于补全信息提供优化后的推荐列表。"""
        
        messages = [{"role": "user", "content": user_message}]
        
        return self.llm_client.chat_completion(messages, system_prompt)
    
    def _extract_review_themes(self, reviews: List[Dict]) -> List[str]:
        """Extract key themes from hotel reviews."""
        themes = []
        theme_keywords = {
            "mountain": ["mountain", "山", "hiking", "登山", "景色", "view"],
            "river": ["river", "河", "water", "水", "fishing", "钓鱼"],
            "downtown": ["downtown", "市中心", "business", "商务", "transportation", "交通"],
            "lake": ["lake", "湖", "swimming", "游泳", "boat", "船"],
            "airport": ["airport", "机场", "shuttle", "班车", "flight", "航班"],
            "historic": ["historic", "历史", "heritage", "遗产", "culture", "文化"],
            "beach": ["beach", "海滩", "ocean", "海洋", "surf", "冲浪"],
            "countryside": ["countryside", "乡村", "farm", "农场", "nature", "自然"]
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
                "confidence_scores": {}
            }
            
            # Analyze geographic proximity
            coords = hotel["coordinates"]
            similar_hotels = self._find_similar_hotels(hotel, coords)
            
            # Infer missing features based on similar hotels
            inferred_features = self._infer_features(hotel, similar_hotels)
            
            completed_info[hotel_id]["inferred_features"] = inferred_features["features"]
            completed_info[hotel_id]["confidence_scores"] = inferred_features["confidence"]
        
        return completed_info
    
    def _find_similar_hotels(self, target_hotel: Dict, target_coords: Dict) -> List[Dict]:
        """Find hotels with similar characteristics."""
        similar_hotels = []
        
        for hotel in self.hotels:
            if hotel["id"] == target_hotel["id"]:
                continue
            
            # Calculate geographic distance
            distance = self._calculate_distance(
                target_coords["lat"], target_coords["lng"],
                hotel["coordinates"]["lat"], hotel["coordinates"]["lng"]
            )
            
            # Consider hotels within 100km as potentially similar
            if distance < 100:
                similarity_score = self._calculate_similarity(target_hotel, hotel)
                if similarity_score > 0.3:
                    similar_hotels.append({
                        "hotel": hotel,
                        "distance": distance,
                        "similarity": similarity_score
                    })
        
        return sorted(similar_hotels, key=lambda x: x["similarity"], reverse=True)[:3]
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates in kilometers."""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
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