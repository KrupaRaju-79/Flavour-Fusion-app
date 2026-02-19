import streamlit as st
import google.generativeai as genai
import random

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Flavour Fusion 🍽️",
    page_icon="🍽️",
    layout="centered"
)

# ─────────────────────────────────────────────
# Custom Styling – Dark Theme with High Contrast
# ─────────────────────────────────────────────
st.markdown("""
    <style>
        /* ── Background ── */
        .stApp, .block-container {
            background-color: #1a1a2e !important;
        }

        /* ── All general text ── */
        p, div, span, li, label, .stMarkdown {
            color: #f0f0f0 !important;
        }

        /* ── Headings ── */
        h1 { color: #ff6b35 !important; }
        h2, h3 { color: #ffa07a !important; }

        /* ── Text inputs ── */
        .stTextInput input,
        .stNumberInput input {
            background-color: #16213e !important;
            color: #f0f0f0 !important;
            border: 1.5px solid #ff6b35 !important;
            border-radius: 8px !important;
        }

        /* ── Generate button ── */
        .stButton > button {
            background-color: #ff6b35 !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 10px 25px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            border: none !important;
        }
        .stButton > button:hover {
            background-color: #e55a25 !important;
        }

        /* ── Download button ── */
        .stDownloadButton > button {
            background-color: #0f3460 !important;
            color: #ffffff !important;
            border: 1.5px solid #ff6b35 !important;
            border-radius: 10px !important;
            font-size: 15px !important;
        }
        .stDownloadButton > button:hover {
            background-color: #ff6b35 !important;
        }

        /* ── Alert boxes ── */
        div[role="alert"] {
            background-color: #16213e !important;
            color: #f0f0f0 !important;
            border-left: 4px solid #ff6b35 !important;
            border-radius: 8px !important;
        }
        div[role="alert"] p,
        div[role="alert"] span {
            color: #f0f0f0 !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: #16213e !important;
        }
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            color: #f0f0f0 !important;
        }
        [data-testid="stSidebar"] input {
            background-color: #0f3460 !important;
            color: #f0f0f0 !important;
            border: 1.5px solid #ff6b35 !important;
        }

        /* ── Generated blog output card ── */
        .recipe-card {
            background-color: #16213e;
            color: #f0f0f0;
            padding: 25px 30px;
            border-radius: 14px;
            border: 1.5px solid #ff6b35;
            line-height: 1.9;
            font-size: 15px;
        }

        /* ── Dividers ── */
        hr { border-color: #ff6b35; opacity: 0.3; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.title("🍽️ Flavour Fusion")
st.subheader("AI-Driven Recipe Blogging powered by Gemini 2.5 Flash")
st.markdown("---")

# ─────────────────────────────────────────────
# Sidebar – API Key Input
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Setup")
    st.markdown("**Step 1:** Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
    api_key = st.text_input("🔑 Enter your Gemini API Key", type="password", placeholder="AIza...")
    st.markdown("---")
    st.info("Your API key is **never stored** — it's only used for this session.")

# ─────────────────────────────────────────────
# Programmer Jokes
# ─────────────────────────────────────────────
def get_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?' 😄",
        "Why do Java developers wear glasses? Because they don't C#! 👓",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
        "I told my wife she was drawing her eyebrows too high. She looked surprised... just like my code reviews. 😅",
        "There are only 10 types of people: those who understand binary, and those who don't. 🤓",
        "Why did the developer go broke? Because he used up all his cache! 💸",
    ]
    return random.choice(jokes)

# ─────────────────────────────────────────────
# Recipe Generation Function
# ─────────────────────────────────────────────
def generate_recipe(topic, word_count, api_key):
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.75,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
    )

    prompt = f"""Write a detailed, engaging recipe blog post about "{topic}".
The blog post should be approximately {word_count} words.
Include: an introduction, ingredients list, step-by-step instructions, tips, and a conclusion.
Make it warm, friendly, and easy to follow for home cooks."""

    with st.spinner("🍳 Cooking up your recipe blog..."):
        joke = get_joke()
        st.info(f"😄 **While you wait, here's a joke:** {joke}")

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"❌ Error generating recipe: {str(e)}")
            return None

# ─────────────────────────────────────────────
# Main UI
# ─────────────────────────────────────────────
st.markdown("### 📝 Create Your Recipe Blog")

col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input(
        "🍕 Recipe Topic",
        placeholder="e.g., Vegan Chocolate Cake, Quick Pasta, Gluten-Free Bread...",
    )

with col2:
    word_count = st.number_input(
        "📏 Word Count",
        min_value=200,
        max_value=2000,
        value=800,
        step=100,
    )

st.markdown("")

generate_btn = st.button("✨ Generate Recipe Blog", use_container_width=True)

# ─────────────────────────────────────────────
# Generate and Display
# ─────────────────────────────────────────────
if generate_btn:
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar first!")
    elif not topic.strip():
        st.warning("⚠️ Please enter a recipe topic!")
    else:
        result = generate_recipe(topic.strip(), word_count, api_key)

        if result:
            st.success("✅ Your recipe blog is ready!")
            st.markdown("---")
            st.markdown("### 📖 Generated Recipe Blog")

            # Render inside a styled dark card for clear readability
            html_content = result.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            st.markdown(
                f"<div class='recipe-card'>{html_content}</div>",
                unsafe_allow_html=True
            )

            st.markdown("---")
            st.download_button(
                label="⬇️ Download as Text File",
                data=result,
                file_name=f"{topic.replace(' ', '_')}_recipe_blog.txt",
                mime="text/plain",
                use_container_width=True,
            )

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#aaaaaa;'>Made with ❤️ using Streamlit & Gemini 2.5 Flash</p>",
    unsafe_allow_html=True,
)