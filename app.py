import streamlit as st
import google.generativeai as genai

# Setup API
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# --- NEW SELF-HEALING MODEL PICKER ---
try:
    # Try to use the standard 1.5 Flash first
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    # Test it with a tiny call to make sure it exists
    model.generate_content("ping") 
except Exception:
    # If that fails, it finds the first model your key IS allowed to use
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model = genai.GenerativeModel(available_models[0])
    st.sidebar.info(f"Using model: {available_models[0]}")


# --- CONFIGURATION ---
# In Streamlit Cloud, you set this in 'Secrets'
api_key = st.secrets["GOOGLE_API_KEY"] 
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.0-flash')
st.set_page_config(page_title="Aussie Job-Ready AI", page_icon="🦘")

st.title("🦘 Aussie Job-Ready AI")
st.caption("Tailored for International Students in Australia")

# --- TOOL SELECTION ---
tool = st.sidebar.selectbox("Select Tool", ["STAR Position Description", "Resume Tailor", "Cover Letter"])

# --- INPUT FIELDS ---
job_desc = st.text_area("Paste the Job Description (Selection Criteria):")
user_notes = st.text_area("Paste your experience or rough notes (What did you actually do?):")

if st.button("Generate Professional Content"):
    if not job_desc or not user_notes:
        st.warning("Please fill in both fields.")
    else:
        with st.spinner("Writing for the Aussie market..."):
            # The "Secret Sauce" Prompts
            prompts = {
                "STAR Position Description": f"""Act as an Australian Career Coach. Rewrite this experience into a high-impact STAR response (Situation, Task, Action, Result) for this job: {job_desc}. 
                Follow these Aussie rules:
                1. Situation & Task: Max 15% of total text.
                2. Action: 70% of total text. Use high-impact verbs (Managed, Spearheaded, Implemented).
                3. Result: 15% of total text. Must be quantifiable (%, $, or hours saved).
                Experience: {user_notes}""",
                
                "Resume Tailor": f"Using Australian standards (1-page max, no photo, no age), tailor this experience: {user_notes} to match this Job: {job_desc}.",
                
                "Cover Letter": f"Write a one-page Australian cover letter expressing passion for the company. Focus on how the student's visa (Working Rights) and skills benefit the employer. Job: {job_desc}, Notes: {user_notes}"
            }
            
            response = model.generate_content(prompts[tool])
            st.subheader(f"Your Generated {tool}")
            st.markdown(response.text)
            st.download_button("Download Text", response.text, file_name=f"{tool}.txt")
