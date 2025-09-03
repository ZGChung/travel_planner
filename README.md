# 🏨 AI-Powered Hotel Recommendation System

An AI-based smart hotel recommendation tool that provides personalized hotel suggestions by analyzing user reviews and personal preferences.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Application
```bash
streamlit run app.py
```

### 3. Access Application
Open `http://localhost:8501` in your browser

## 📖 User Guide

### 🎯 Get Hotel Recommendations

1. **Enter Your Requirements**
   - Describe your hotel preferences in the "User Requirements Input" area
   - For example: "I want to stay near mountains, in a quiet environment suitable for relaxation"
   - Or choose from preset example requirements

2. **Get Basic Recommendations**
   - Click the "🚀 Get Basic Recommendations" button
   - System will analyze all hotel reviews and generate initial recommendations

3. **Get Enhanced Recommendations** (Optional)
   - Click the "⭐ Get Enhanced Recommendations" button
   - System will complete missing information and provide more accurate recommendations
   - View detailed information completion process

### 🏨 View Hotel Details

- **Browse Hotel List**: Expand "View All Hotels" in the left sidebar
- **Click Hotel Name**: View detailed information, including:
  - 📍 Basic Information (address, coordinates)
  - 🏷️ Hotel Tags (star rating, price, amenities)
  - 📊 Review Statistics (average rating, rating distribution)
  - 💬 User Reviews (supports rating filtering and sorting)

### 🔍 Compare Recommendations

System provides two recommendation modes:

- **📋 Basic Recommendations**: Initial recommendations based on review analysis
- **⭐ Enhanced Recommendations**: Optimized recommendations with information completion
  - 🆕 New recommended hotels
  - ✅ Hotels with complete information
  - 🔍 Recommendations based on completed information
  - Shows confidence scores and change explanations

## ⚙️ Configuration Options

### API Configuration (Optional)

Edit `config.json` file to configure DeepSeek API:

```json
{
  "llm_provider": "deepseek",
  "deepseek_api_key": "YOUR_API_KEY_HERE",
  "deepseek_base_url": "https://api.deepseek.com",
  "model_name": "deepseek-chat",
  "max_tokens": 2000,
  "temperature": 0.7
}
```

> 💡 **Tip**: System uses simulation response mode when API key is not configured, all features remain fully functional.

## ✨ Key Features

### 🎯 Smart Recommendations
- Natural language requirement analysis
- Deep review mining
- Dual recommendation modes (Basic + Enhanced)

### 🔍 Information Completion
- Geographic location inference
- Similarity analysis
- Confidence assessment (realistically reflects uncertainty in inferred information)

### 🏨 Hotel Details
- 15 curated hotel datasets
- 150 authentic user reviews
- Multi-dimensional hotel information display

### 🎨 User Interface
- Responsive design
- Intuitive operation flow
- Real-time status feedback

## 🏗️ System Features

- **Intelligent Analysis**: AI-driven review analysis and requirement matching
- **Visual Comparison**: Clear display of recommendation changes and improvements
- **Interactive Experience**: Click-based hotel detail browsing
- **Flexible Configuration**: Supports multiple LLM backends
- **Fault Tolerance**: Automatic degradation when API is unavailable

## 🔧 Troubleshooting

**Application won't start?**
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Recommendations not ideal?**
- Try describing requirements in more detail
- Use example requirements as reference
- Configure real API key for better results

**Hotel detail page blank?**
- Make sure you clicked a hotel name in the sidebar
- Use "🔙 Return to Home" button to go back to main interface

## 📚 More Information

For detailed technical documentation and development guide, please refer to `INSTRUCTION.md` file.

---

🎉 **Start experiencing smart hotel recommendations!** Enter your requirements to discover the most suitable hotels.