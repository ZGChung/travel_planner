import streamlit as st
import json
from recommendation_engine import RecommendationEngine

# Page configuration
st.set_page_config(
    page_title="AI Hotel Recommendation System",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# (Sidebar uses default Streamlit style; no custom CSS applied)

# Initialize session state
if "recommendation_engine" not in st.session_state:
    st.session_state.recommendation_engine = RecommendationEngine()

if "basic_recommendations" not in st.session_state:
    st.session_state.basic_recommendations = None

if "enhanced_recommendations" not in st.session_state:
    st.session_state.enhanced_recommendations = None

if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = ""

if "selected_hotel" not in st.session_state:
    st.session_state.selected_hotel = None

if "show_hotel_detail" not in st.session_state:
    st.session_state.show_hotel_detail = False

# Main title
st.title("🏨 AI Hotel Recommendation System")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ System Configuration")

    # Display current configuration
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        st.subheader("Current Configuration")
        st.write(f"**LLM Provider**: {config.get('llm_provider', 'deepseek')}")
        st.write(f"**Model**: {config.get('model_name', 'deepseek-chat')}")

        api_key = config.get("deepseek_api_key", "")
        if api_key == "YOUR_DEEPSEEK_API_KEY_HERE":
            st.warning("⚠️ Please configure your API key in config.json")
            st.info("💡 Currently using simulation response mode")
        else:
            st.success("✅ API key configured")

    except Exception as e:
        st.error(f"Configuration file read error: {str(e)}")

    st.markdown("---")

    # Hotel data summary
    st.subheader("📊 Data Overview")
    hotels = st.session_state.recommendation_engine.hotels
    st.write(f"**Number of Hotels**: {len(hotels)}")

    total_reviews = sum(len(hotel.get("reviews", [])) for hotel in hotels)
    st.write(f"**Total Reviews**: {total_reviews}")

    # Show hotel list with clickable names
    with st.expander("View All Hotels"):
        for hotel in hotels:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(
                    f"📍 {hotel['name']}",
                    key=f"hotel_{hotel['id']}",
                    help="Click to view details",
                ):
                    st.session_state.selected_hotel = hotel["id"]
                    st.session_state.show_hotel_detail = True
                    st.rerun()
            with col2:
                st.write(f"({len(hotel.get('reviews', []))} reviews)")

# Check if hotel detail should be shown
if st.session_state.show_hotel_detail and st.session_state.selected_hotel:
    # Show hotel detail page
    selected_hotel_data = None
    for hotel in hotels:
        if hotel["id"] == st.session_state.selected_hotel:
            selected_hotel_data = hotel
            break

    if selected_hotel_data:
        # Hotel detail header
        col1, col2 = st.columns([4, 1])
        with col1:
            st.header(f"🏨 {selected_hotel_data['name']}")
        with col2:
            if st.button("🔙 Return to Home", type="secondary"):
                st.session_state.show_hotel_detail = False
                st.session_state.selected_hotel = None
                st.rerun()

        st.markdown("---")

        # Hotel basic information
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📍 Basic Information")
            st.write(f"**Address**: {selected_hotel_data['address']}")
            st.write(
                f"**Coordinates**: {selected_hotel_data['coordinates']['lat']}, {selected_hotel_data['coordinates']['lng']}"
            )

            # Tags information
            tags = selected_hotel_data.get("tags", {})
            st.subheader("🏷️ Hotel Tags")

            col_tag1, col_tag2 = st.columns(2)
            with col_tag1:
                st.write(f"⭐ **Star Rating**: {tags.get('star_rating', 'N/A')}")
                st.write(f"💰 **Price Range**: {tags.get('price_range', 'N/A')}")

            with col_tag2:
                amenities = tags.get("amenities", [])
                if amenities:
                    st.write("🎯 **Amenities & Services**:")
                    for amenity in amenities:
                        st.write(f"  • {amenity}")

            # Special features
            special_features = []
            for key, value in tags.items():
                if (
                    key not in ["star_rating", "price_range", "amenities"]
                    and value is True
                ):
                    special_features.append(key)

            if special_features:
                st.write("✨ **Special Features**:")
                for feature in special_features:
                    st.write(f"  • {feature}")

        with col2:
            # Review statistics
            reviews = selected_hotel_data.get("reviews", [])
            if reviews:
                st.subheader("📊 Review Statistics")
                avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
                st.metric(
                    "Average Rating", f"{avg_rating:.1f}/5", f"{len(reviews)} reviews"
                )

                # Rating distribution
                rating_counts = {}
                for r in reviews:
                    rating = r["rating"]
                    rating_counts[rating] = rating_counts.get(rating, 0) + 1

                st.write("**Rating Distribution**:")
                for rating in sorted(rating_counts.keys(), reverse=True):
                    count = rating_counts[rating]
                    percentage = (count / len(reviews)) * 100
                    st.write(f"{rating}⭐: {count} reviews ({percentage:.1f}%)")

        st.markdown("---")

        # Reviews section
        st.subheader("💬 User Reviews")

        if reviews:
            # Review filter
            col1, col2 = st.columns([2, 1])
            with col1:
                rating_filter = st.selectbox(
                    "Filter by Rating",
                    [
                        "All Ratings",
                        "5 Stars",
                        "4 Stars",
                        "3 Stars",
                        "2 Stars",
                        "1 Star",
                    ],
                    key="rating_filter",
                )
            with col2:
                sort_order = st.selectbox(
                    "Sort By",
                    ["Highest to Lowest", "Lowest to Highest"],
                    key="sort_order",
                )

            # Filter and sort reviews
            filtered_reviews = reviews.copy()
            if rating_filter != "All Ratings":
                target_rating = int(rating_filter[0])
                filtered_reviews = [
                    r for r in filtered_reviews if r["rating"] == target_rating
                ]

            if sort_order == "Highest to Lowest":
                filtered_reviews.sort(key=lambda x: x["rating"], reverse=True)
            else:
                filtered_reviews.sort(key=lambda x: x["rating"])

            # Display reviews
            for i, review in enumerate(filtered_reviews):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{review['user']}**")
                    with col2:
                        st.write(f"{'⭐' * review['rating']} ({review['rating']}/5)")

                    st.write(review["text"])

                    if i < len(filtered_reviews) - 1:
                        st.markdown("---")
        else:
            st.info("No user reviews yet")

    else:
        st.error("Selected hotel information not found")
        if st.button("Return to Home"):
            st.session_state.show_hotel_detail = False
            st.session_state.selected_hotel = None
            st.rerun()

else:
    # Main content area (original layout)

    st.header("🎯 User Requirements Input")

    # User preferences input
    user_preferences = st.text_area(
        "Please describe your hotel preferences and requirements:",
        placeholder="Example: I want to stay near mountains, in a quiet environment suitable for relaxation. Or: I need a hotel with convenient transportation for business travel...",
        height=150,
        value=st.session_state.user_preferences,
    )

    # Update session state
    st.session_state.user_preferences = user_preferences

    # Example preferences
    st.subheader("💡 Example Requirements")
    example_preferences = [
        "I like hotels near mountains, with quiet environment, suitable for hiking and relaxation",
        "I need a hotel with convenient transportation, close to city center, suitable for business activities",
        "I want a beachfront resort with beach access and water sports facilities",
        "I prefer hotels with historical and cultural character, with classical atmosphere",
        "I need a hotel near the airport with shuttle service, suitable for layovers",
    ]

    selected_example = st.selectbox(
        "Select Example Requirements (Optional):", example_preferences
    )

    if selected_example and st.button("Use Example Requirements"):
        st.session_state.user_preferences = selected_example
        st.rerun()

    st.header("🔍 Recommendations")

    # First recommendation button
    if st.button(
        "🚀 Get Basic Recommendations", type="primary", use_container_width=True
    ):
        if not user_preferences.strip():
            st.error("Please enter your preferences first!")
        else:
            with st.spinner(
                "Analyzing your requirements and generating recommendations..."
            ):
                try:
                    basic_rec = st.session_state.recommendation_engine.get_basic_recommendations(
                        user_preferences
                    )
                    st.session_state.basic_recommendations = basic_rec
                    st.success("Basic recommendations generated!")
                except Exception as e:
                    st.error(f"Error generating recommendations: {str(e)}")

    # Second recommendation button (only show if basic recommendations exist)
    if st.session_state.basic_recommendations:
        if st.button(
            "⭐ Get Enhanced Recommendations",
            type="secondary",
            use_container_width=True,
        ):
            with st.spinner(
                "Completing hotel information and optimizing recommendations..."
            ):
                try:
                    enhanced_rec = st.session_state.recommendation_engine.get_enhanced_recommendations(
                        user_preferences, st.session_state.basic_recommendations
                    )
                    st.session_state.enhanced_recommendations = enhanced_rec
                    st.success("Enhanced recommendations generated!")
                except Exception as e:
                    st.error(f"Error generating enhanced recommendations: {str(e)}")

    # Display recommendations
    st.markdown("---")

    # Create tabs for different recommendation results
    if (
        st.session_state.basic_recommendations
        or st.session_state.enhanced_recommendations
    ):
        tabs = []
        tab_names = []

        if st.session_state.basic_recommendations:
            tab_names.append("📋 Basic Recommendations")

        if st.session_state.enhanced_recommendations:
            tab_names.append("⭐ Enhanced Recommendations")

        if len(tab_names) > 1:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Review-Based Basic Recommendations")
                st.markdown(st.session_state.basic_recommendations)

            with col2:
                st.markdown("### Information-Enhanced Recommendations")
                st.markdown(st.session_state.enhanced_recommendations)

        elif st.session_state.basic_recommendations:
            st.markdown("### 📋 Basic Recommendation Results")
            st.markdown(st.session_state.basic_recommendations)

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #666;'>
        <p>🏨 AI Hotel Recommendation System | Personalized Recommendations Powered by Large Language Models</p>
        <p>💡 Tip: Configure your DeepSeek API key for more accurate recommendation results</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Clear recommendations button
    if (
        st.session_state.basic_recommendations
        or st.session_state.enhanced_recommendations
    ):
        if st.button("🗑️ Clear All Recommendations"):
            st.session_state.basic_recommendations = None
            st.session_state.enhanced_recommendations = None
            st.rerun()
