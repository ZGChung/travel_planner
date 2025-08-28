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
            "补全" in last_message
            or "enhanced" in last_message.lower()
            or "优化" in last_message
        ):
            return self._generate_enhanced_mock_response(last_message)
        elif "推荐" in last_message or "recommend" in last_message.lower():
            return self._generate_basic_mock_response(last_message)
        else:
            return "我理解您的需求。请告诉我您更关注酒店的哪些方面，比如位置特色、交通便利性、自然环境等，我会为您提供个性化的推荐。"

    def _generate_basic_mock_response(self, user_input: str) -> str:
        """Generate basic mock recommendation response."""
        # Analyze user preferences from input
        preferences = self._analyze_user_preferences(user_input)

        if "山" in user_input or "mountain" in user_input.lower():
            return """基于您的需求分析，我为您推荐以下酒店：

**推荐列表：**

1. **Mountain View Resort** (评分: 4.5/5)
   - 推荐理由: 位于山脚下，提供绝佳的山景视野，适合喜欢自然环境的客人
   - 特色: 直接通往登山步道，提供山地自行车租赁服务

2. **Countryside Manor** (评分: 4.1/5)
   - 推荐理由: 乡村环境安静，周围有丘陵地带，适合放松
   - 特色: 远离城市喧嚣，提供宁静的自然环境

3. **Riverside Inn** (评分: 4.2/5) 
   - 推荐理由: 河边位置提供宁静的环境，河水声有助于放松
   - 特色: 直接河流通道，提供钓鱼和皮划艇设备租赁

这些推荐基于评论中提到的位置特色和客人反馈进行分析。"""

        elif (
            "交通" in user_input
            or "business" in user_input.lower()
            or "商务" in user_input
        ):
            return """基于您的需求分析，我为您推荐以下酒店：

**推荐列表：**

1. **Downtown Business Hotel** (评分: 4.3/5)
   - 推荐理由: 市中心位置，交通便利，适合商务和城市观光
   - 特色: 步行可达地铁站，周边餐饮和购物选择丰富

2. **Airport Express Hotel** (评分: 4.0/5)
   - 推荐理由: 靠近机场，班车服务便利，适合商务出行
   - 特色: 24小时班车服务，商务设施完善

3. **Historic Town Square Inn** (评分: 4.2/5)
   - 推荐理由: 位于历史城区中心，交通便利且有文化特色
   - 特色: 步行可达多个历史景点和商业区

这些推荐基于评论中提到的交通便利性和商务设施进行分析。"""

        else:
            return """基于您的需求分析，我为您推荐以下酒店：

**推荐列表：**

1. **Beachfront Paradise Resort** (评分: 4.6/5)
   - 推荐理由: 海滨位置，环境优美，适合度假放松
   - 特色: 直接海滩通道，水上运动设施齐全

2. **Lakeside Lodge** (评分: 4.3/5)
   - 推荐理由: 湖边环境宁静，适合家庭度假
   - 特色: 湖景房间，提供船只租赁服务

3. **Mountain View Resort** (评分: 4.5/5)
   - 推荐理由: 山景优美，空气清新，适合自然爱好者
   - 特色: 登山步道，户外活动丰富

这些推荐基于评论中提到的环境特色和客人反馈进行分析。"""

    def _generate_enhanced_mock_response(self, user_input: str) -> str:
        """Generate enhanced mock recommendation response with information completion."""
        # Analyze user preferences
        if "山" in user_input or "mountain" in user_input.lower():
            return """**🔍 信息补全分析结果：**

基于地理位置和相似酒店的信息，我对缺失信息进行了推测：

**📊 补全信息：**
- **Countryside Manor**: 推测靠近山区 (置信度: 72%) - 基于地理位置相似性
- **Historic Town Square Inn**: 推测周边有山景 (置信度: 58%) - 基于相似酒店特征
- **Lakeside Lodge**: 推测湖泊周围有山丘 (置信度: 67%) - 基于地形分析

**⭐ 更新后的推荐：**

1. **Mountain View Resort** (评分: 4.5/5) 
   - 推荐理由: 位于山脚下，提供绝佳的山景视野 ✅ *信息完整*
   - 特色: 直接通往登山步道，提供山地自行车租赁服务

2. **🆕 Lakeside Lodge** (评分: 4.4/5) *排名上升*
   - 推荐理由: 湖泊周围可能有山丘环绕 🔍 *基于补全信息 (67% 置信度)*
   - 特色: 潜在的湖景+山景双重体验，适合多样化户外活动

3. **🆕 Countryside Manor** (评分: 4.3/5) *新增推荐*
   - 推荐理由: 可能位于乡村山区环境 🔍 *基于补全信息 (72% 置信度)*
   - 特色: 推测远离城市，可能有纯净山区空气

**📈 推荐变化说明：**
- 新增了2个基于信息补全的酒店推荐（置信度均低于75%）
- 重新排序了推荐优先级，考虑了信息不确定性
- 补全信息提供了更多可能性，但需要实际验证"""

        elif (
            "交通" in user_input
            or "business" in user_input.lower()
            or "商务" in user_input
        ):
            return """**🔍 信息补全分析结果：**

基于地理位置和相似酒店的信息，我对缺失信息进行了推测：

**📊 补全信息：**
- **Historic Town Square Inn**: 推测交通便利性较高 (置信度: 63%) - 基于城区位置
- **Beachfront Paradise Resort**: 推测可能有机场班车 (置信度: 45%) - 基于度假村标准
- **Lakeside Lodge**: 推测交通可能不便 (置信度: 78%) - 基于偏远位置

**⭐ 更新后的推荐：**

1. **Downtown Business Hotel** (评分: 4.3/5)
   - 推荐理由: 市中心位置，交通便利 ✅ *信息完整*
   - 特色: 步行可达地铁站，周边餐饮和购物选择丰富

2. **🆕 Historic Town Square Inn** (评分: 4.4/5) *排名上升*
   - 推荐理由: 历史城区中心，可能交通便利且有文化特色 🔍 *基于补全信息 (63% 置信度)*
   - 特色: 推测步行可达多个交通枢纽和商业区

3. **Airport Express Hotel** (评分: 4.0/5)
   - 推荐理由: 机场附近，班车服务便利 ✅ *信息完整*
   - 特色: 24小时班车服务，商务设施完善

**📈 推荐变化说明：**
- Historic Town Square Inn 基于推测的交通信息排名提升（置信度63%）
- 过滤掉了交通可能不便的偏远酒店（置信度78%）
- 补全信息提供了更多参考，但需要实际验证准确性"""

        else:
            return """**🔍 信息补全分析结果：**

基于地理位置和相似酒店的信息，我对缺失信息进行了推测：

**📊 补全信息：**
- **Mountain View Resort**: 推测可能提供SPA服务 (置信度: 52%) - 基于度假村特征
- **Historic Town Square Inn**: 推测可能有文化活动 (置信度: 68%) - 基于历史位置
- **Countryside Manor**: 推测可能有有机餐厅 (置信度: 47%) - 基于乡村特色

**⭐ 更新后的推荐：**

1. **🆕 Historic Town Square Inn** (评分: 4.5/5) *排名上升*
   - 推荐理由: 历史文化氛围浓厚，可能有定期文化活动 🔍 *基于补全信息 (68% 置信度)*
   - 特色: 历史建筑+潜在文化体验，独特的住宿可能性

2. **Beachfront Paradise Resort** (评分: 4.6/5)
   - 推荐理由: 海滨位置，环境优美 ✅ *信息完整*
   - 特色: 直接海滩通道，水上运动设施齐全

3. **🆕 Mountain View Resort** (评分: 4.6/5) *服务升级*
   - 推荐理由: 山景优美+可能提供SPA服务 🔍 *基于补全信息 (52% 置信度)*
   - 特色: 登山步道+潜在SPA中心，可能的身心放松体验

**📈 推荐变化说明：**
- 基于推测信息重新评估了酒店服务质量（置信度均低于70%）
- Historic Town Square Inn 因潜在文化特色排名提升
- 补全信息提供了服务升级的可能性，但需要实际确认"""

    def _analyze_user_preferences(self, user_input: str) -> dict:
        """Analyze user preferences from input text."""
        preferences = {
            "mountain": "山" in user_input or "mountain" in user_input.lower(),
            "business": "交通" in user_input
            or "business" in user_input.lower()
            or "商务" in user_input,
            "quiet": "安静" in user_input or "quiet" in user_input.lower(),
            "beach": "海" in user_input or "beach" in user_input.lower(),
            "culture": "文化" in user_input or "culture" in user_input.lower(),
        }
        return preferences
