import streamlit as st
import json
from recommendation_engine import RecommendationEngine

# Page configuration
st.set_page_config(
    page_title="智能旅游酒店推荐系统",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make sidebar wider
st.markdown("""
<style>
    .css-1d391kg {
        width: 900px;
    }
    .css-1lcbmhc {
        width: 900px;
    }
    .css-17eq0hr {
        width: 900px;
    }
    section[data-testid="stSidebar"] {
        width: 900px !important;
    }
    section[data-testid="stSidebar"] > div {
        width: 900px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommendation_engine' not in st.session_state:
    st.session_state.recommendation_engine = RecommendationEngine()

if 'basic_recommendations' not in st.session_state:
    st.session_state.basic_recommendations = None

if 'enhanced_recommendations' not in st.session_state:
    st.session_state.enhanced_recommendations = None

if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = ""

if 'selected_hotel' not in st.session_state:
    st.session_state.selected_hotel = None

if 'show_hotel_detail' not in st.session_state:
    st.session_state.show_hotel_detail = False

# Main title
st.title("🏨 智能旅游酒店推荐系统")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ 系统配置")
    
    # Display current configuration
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        st.subheader("当前配置")
        st.write(f"**LLM提供商**: {config.get('llm_provider', 'deepseek')}")
        st.write(f"**模型**: {config.get('model_name', 'deepseek-chat')}")
        
        api_key = config.get('deepseek_api_key', '')
        if api_key == "YOUR_DEEPSEEK_API_KEY_HERE":
            st.warning("⚠️ 请在config.json中配置您的API密钥")
            st.info("💡 当前使用模拟响应模式")
        else:
            st.success("✅ API密钥已配置")
            
    except Exception as e:
        st.error(f"配置文件读取错误: {str(e)}")

    st.markdown("---")
    
    # Hotel data summary
    st.subheader("📊 数据概览")
    hotels = st.session_state.recommendation_engine.hotels
    st.write(f"**酒店数量**: {len(hotels)}")
    
    total_reviews = sum(len(hotel.get('reviews', [])) for hotel in hotels)
    st.write(f"**评论总数**: {total_reviews}")
    
    # Show hotel list with clickable names
    with st.expander("查看所有酒店"):
        for hotel in hotels:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📍 {hotel['name']}", key=f"hotel_{hotel['id']}", help="点击查看详情"):
                    st.session_state.selected_hotel = hotel['id']
                    st.session_state.show_hotel_detail = True
                    st.rerun()
            with col2:
                st.write(f"({len(hotel.get('reviews', []))} 条评论)")

# Check if hotel detail should be shown
if st.session_state.show_hotel_detail and st.session_state.selected_hotel:
    # Show hotel detail page
    selected_hotel_data = None
    for hotel in hotels:
        if hotel['id'] == st.session_state.selected_hotel:
            selected_hotel_data = hotel
            break
    
    if selected_hotel_data:
        # Hotel detail header
        col1, col2 = st.columns([4, 1])
        with col1:
            st.header(f"🏨 {selected_hotel_data['name']}")
        with col2:
            if st.button("🔙 返回主页", type="secondary"):
                st.session_state.show_hotel_detail = False
                st.session_state.selected_hotel = None
                st.rerun()
        
        st.markdown("---")
        
        # Hotel basic information
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📍 基本信息")
            st.write(f"**地址**: {selected_hotel_data['address']}")
            st.write(f"**坐标**: {selected_hotel_data['coordinates']['lat']}, {selected_hotel_data['coordinates']['lng']}")
            
            # Tags information
            tags = selected_hotel_data.get('tags', {})
            st.subheader("🏷️ 酒店标签")
            
            col_tag1, col_tag2 = st.columns(2)
            with col_tag1:
                st.write(f"⭐ **星级**: {tags.get('star_rating', 'N/A')}")
                st.write(f"💰 **价格区间**: {tags.get('price_range', 'N/A')}")
            
            with col_tag2:
                amenities = tags.get('amenities', [])
                if amenities:
                    st.write("🎯 **设施服务**:")
                    for amenity in amenities:
                        st.write(f"  • {amenity}")
            
            # Special features
            special_features = []
            for key, value in tags.items():
                if key not in ['star_rating', 'price_range', 'amenities'] and value is True:
                    special_features.append(key)
            
            if special_features:
                st.write("✨ **特色标签**:")
                for feature in special_features:
                    st.write(f"  • {feature}")
        
        with col2:
            # Review statistics
            reviews = selected_hotel_data.get('reviews', [])
            if reviews:
                st.subheader("📊 评论统计")
                avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
                st.metric("平均评分", f"{avg_rating:.1f}/5", f"{len(reviews)} 条评论")
                
                # Rating distribution
                rating_counts = {}
                for r in reviews:
                    rating = r['rating']
                    rating_counts[rating] = rating_counts.get(rating, 0) + 1
                
                st.write("**评分分布**:")
                for rating in sorted(rating_counts.keys(), reverse=True):
                    count = rating_counts[rating]
                    percentage = (count / len(reviews)) * 100
                    st.write(f"{rating}⭐: {count} 条 ({percentage:.1f}%)")
        
        st.markdown("---")
        
        # Reviews section
        st.subheader("💬 用户评论")
        
        if reviews:
            # Review filter
            col1, col2 = st.columns([2, 1])
            with col1:
                rating_filter = st.selectbox(
                    "筛选评分",
                    ["全部评分", "5星", "4星", "3星", "2星", "1星"],
                    key="rating_filter"
                )
            with col2:
                sort_order = st.selectbox(
                    "排序方式",
                    ["评分从高到低", "评分从低到高"],
                    key="sort_order"
                )
            
            # Filter and sort reviews
            filtered_reviews = reviews.copy()
            if rating_filter != "全部评分":
                target_rating = int(rating_filter[0])
                filtered_reviews = [r for r in filtered_reviews if r['rating'] == target_rating]
            
            if sort_order == "评分从高到低":
                filtered_reviews.sort(key=lambda x: x['rating'], reverse=True)
            else:
                filtered_reviews.sort(key=lambda x: x['rating'])
            
            # Display reviews
            for i, review in enumerate(filtered_reviews):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{review['user']}**")
                    with col2:
                        st.write(f"{'⭐' * review['rating']} ({review['rating']}/5)")
                    
                    st.write(review['text'])
                    
                    if i < len(filtered_reviews) - 1:
                        st.markdown("---")
        else:
            st.info("暂无用户评论")
    
    else:
        st.error("未找到选中的酒店信息")
        if st.button("返回主页"):
            st.session_state.show_hotel_detail = False
            st.session_state.selected_hotel = None
            st.rerun()

else:
    # Main content area (original layout)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("🎯 用户需求输入")
    
    # User preferences input
    user_preferences = st.text_area(
        "请描述您的酒店偏好和需求：",
        placeholder="例如：我希望住在靠近山的地方，环境要安静，适合放松。或者：我需要交通便利的酒店，方便商务出行...",
        height=150,
        value=st.session_state.user_preferences
    )
    
    # Update session state
    st.session_state.user_preferences = user_preferences
    
    # Example preferences
    st.subheader("💡 示例需求")
    example_preferences = [
        "我喜欢靠近山的酒店，环境要安静，适合徒步和放松",
        "我需要交通便利的酒店，靠近市中心，方便商务活动",
        "我想要海边度假酒店，有沙滩和水上运动设施",
        "我偏爱有历史文化特色的酒店，环境要有古典氛围",
        "我需要靠近机场的酒店，有班车服务，适合转机"
    ]
    
    selected_example = st.selectbox("选择示例需求（可选）：", [""] + example_preferences)
    
    if selected_example and st.button("使用示例需求"):
        st.session_state.user_preferences = selected_example
        st.rerun()

    with col2:
        st.header("🔍 推荐结果")
        
        # First recommendation button
        if st.button("🚀 获取基础推荐", type="primary", use_container_width=True):
            if not user_preferences.strip():
                st.error("请先输入您的需求偏好！")
            else:
                with st.spinner("正在分析您的需求并生成推荐..."):
                    try:
                        basic_rec = st.session_state.recommendation_engine.get_basic_recommendations(user_preferences)
                        st.session_state.basic_recommendations = basic_rec
                        st.success("基础推荐已生成！")
                    except Exception as e:
                        st.error(f"生成推荐时出错: {str(e)}")
        
        # Second recommendation button (only show if basic recommendations exist)
        if st.session_state.basic_recommendations:
            if st.button("⭐ 获取增强推荐", type="secondary", use_container_width=True):
                with st.spinner("正在补全酒店信息并优化推荐..."):
                    try:
                        enhanced_rec = st.session_state.recommendation_engine.get_enhanced_recommendations(
                            user_preferences, 
                            st.session_state.basic_recommendations
                        )
                        st.session_state.enhanced_recommendations = enhanced_rec
                        st.success("增强推荐已生成！")
                    except Exception as e:
                        st.error(f"生成增强推荐时出错: {str(e)}")

    # Display recommendations
    st.markdown("---")

    # Create tabs for different recommendation results
    if st.session_state.basic_recommendations or st.session_state.enhanced_recommendations:
        tabs = []
        tab_names = []
        
        if st.session_state.basic_recommendations:
            tab_names.append("📋 基础推荐")
        
        if st.session_state.enhanced_recommendations:
            tab_names.append("⭐ 增强推荐")
        
        if len(tab_names) > 1:
            tab1, tab2 = st.tabs(tab_names)
            
            with tab1:
                st.markdown("### 基于评论分析的基础推荐")
                st.markdown(st.session_state.basic_recommendations)
            
            with tab2:
                st.markdown("### 基于信息补全的增强推荐")
                st.markdown(st.session_state.enhanced_recommendations)
                
                # Show information completion details
                with st.expander("查看信息补全详情"):
                    try:
                        completed_info = st.session_state.recommendation_engine._complete_missing_information()
                        for hotel_id, info in completed_info.items():
                            if info["inferred_features"]:
                                st.write(f"**{info['name']}**:")
                                for feature in info["inferred_features"]:
                                    confidence = info["confidence_scores"].get(feature, 0)
                                    st.write(f"  • {feature}: {confidence}% 置信度")
                    except Exception as e:
                        st.error(f"无法显示补全详情: {str(e)}")
        
        elif st.session_state.basic_recommendations:
            st.markdown("### 📋 基础推荐结果")
            st.markdown(st.session_state.basic_recommendations)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🏨 智能旅游酒店推荐系统 | 基于大语言模型的个性化推荐</p>
        <p>💡 提示：配置您的DeepSeek API密钥以获得更准确的推荐结果</p>
    </div>
    """, unsafe_allow_html=True)

    # Clear recommendations button
    if st.session_state.basic_recommendations or st.session_state.enhanced_recommendations:
        if st.button("🗑️ 清除所有推荐结果"):
            st.session_state.basic_recommendations = None
            st.session_state.enhanced_recommendations = None
            st.rerun()