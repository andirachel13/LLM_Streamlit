
import streamlit as st
import os
from PIL import Image
import io
import time

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
