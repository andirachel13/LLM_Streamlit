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
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
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

# Main application
def main():
    st.title("🎨 Creative Brief Generator Pro")
    st.markdown("Generate strategic marketing briefs and campaign content using AI")
    
    # Sidebar for parameters
    with st.sidebar:
        st.header("Campaign Parameters")
        
        brand_archetype = st.selectbox(
            "Brand Archetype",
            options=list(BRAND_ARCHETYPES.keys()),
            format_func=lambda x: f"{x.title()} - {BRAND_ARCHETYPES[x].split(' - ')[0]}"
        )
        
        positioning = st.selectbox(
            "Competitive Positioning",
            options=list(POSITIONING_STRATEGIES.keys()),
            format_func=lambda x: f"{x.replace('-', ' ').title()} - {POSITIONING_STRATEGIES[x]}"
        )
        
        journey_stage = st.selectbox(
            "Customer Journey Stage",
            options=list(JOURNEY_STAGES.keys()),
            format_func=lambda x: f"{x.title()} - {JOURNEY_STAGES[x].split(' - ')[0]}"
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This tool helps marketers create strategic creative briefs 
        using proven marketing frameworks and AI-powered insights.
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Campaign Input")
        
        # Image upload
        uploaded_image = st.file_uploader(
            "Upload Product/Inspiration Image (Optional)",
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image of your product, brand, or inspiration"
        )
        
        image = None
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Campaign details
        campaign_goal = st.text_area(
            "Campaign Goal & Context",
            placeholder="Example: Launch new eco-friendly coffee brand to millennials who value sustainability...",
            height=100
        )
        
        additional_context = st.text_area(
            "Additional Context (Optional)",
            placeholder="Key features, unique benefits, competitors, special considerations...",
            height=80
        )
        
        # Generate button
        if st.button("🚀 Generate Creative Brief", type="primary", use_container_width=True):
            if not campaign_goal:
                st.warning("Please enter a campaign goal")
            else:
                with st.spinner("Creating your strategic creative brief..."):
                    brief = generate_creative_brief(
                        image, campaign_goal, brand_archetype, 
                        positioning, journey_stage, additional_context
                    )
                    
                    if brief:
                        st.session_state.creative_brief = brief
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"Here's your creative brief based on {brand_archetype} archetype and {positioning} positioning:"
                        })
                        st.rerun()
    
    with col2:
        st.subheader("Creative Brief & Content")
        
        # Display creative brief
        if st.session_state.creative_brief:
            with st.expander("📋 Strategic Creative Brief", expanded=True):
                st.markdown(st.session_state.creative_brief)
            
            # Content generation options
            st.subheader("Generate Campaign Content")
            content_type = st.radio(
                "Select content type:",
                ["social_media", "email_copy", "ad_copy"],
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            if st.button(f"Generate {content_type.replace('_', ' ').title()}", use_container_width=True):
                with st.spinner(f"Creating {content_type.replace('_', ' ')}..."):
                    content = generate_campaign_content(
                        st.session_state.creative_brief, 
                        content_type
                    )
                    
                    if content:
                        st.session_state.campaign_content[content_type] = content
                        
                        with st.expander(f"📝 Generated {content_type.replace('_', ' ').title()}", expanded=True):
                            st.markdown(content)
            
            # Display previously generated content
            for content_type, content in st.session_state.campaign_content.items():
                with st.expander(f"📝 {content_type.replace('_', ' ').title()} (Previously Generated)"):
                    st.markdown(content)
        
        else:
            st.info("👈 Enter campaign details and generate a creative brief to get started")
    
    # Chat interface for follow-up questions
    st.markdown("---")
    st.subheader("💬 Creative Strategy Chat")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask questions about your creative strategy..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    
                    chat_context = f"""
                    Creative Brief Context:
                    {st.session_state.creative_brief if st.session_state.creative_brief else 'No brief generated yet'}
                    
                    Current conversation:
                    """
                    
                    full_prompt = f"{chat_context}\n\nUser question: {prompt}"
                    response = model.generate_content(full_prompt)
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
                except Exception as e:
                    st.error(f"Error in chat: {str(e)}")

if __name__ == "__main__":
    main()
