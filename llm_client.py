import json
import requests
from typing import Dict, Any, Optional


class LLMClient:
    def __init__(self, config_path: str = "config.json"):
        """Initialize LLM client with configuration."""
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.provider = self.config.get("llm_provider", "deepseek")
        self.api_key = self.config.get("deepseek_api_key")
        self.base_url = self.config.get("deepseek_base_url", "https://api.deepseek.com")
        self.model_name = self.config.get("model_name", "deepseek-chat")
        self.max_tokens = self.config.get("max_tokens", 2000)
        self.temperature = self.config.get("temperature", 0.7)

    def chat_completion(
        self, messages: list, system_prompt: Optional[str] = None
    ) -> str:
        """Send chat completion request to LLM."""
        if not self.api_key or self.api_key == "YOUR_DEEPSEEK_API_KEY_HERE":
            return self._mock_response(messages, system_prompt)

        try:
            # Prepare messages
            formatted_messages = []
            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})

            for msg in messages:
                formatted_messages.append(msg)

            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "model": self.model_name,
                "messages": formatted_messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }

            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._mock_response(messages, system_prompt)

        except Exception as e:
            print(f"LLM API Error: {str(e)}")
            return self._mock_response(messages, system_prompt)

    def _mock_response(
        self, messages: list, system_prompt: Optional[str] = None
    ) -> str:
        """Provide mock response when API is not available."""
        last_message = messages[-1]["content"] if messages else ""

        # Check if this is an enhanced recommendation request
        if (
            "complete" in last_message.lower()
            or "enhanced" in last_message.lower()
            or "optimize" in last_message.lower()
        ):
            return self._generate_enhanced_mock_response(last_message)
        elif "recommend" in last_message.lower():
            return self._generate_basic_mock_response(last_message)
        else:
            return "I understand your requirements. Please tell me which aspects of the hotel you care about most, such as location features, transportation convenience, natural environment, etc., and I will provide personalized recommendations."

    def _generate_basic_mock_response(self, user_input: str) -> str:
        """Generate basic mock recommendation response."""
        # Analyze user preferences from input
        preferences = self._analyze_user_preferences(user_input)

        if "mountain" in user_input.lower():
            return """Based on your requirements analysis, I recommend the following hotels:

**Recommendations:**

1. **Mountain View Resort** (Rating: 4.5/5)
   - Reason: Located at the foot of mountains, offering excellent mountain views, perfect for nature lovers
   - Features: Direct access to hiking trails, mountain bike rental service

2. **Countryside Manor** (Rating: 4.1/5)
   - Reason: Quiet rural environment with surrounding hills, suitable for relaxation
   - Features: Away from city noise, providing peaceful natural environment

3. **Riverside Inn** (Rating: 4.2/5) 
   - Reason: Riverside location provides quiet environment, river sounds help relaxation
   - Features: Direct river access, fishing and kayak equipment rental

These recommendations are based on location features and guest feedback mentioned in reviews."""

        elif "transportation" in user_input.lower() or "business" in user_input.lower():
            return """Based on your requirements analysis, I recommend the following hotels:

**Recommendations:**

1. **Downtown Business Hotel** (Rating: 4.3/5)
   - Reason: City center location, convenient transportation, suitable for business and city sightseeing
   - Features: Walking distance to metro station, rich dining and shopping options nearby

2. **Airport Express Hotel** (Rating: 4.0/5)
   - Reason: Close to airport, convenient shuttle service, suitable for business travel
   - Features: 24-hour shuttle service, comprehensive business facilities

3. **Historic Town Square Inn** (Rating: 4.2/5)
   - Reason: Located in historic district center, convenient transportation with cultural character
   - Features: Walking distance to multiple historic sites and business districts

These recommendations are based on transportation convenience and business facilities mentioned in reviews."""

        else:
            return """Based on your requirements analysis, I recommend the following hotels:

**Recommendations:**

1. **Beachfront Paradise Resort** (Rating: 4.6/5)
   - Reason: Beachfront location, beautiful environment, perfect for vacation relaxation
   - Features: Direct beach access, complete water sports facilities

2. **Lakeside Lodge** (Rating: 4.3/5)
   - Reason: Lakeside environment is quiet, suitable for family vacation
   - Features: Lake view rooms, boat rental service

3. **Mountain View Resort** (Rating: 4.5/5)
   - Reason: Beautiful mountain views, fresh air, suitable for nature enthusiasts
   - Features: Hiking trails, rich outdoor activities

These recommendations are based on environmental features and guest feedback mentioned in reviews."""

    def _generate_enhanced_mock_response(self, user_input: str) -> str:
        """Generate enhanced mock recommendation response with information completion."""
        # Analyze user preferences
        if "mountain" in user_input.lower():
            return """**🔍 Information Completion Analysis Results:**

Based on geographic location and similar hotel information, I have inferred missing information:

**📊 Completed Information:**
- **Countryside Manor**: Inferred near mountain area (Confidence: 72%) - Based on geographic location similarity
- **Historic Town Square Inn**: Inferred mountain views nearby (Confidence: 58%) - Based on similar hotel features
- **Lakeside Lodge**: Inferred hills around lake (Confidence: 67%) - Based on terrain analysis

**⭐ Updated Recommendations:**

1. **Mountain View Resort** (Rating: 4.5/5) 
   - Reason: Located at mountain foot, offering excellent mountain views ✅ *Complete Information*
   - Features: Direct access to hiking trails, mountain bike rental service

2. **🆕 Lakeside Lodge** (Rating: 4.4/5) *Ranking Improved*
   - Reason: Lake possibly surrounded by hills 🔍 *Based on completed information (67% confidence)*
   - Features: Potential lake + mountain view dual experience, suitable for diverse outdoor activities

3. **🆕 Countryside Manor** (Rating: 4.3/5) *New Recommendation*
   - Reason: Possibly located in rural mountain area 🔍 *Based on completed information (72% confidence)*
   - Features: Inferred away from city, possibly pure mountain air

**📈 Recommendation Changes Explained:**
- Added 2 hotels based on information completion (confidence below 75%)
- Reordered recommendation priority, considering information uncertainty
- Completed information provides more possibilities, but needs actual verification"""

        elif "transportation" in user_input.lower() or "business" in user_input.lower():
            return """**🔍 Information Completion Analysis Results:**

Based on geographic location and similar hotel information, I have inferred missing information:

**📊 Completed Information:**
- **Historic Town Square Inn**: Inferred high transportation convenience (Confidence: 63%) - Based on urban location
- **Beachfront Paradise Resort**: Inferred possible airport shuttle (Confidence: 45%) - Based on resort standards
- **Lakeside Lodge**: Inferred possibly inconvenient transportation (Confidence: 78%) - Based on remote location

**⭐ Updated Recommendations:**

1. **Downtown Business Hotel** (Rating: 4.3/5)
   - Reason: City center location, convenient transportation ✅ *Complete Information*
   - Features: Walking distance to metro station, rich dining and shopping options nearby

2. **🆕 Historic Town Square Inn** (Rating: 4.4/5) *Ranking Improved*
   - Reason: Historic district center, possibly convenient transportation with cultural character 🔍 *Based on completed information (63% confidence)*
   - Features: Inferred walking distance to multiple transportation hubs and business districts

3. **Airport Express Hotel** (Rating: 4.0/5)
   - Reason: Near airport, convenient shuttle service ✅ *Complete Information*
   - Features: 24-hour shuttle service, comprehensive business facilities

**📈 Recommendation Changes Explained:**
- Historic Town Square Inn ranking improved based on inferred transportation information (63% confidence)
- Filtered out hotels with potentially inconvenient transportation (78% confidence)
- Completed information provides more reference, but accuracy needs actual verification"""

        else:
            return """**🔍 Information Completion Analysis Results:**

Based on geographic location and similar hotel information, I have inferred missing information:

**📊 Completed Information:**
- **Mountain View Resort**: Inferred possible SPA service (Confidence: 52%) - Based on resort features
- **Historic Town Square Inn**: Inferred possible cultural activities (Confidence: 68%) - Based on historic location
- **Countryside Manor**: Inferred possible organic restaurant (Confidence: 47%) - Based on rural character

**⭐ Updated Recommendations:**

1. **🆕 Historic Town Square Inn** (Rating: 4.5/5) *Ranking Improved*
   - Reason: Rich historical cultural atmosphere, possibly regular cultural activities 🔍 *Based on completed information (68% confidence)*
   - Features: Historic building + potential cultural experience, unique accommodation possibility

2. **Beachfront Paradise Resort** (Rating: 4.6/5)
   - Reason: Beachfront location, beautiful environment ✅ *Complete Information*
   - Features: Direct beach access, complete water sports facilities

3. **🆕 Mountain View Resort** (Rating: 4.6/5) *Service Upgrade*
   - Reason: Beautiful mountain views + possible SPA service 🔍 *Based on completed information (52% confidence)*
   - Features: Hiking trails + potential SPA center, possible physical and mental relaxation experience

**📈 Recommendation Changes Explained:**
- Re-evaluated hotel service quality based on inferred information (all confidence below 70%)
- Historic Town Square Inn ranking improved due to potential cultural features
- Completed information provides service upgrade possibilities, but needs actual confirmation"""

    def _analyze_user_preferences(self, user_input: str) -> dict:
        """Analyze user preferences from input text."""
        preferences = {
            "mountain": "mountain" in user_input.lower(),
            "business": "transportation" in user_input.lower()
            or "business" in user_input.lower(),
            "quiet": "quiet" in user_input.lower(),
            "beach": "beach" in user_input.lower(),
            "culture": "culture" in user_input.lower(),
        }
        return preferences
