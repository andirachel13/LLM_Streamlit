import streamlit as st
from PIL import Image
import io
import time
from google import genai
client = genai.Client(api_key='GeminiAPI')

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
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "gemini_configured" not in st.session_state:
    st.session_state.gemini_configured = False

# Brand archetypes dictionary
BRAND_ARCHETYPES = {
    "hero": "Courageous, inspiring, overcoming challenges",
    "rebel": "Disruptive, revolutionary, anti-establishment", 
    "sage": "Wisdom, truth, expertise, knowledge-sharing",
    "innocent": "Simple, optimistic, nostalgic, pure",
    "explorer": "Adventure, freedom, discovery, independence",
    "magician": "Transformation, vision, making dreams real",
    "everyman": "Relatable, authentic, humble, inclusive",
    "lover": "Intimacy, passion, sensory pleasure, connection",
    "jester": "Playful, humorous, entertaining, irreverent",
    "caregiver": "Compassionate, nurturing, protective, supportive",
    "creator": "Innovation, imagination, self-expression",
    "ruler": "Power, control, exclusivity, leadership"
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

def configure_gemini(api_key):
    try:
        client = genai.Client(api_key=api_key)
        st.session_state.gemini_client = client
        st.session_state.gemini_configured = True
        return True
    except Exception as e:
        st.error(f"Invalid API key: {str(e)}")
        st.session_state.gemini_configured = False
        return False


def generate_creative_brief(image, campaign_goal, brand_archetype, positioning, journey_stage, additional_context=""):
    """Generate creative brief using Gemini"""
    
    try:
        client = st.session_state.gemini_client
        
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
        2. BRAND POSITIONING & MESSAGING
        3. CREATIVE DIRECTION

        Keep the brief professional yet actionable.
        """

        if image:
            # Convert image to bytes for multimodal model
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes = img_bytes.getvalue()

            response = client.models.generate_content(
                model="gemini-2.5-multimodal-preview",
                contents=[prompt, img_bytes]  # ✅ plural 'contents'
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt]  # ✅ plural 'contents'
            )

        return response[0].text  # response is a list of generations

    except Exception as e:
        st.error(f"Error generating creative brief: {str(e)}")
        return None


def generate_campaign_content(brief, content_type):
    """Generate campaign content based on the creative brief"""
    
    try:
        client = st.session_state.gemini_client
        
        content_prompts = {
            "social_media": f"Based on this creative brief, create 5 engaging social media posts:\n{brief}",
            "email_copy": f"Based on this creative brief, write 2 email variations:\n{brief}",
            "ad_copy": f"Based on this creative brief, create 3 ad variations for digital platforms:\n{brief}"
        }
        
        prompt = content_prompts.get(content_type, content_prompts["social_media"])

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt]  # ✅ plural 'contents'
        )

        return response[0].text  # response is a list

    except Exception as e:
        st.error(f"Error generating {content_type}: {str(e)}")
        return None
        

# Demo content
DEMO_BRIEF = """
# 🎯 Creative Brief: Eco-Friendly Coffee Launch

## 1. TARGET AUDIENCE PERSONA
**Primary Audience:** Millennials & Gen Z (25-40 years old)
- **Demographics:** Urban professionals, college-educated, $60K+ annual income
- **Psychographics:** Value sustainability, health-conscious, tech-savvy, experience-driven
- **Behaviors:** Active on social media, research purchases online, prefer authentic brands

## 2. BRAND POSITIONING & MESSAGING
**Key Messaging Pillars:**
1. **Sustainable innovation** that doesn't compromise quality
2. **Empowering customers** to make conscious choices  
3. **Building community** around shared values

**Brand Voice:** Authentic, Inspiring, Knowledgeable
**Unique Selling Proposition:** Premium organic coffee with carbon-neutral supply chain

## 3. CREATIVE DIRECTION
**Visual Style:** Clean, natural aesthetics with bold accent colors
**Content Themes:** Sustainability stories, user-generated content, educational content
**Call-to-Action Strategy:** Focus on community building and trial offers

---

*Note: This is a demo brief. Enter your Gemini API key to generate personalized AI-powered creative briefs.*
"""

DEMO_SOCIAL_MEDIA = """
## 📱 Social Media Posts

**Post 1: Brand Story**
🎯 **Visual:** Behind-the-scenes of coffee farming
💬 **Caption:** "From our sustainable farms to your morning cup - every bean tells a story of positive impact. ☕️🌱 #SustainableCoffee #EcoFriendly"
🏷️ **Hashtags:** #CoffeeLovers #EcoWarrior #MorningRitual

**Post 2: Product Highlight**  
🎯 **Visual:** Artistic shot of coffee packaging
💬 **Caption:** "Packaged with purpose, brewed with passion. Our compostable packaging is just the beginning. ♻️"
🏷️ **Hashtags:** #ZeroWaste #EcoPackaging #GreenLiving

**Post 3: Community Engagement**
🎯 **Visual:** User-generated content collage
💬 **Caption:** "How do you take your sustainable brew? Share your morning routine with us! 👇"
🏷️ **Hashtags:** #CoffeeCommunity #SustainableLiving #ShareYourBrew
"""

DEMO_EMAIL_COPY = """
## 📧 Email Campaign

**Variation 1: Welcome Series**
**Subject:** Start Your Sustainable Coffee Journey ☕️  
**Preheader:** Discover how your morning brew can make a difference

**Body:**
Welcome to the revolution! We're thrilled to have you join our community of conscious coffee lovers. 

✨ **What makes us different:**
• Carbon-neutral supply chain
• Direct trade with farmers
• 100% compostable packaging

**CTA:** [Explore Our Blends]

---

**Variation 2: Educational Content**
**Subject:** The Truth About Sustainable Coffee 🌱
**Preheader:** 5 things every coffee drinker should know

**Body:**
Did you know traditional coffee farming contributes to deforestation? We're changing that, one cup at a time.

📚 **In this email:**
- The impact of shade-grown coffee
- How direct trade supports farmers
- Our sustainability certifications

**CTA:** [Learn More About Our Mission]
"""

# Main application
def main():
    st.title("🎨 Creative Brief Generator Pro")
    st.markdown("Generate strategic marketing briefs and campaign content using AI")
    
    # Try to get API key from secrets first
    try:
        secrets_api_key = st.secrets.get("api_key")
        if secrets_api_key and not st.session_state.api_key:
            if configure_gemini(secrets_api_key):
                st.session_state.api_key = secrets_api_key
                st.session_state.demo_mode = False
    except:
        pass  # No secrets available, use manual input
    
    # API Key input in sidebar
    with st.sidebar:
        st.header("🔑 Configuration")
        
        st.markdown("""
        **Get your free API key:**
        1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy and paste below
        """)
        
        api_key_input = st.text_input(
            "Enter your Gemini API Key:",
            type="password",
            placeholder="AIzaSy...",
            help="Your key stays in your browser and is never stored",
            value=st.session_state.api_key if st.session_state.api_key else ""
        )
        
        if api_key_input and api_key_input != st.session_state.api_key:
            if configure_gemini(api_key_input):
                st.session_state.api_key = api_key_input
                st.session_state.demo_mode = True
                st.success("✅ API key configured successfully!")
            else:
                st.session_state.api_key = ""
        
        st.markdown("---")
        st.header("🎯 Campaign Parameters")
        
        brand_archetype = st.selectbox(
            "Brand Archetype",
            options=list(BRAND_ARCHETYPES.keys()),
            format_func=lambda x: f"{x.title()} - {BRAND_ARCHETYPES[x]}",
            index=3  # Default to Innocent
        )
        
        positioning = st.selectbox(
            "Competitive Positioning",
            options=list(POSITIONING_STRATEGIES.keys()),
            format_func=lambda x: f"{x.replace('-', ' ').title()} - {POSITIONING_STRATEGIES[x]}",
            index=4  # Default to Customer Champion
        )
        
        journey_stage = st.selectbox(
            "Customer Journey Stage",
            options=list(JOURNEY_STAGES.keys()),
            format_func=lambda x: f"{x.title()} - {JOURNEY_STAGES[x]}",
            index=0  # Default to Awareness
        )
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Use clear, specific campaign goals
        - Upload product images for visual analysis
        - Experiment with different brand archetypes
        - No API key? Use demo mode to explore features
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Campaign Input")
        
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
            placeholder="Example: Launch new eco-friendly coffee brand to millennials who value sustainability and premium quality...",
            height=100,
            value="Launch sustainable coffee brand targeting eco-conscious millennials" if not st.session_state.api_key else ""
        )
        
        additional_context = st.text_area(
            "Additional Context (Optional)",
            placeholder="Key features, unique benefits, competitors, budget constraints, timeline...",
            height=80
        )
        
        # Generate buttons
        col1a, col1b = st.columns(2)
        
        with col1a:
            if st.button(
                "🚀 Generate Creative Brief", 
                type="primary", 
                use_container_width=True,
                disabled=not st.session_state.gemini_configured
            ):
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
                                "content": f"Here's your creative brief based on **{brand_archetype}** archetype and **{positioning}** positioning:"
                            })
                            st.rerun()
        
        with col1b:
            if not st.session_state.gemini_configured:
                if st.button("👀 View Demo", use_container_width=True):
                    st.session_state.demo_mode = True
                    st.session_state.creative_brief = DEMO_BRIEF
                    st.rerun()
        
        # API key message
        if not st.session_state.gemini_configured:
            st.info("""
            **🔑 API Key Required for AI Generation**
            - Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey)
            - No credit card required
            - Or explore features with Demo Mode
            """)
        else:
            st.success("✅ Gemini AI is configured and ready!")
    
    with col2:
        st.subheader("📋 Creative Brief & Content")
        
        # Display creative brief
        if st.session_state.creative_brief:
            with st.expander("🎯 Strategic Creative Brief", expanded=True):
                st.markdown(st.session_state.creative_brief)
            
            # Content generation options
            st.subheader("🎨 Generate Campaign Content")
            content_type = st.radio(
                "Select content type:",
                ["social_media", "email_copy", "ad_copy"],
                format_func=lambda x: x.replace('_', ' ').title(),
                horizontal=True
            )
            
            if st.session_state.gemini_configured:
                if st.button(f"Generate {content_type.replace('_', ' ').title()}", use_container_width=True):
                    with st.spinner(f"Creating {content_type.replace('_', ' ')}..."):
                        content = generate_campaign_content(
                            st.session_state.creative_brief, 
                            content_type
                        )
                        
                        if content:
                            st.session_state.campaign_content[content_type] = content
                            st.rerun()
            else:
                # Show demo content
                demo_content = {
                    "social_media": DEMO_SOCIAL_MEDIA,
                    "email_copy": DEMO_EMAIL_COPY,
                    "ad_copy": "**Demo Ad Copy:** Enter API key to generate personalized ad variations..."
                }
                
                with st.expander(f"📝 Demo {content_type.replace('_', ' ').title()}", expanded=True):
                    st.markdown(demo_content[content_type])
                    st.info("🔑 Enter API key to generate personalized content")
            
            # Display previously generated content
            for content_type, content in st.session_state.campaign_content.items():
                with st.expander(f"📝 {content_type.replace('_', ' ').title()}"):
                    st.markdown(content)
        
        else:
            st.info("👈 Enter campaign details and generate a creative brief to get started")
            
            # Show feature preview
            with st.expander("🚀 What you can create:"):
                st.markdown("""
                **With AI Generation:**
                - 📋 Strategic creative briefs
                - 📱 Social media content
                - 📧 Email campaigns  
                - 🎯 Ad copy variations
                - 💬 Strategy consulting
                
                **Try the demo to see examples!**
                """)
    
    # Chat interface for follow-up questions (only with API key)
    if st.session_state.gemini_configured and st.session_state.creative_brief:
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
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        chat_context = f"""
                        You are a senior marketing strategist. Based on this creative brief, answer the user's question.
                        
                        CREATIVE BRIEF:
                        {st.session_state.creative_brief}
                        
                        USER QUESTION: {prompt}
                        
                        Provide strategic, actionable advice based on the brief above.
                        """
                        
                        response = model.generate_content(chat_context)
                        
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                        
                    except Exception as e:
                        st.error(f"Error in chat: {str(e)}")

if __name__ == "__main__":
    main()
