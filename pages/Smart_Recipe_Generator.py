import streamlit as st
from ai_recipe import generate_recipe
from db import SessionLocal, Recipe
import base64

# Page config
st.set_page_config(page_title="Smart Recipe Generator", layout="wide")

# Background image function
def add_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("assets/main_bg.jpg")

# Custom CSS styling
st.markdown("""
    <style>
    .custom-title {
        color: white;
        font-family: 'Brush Script MT', cursive;
        font-size: 60px;
        text-align: center;
        margin-top: -30px;
        margin-bottom: 20px;
    }

    label, .stSelectbox label, .stTextArea label, .stTextInput label,
    .stMarkdown p, .stMarkdown h3 {
        color: white !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px !important;
        font-weight: bold;
    }

    .stImage + div > p, .stImage + div > div {
        color: white !important;
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px !important;
    }

    .stTextArea textarea,
    .stTextInput input {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        font-size: 16px !important;
        font-family: 'Segoe UI', sans-serif !important;
        border: 1px solid #ccc !important;
        border-radius: 10px !important;
    }

    ::placeholder {
        color: #ccc !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        font-size: 16px !important;
        font-family: 'Segoe UI', sans-serif !important;
        border-radius: 10px !important;
        border: 1px solid #ccc !important;
    }

    .stSelectbox div[data-baseweb="popover"] {
        background-color: rgba(30, 30, 30, 0.95) !important;
        color: white !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    .stTabs [role="tab"] {
        color: white !important;
        font-weight: 600;
        font-size: 16px;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #f39c12 !important;
        color: #f39c12 !important;
    }

    button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown('<div class="custom-title">Smart Recipe Generator 🍳</div>', unsafe_allow_html=True)

# Check if user is logged in
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login from the homepage.")
    st.stop()

user = st.session_state.user

# Initialize state
if "last_input_ingredients" not in st.session_state:
    st.session_state.last_input_ingredients = ""
if "last_recipe" not in st.session_state:
    st.session_state.last_recipe = None

col1, col2 = st.columns([1, 3])

# ----------------- LEFT PROFILE SECTION ----------------- #
with col1:
    st.markdown("### 👤 Profile")
    st.image(user.profile_pic if user.profile_pic else "assets/default_profile.png", width=150)
    st.write(f"**Username:** {user.name}")
    st.write(f"**Phone Number:** {user.phone}")
    st.write(f"**Email ID:** {user.email}")

    if st.button("Logout"):
        st.session_state.user = None
        st.switch_page("app.py")

# ----------------- MAIN RECIPE SECTION ----------------- #
with col2:
    tabs = st.tabs(["Home", "Saved Recipes"])

    # ---------------- Home Tab ---------------- #
    with tabs[0]:
        ingredients_text = st.text_area(
            "Enter Ingredients (comma-separated)",
            placeholder="e.g. tomato, onion, garlic, rice",
            key="ingredient_input"
        )
        category = st.selectbox("Select Category", ["Veg", "Non-Veg"], key="category_selector")
        cuisine = st.selectbox("Cuisine", ["Any", "Indian", "Italian", "Chinese", "Mexican"], key="cuisine_selector")
        health_pref = st.selectbox("Health Preference", ["None", "Low Calorie", "High Protein", "Vegan"], key="health_selector")

        if st.button("Generate Recipe", key="generate_button"):
            if ingredients_text.strip():
                st.session_state.last_input_ingredients = ingredients_text.strip()
                st.session_state.last_recipe = generate_recipe(
                    st.session_state.last_input_ingredients,
                    category,
                    cuisine,
                    health_pref
                )
                st.rerun()
            else:
                st.warning("Please enter some ingredients first.")

        # Show recipe + regenerate/save if recipe exists
        if st.session_state.last_recipe:
            st.text_area("Generated Recipe", value=st.session_state.last_recipe, height=300, key="recipe_display_unique")

            col_gen, col_save = st.columns([1, 1])

            with col_gen:
                if st.button("🔁 Regenerate Recipe", key="regenerate_button"):
                    st.session_state.last_recipe = generate_recipe(
                        st.session_state.last_input_ingredients,
                        category,
                        cuisine,
                        health_pref
                    )
                    st.rerun()

            with col_save:
                if st.button("📂 Save Recipe", key="save_button"):
                    db = SessionLocal()
                    new_recipe = Recipe(
                        user_id=user.id,
                        input_text=st.session_state.last_input_ingredients,
                        category=category,
                        cuisine=cuisine,
                        health_pref=health_pref,
                        recipe_output=st.session_state.last_recipe
                    )
                    db.add(new_recipe)
                    db.commit()
                    db.close()
                    st.success("✅ Recipe saved successfully!")

    # ---------------- Saved Recipes Tab ---------------- #
    with tabs[1]:
        db = SessionLocal()
        recipes = db.query(Recipe).filter(Recipe.user_id == user.id).all()

        if not recipes:
            st.info("ℹ️ No recipes saved yet.")
        else:
            recipe_titles = [
                r.recipe_output.strip().split('\n')[0] if r.recipe_output else f"{r.category} Recipe"
                for r in recipes
            ]

            selected = st.selectbox("Select a Saved Recipe", recipe_titles, key="saved_dropdown")
            selected_index = recipe_titles.index(selected)
            selected_recipe = recipes[selected_index]

            st.markdown("### 🍽️ " + selected)
            st.markdown(f"**Ingredients Used:** {selected_recipe.input_text}")
            st.markdown(f"**Category:** {selected_recipe.category}")
            st.markdown(f"**Cuisine:** {selected_recipe.cuisine}")
            st.markdown(f"**Health Preference:** {selected_recipe.health_pref}")
            st.text_area("Saved Recipe", value=selected_recipe.recipe_output, height=300, key="saved_recipe_area")

            if st.button("🗑 Delete This Recipe", key="delete_button"):
                db.delete(selected_recipe)
                db.commit()
                db.close()
                st.success("❌ Recipe deleted successfully!")
                st.rerun()
