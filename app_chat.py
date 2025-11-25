
import streamlit as st
import os
from PIL import Image
import io
import time

# Page configuration
st.set_page_config(
    page_title="Creative Brief Generator Pro",
    page_icon="🎨",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "creative_brief" not in st.session_state:
    st.session_state.creative_brief = None
if "campaign_content" not in st.session_state:
    st.session_state.campaign_content = {}

# Configure Gemini
def configure_gemini():
    api_key = st.secrets.get("GeminiAPI", os.getenv("GeminiAPI"))
    if not api_key:
        st.error("Please set GEMINI_API_KEY in secrets or environment variables")
        st.stop()
    genai.configure(api_key=api_key)

configure_gemini()

# Brand archetypes dictionary
BRAND_ARCHETYPES = {
    "hero": "Courageous, inspiring, overcoming challenges - brands like Nike, FedEx",
    "rebel": "Disruptive, revolutionary, anti-establishment - brands like Harley-Davidson, Apple",
    "sage": "Wisdom, truth, expertise, knowledge-sharing - brands like Google, BBC",
    "innocent": "Simple, optimistic, nostalgic, pure - brands like Coca-Cola, Dove",
    "explorer": "Adventure, freedom, discovery, independence - brands like Jeep, Patagonia",
    "magician": "Transformation, vision, making dreams real - brands like Disney, Dyson",
    "everyman": "Relatable, authentic, humble, inclusive - brands like IKEA, eBay",
    "lover": "Intimacy, passion, sensory pleasure, connection - brands like Victoria's Secret, Godiva",
    "jester": "Playful, humorous, entertaining, irreverent - brands like Old Spice, Skittles",
    "caregiver": "Compassionate, nurturing, protective, supportive - brands like Johnson & Johnson, UNICEF",
    "creator": "Innovation, imagination, self-expression - brands like Lego, Crayola",
    "ruler": "Power, control, exclusivity, leadership - brands like Rolex, Mercedes-Benz"
}

# Positioning strategies
POSITIONING_STRATEGIES = {
    "market-leader": "Confident, authoritative, setting industry standards",
    "challenger": "Disruptive, comparative, highlighting competitor weaknesses",
    "niche-specialist": "Expert, focused, deep domain knowledge",
    "value-innovator": "Game-changing benefits, unique value proposition",
    "customer-champion": "Empathetic, user-focused, community-driven"
}

# Customer journey stages
JOURNEY_STAGES = {
    "awareness": "Top-of-funnel: Educational content, problem awareness",
    "consideration": "Middle-of-funnel: Comparison, feature-benefit analysis",
    "conversion": "Bottom-of-funnel: Urgency, clear CTAs, purchase-focused",
    "retention": "Post-purchase: Loyalty, community, ongoing value",
    "advocacy": "Advocacy: Social proof, testimonials, referrals"
}

def generate_creative_brief(image, campaign_goal, brand_archetype, positioning, journey_stage, additional_context=""):
    """Generate creative brief using Gemini"""

    try:
        # Use multimodal model if image is provided
        if image:
            model = genai.GenerativeModel('gemini-pro-vision')

            prompt = f"""
            As a senior marketing strategist, analyze the provided image and generate a comprehensive creative brief.

            CAMPAIGN CONTEXT:
            - Primary Goal: {campaign_goal}
            - Brand Archetype: {brand_archetype} - {BRAND_ARCHETYPES[brand_archetype]}
            - Market Positioning: {positioning} - {POSITIONING_STRATEGIES[positioning]}
            - Target Journey Stage: {journey_stage} - {JOURNEY_STAGES[journey_stage]}
            - Additional Context: {additional_context}

            Please provide a structured creative brief with these sections:

            1. VISUAL ANALYSIS & MOOD
            - Describe the visual style, colors, and mood of the image
            - Key visual elements and their emotional impact

            2. TARGET AUDIENCE PERSONA
            - Demographics, psychographics, and behaviors
            - Core needs and pain points

            3. BRAND POSITIONING & MESSAGING
            - Key messaging pillars (3-4 core messages)
            - Brand voice and tone descriptors
            - Unique selling proposition

            4. CREATIVE DIRECTION
            - Visual style recommendations
            - Content themes and storytelling approach
            - Call-to-action strategy

            Keep the brief professional yet actionable. Focus on strategic insights.
            """

            response = model.generate_content([prompt, image])
        else:
            model = genai.GenerativeModel('gemini-2.5-flash')

            prompt = f"""
            As a senior marketing strategist, generate a comprehensive creative brief.

            CAMPAIGN CONTEXT:
            - Primary Goal: {campaign_goal}
            - Brand Archetype: {brand_archetype} - {BRAND_ARCHETYPES[brand_archetype]}
            - Market Positioning: {positioning} - {POSITIONING_STRATEGIES[positioning]}
            - Target Journey Stage: {journey_stage} - {JOURNEY_STAGES[journey_stage]}
            - Additional Context: {additional_context}

            Please provide a structured creative brief with these sections:

            1. TARGET AUDIENCE PERSONA
            - Demographics, psychographics, and behaviors
            - Core needs and pain points

            2. BRAND POSITIONING & MESSAGING
            - Key messaging pillars (3-4 core messages)
            - Brand voice and tone descriptors
            - Unique selling proposition

            3. CREATIVE DIRECTION
            - Visual style recommendations (since no image provided)
            - Content themes and storytelling approach
            - Call-to-action strategy

            4. IMPLEMENTATION GUIDELINES
            - Channel-specific recommendations
            - Success metrics to track

            Keep the brief professional yet actionable. Focus on strategic insights.
            """

            response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        st.error(f"Error generating creative brief: {str(e)}")
        return None

def generate_campaign_content(brief, content_type):
    """Generate specific campaign content based on the creative brief"""

    try:
        model = genai.GenerativeModel('gemini-pro')

        content_prompts = {
            "social_media": f"""
            Based on this creative brief, create 5 engaging social media posts for Instagram/LinkedIn:

            {brief}

            Create posts that:
            - Match the brand voice and target audience
            - Include relevant hashtags
            - Have compelling captions
            - Specify visual suggestions for each post
            """,

            "email_copy": f"""
            Based on this creative brief, write 2 email variations:

            {brief}

            Include:
            - Compelling subject lines
            - Engaging preheader text
            - Clear body copy with benefits
            - Strong call-to-action
            - Personalization suggestions
            """,

            "ad_copy": f"""
            Based on this creative brief, create 3 ad variations for digital platforms:

            {brief}

            For each ad include:
            - Headline (max 40 characters)
            - Primary text (max 125 characters)
            - Description (max 150 characters)
            - Call-to-action button text
            - Target audience suggestions
            """
        }

        prompt = content_prompts.get(content_type, content_prompts["social_media"])
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        st.error(f"Error generating {content_type}: {str(e)}")
        return None
