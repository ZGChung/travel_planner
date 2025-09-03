# 🏨 AI-Powered Hotel Recommendation System

An intelligent hotel recommendation tool based on large language models that analyzes numerous user reviews and provides personalized recommendations based on individual preferences.

## ✨ Key Features

### 🎯 Personalized Recommendations
- **Intelligent Requirement Analysis**: Analyzes user preferences from natural language input
- **Deep Review Mining**: Automatically analyzes hundreds of user reviews to extract key information
- **Dual Recommendation Modes**: Provides both basic and enhanced recommendation modes

### 🔍 Information Completion Technology
- **Geographic Location Inference**: Infers similar features based on hotel locations
- **Similarity Analysis**: Completes missing information through similar hotel features
- **Confidence Scoring**: Provides reliability assessment for inferred information

### 🤖 Configurable AI Backend
- **Multi-Model Support**: Default support for DeepSeek API, easily switchable to other LLMs
- **Smart Degradation**: Automatically switches to simulation response mode when API is unavailable
- **Flexible Configuration**: Easily adjust model parameters through configuration file

## 🚀 Quick Start

### Environment Requirements
- Python 3.8+
- Network connection (for API calls)

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key** (Optional)
   
   Edit `config.json` file to add your DeepSeek API key:
   ```json
   {
     "llm_provider": "deepseek",
     "deepseek_api_key": "YOUR_DEEPSEEK_API_KEY_HERE",
     "deepseek_base_url": "https://api.deepseek.com",
     "model_name": "deepseek-chat",
     "max_tokens": 2000,
     "temperature": 0.7
   }
   ```
   
   > 💡 **Tip**: If API key is not configured, system will use built-in simulation response mode, all features remain fully functional.

3. **Launch Application**
   ```bash
   streamlit run app.py
   ```

4. **Access Application**
   
   Open the displayed URL in your browser (usually `http://localhost:8501`)

## 📖 User Guide

### Basic Usage Flow

1. **Input Requirements**: Describe your hotel preferences in the text box
   - Example: "I want to stay near mountains, in a quiet environment suitable for relaxation and hiking"
   - Example: "I need a hotel with convenient transportation, close to city center, suitable for business activities"

2. **Get Basic Recommendations**: Click "🚀 Get Basic Recommendations" button
   - System will analyze all hotel reviews
   - Generate initial recommendation list based on your requirements

3. **Get Enhanced Recommendations**: Click "⭐ Get Enhanced Recommendations" button
   - System will complete missing hotel information
   - Provide more accurate optimized recommendation list
   - View detailed information completion process

### Interface Features

#### Left Sidebar
- **System Configuration**: Shows current LLM configuration and API status
- **Data Overview**: Displays hotel and review data statistics
- **Hotel List**: Can expand to view all available hotels

#### Main Interface
- **User Requirements Input**: Free text input box and example requirement selection
- **Recommendations**: Shows basic and enhanced recommendations in tabs
- **Information Completion Details**: Can expand to view AI reasoning process

## 🏗️ System Architecture

### Core Components

1. **LLM Client** (`llm_client.py`)
   - Supports DeepSeek API integration
   - Provides simulation response degradation mechanism
   - Expandable to support other LLM providers

2. **Recommendation Engine** (`recommendation_engine.py`)
   - Review topic extraction and analysis
   - Geographic location similarity calculation
   - Information completion and confidence assessment

3. **Data Layer** (`hotel_data.json`)
   - 8 simulated hotel datasets
   - Each hotel contains 10 detailed reviews
   - Covers mountain views, river views, city center, beach, and other scenarios

4. **User Interface** (`app.py`)
   - Interactive web interface built with Streamlit
   - Responsive design, supports multiple screen sizes
   - Real-time status feedback and error handling

### Technical Features

- **Intelligent Review Analysis**: Uses keyword matching and topic extraction technology
- **Similarity Algorithm**: Calculates based on multiple dimensions including geographic location, star rating, price
- **Confidence Mechanism**: Provides reliability scores for inferred information
- **Fault Tolerance**: Automatically degrades to local processing when API fails

## ⚙️ Configuration Options

### config.json Parameter Description

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `llm_provider` | LLM provider | "deepseek" |
| `deepseek_api_key` | DeepSeek API key | "YOUR_DEEPSEEK_API_KEY_HERE" |
| `deepseek_base_url` | API base URL | "https://api.deepseek.com" |
| `model_name` | Model name | "deepseek-chat" |
| `max_tokens` | Maximum generated tokens | 2000 |
| `temperature` | Generation temperature | 0.7 |

## 🔧 Development and Extension

### Adding New Hotel Data
Edit `hotel_data.json` file, add new hotels following existing format:
```json
{
  "id": "hotel_new",
  "name": "New Hotel Name",
  "address": "Hotel Address",
  "coordinates": {"lat": latitude, "lng": longitude},
  "tags": {
    "star_rating": rating,
    "amenities": ["amenity list"],
    "price_range": "price range"
  },
  "reviews": [
    {"user": "username", "rating": rating, "text": "review content"}
  ]
}
```

### Integrating Other LLM Providers
Modify the `chat_completion` method in `llm_client.py` to add new API call logic.

### Customizing Recommendation Algorithm
Modify similarity calculation and feature inference logic in `recommendation_engine.py`.

## 🐛 Troubleshooting

### Common Issues

**Q: Recommendations show as simulation response?**
A: Check if API key is correctly configured in `config.json`.

**Q: Application fails to start?**
A: Make sure all dependencies are installed: `pip install -r requirements.txt`

**Q: Recommendations not accurate?**
A: Try describing your requirements in more detail, or configure a real API key for better results.

**Q: Information completion details empty?**
A: This is normal in simulation mode, detailed reasoning process will be shown after configuring real API key.

## 📄 License

This project is for learning and demonstration purposes only.

## 🤝 Contribution

Welcome to submit Issues and Pull Requests to improve this project!

---

**💡 Tip**: For best experience, it's recommended to configure a real DeepSeek API key. This will enable complete AI reasoning functionality and provide more accurate and personalized recommendation results.