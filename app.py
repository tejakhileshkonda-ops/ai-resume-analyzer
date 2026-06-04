import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import json
from google import genai
from google.genai import types  # Import types for structured configurations
from dotenv import load_dotenv

# 1. Load secret API key safely from the hidden file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Google GenAI Client
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("⚠️ GEMINI_API_KEY not found! Verify that your .env file is configured properly.")

# Configure page width and layout
st.set_page_config(page_title="AI Resume Scorer", layout="wide")

def convert_pdf_to_image(uploaded_file):
    """Parses PDF binary data directly in memory and renders Page 1 to an image."""
    pdf_bytes = uploaded_file.read()
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    page = pdf_document.load_page(0)  # Extract page 1
    pix = page.get_pixmap(dpi=150)    # Convert text layout to visual pixel map
    img_data = pix.tobytes("png")
    
    return Image.open(io.BytesIO(img_data))

# --- UI FRONTEND ---
st.title("🎯 Personalized AI Resume Scorer")
st.markdown("---")

# Left Sidebar Control Form
st.sidebar.header("👤 User Profile Settings")
username = st.sidebar.text_input("Enter your Username:", placeholder="e.g., Alex77")
target_role = st.sidebar.text_input("Target Job Role:", placeholder="e.g., Data Scientist")
experience_years = st.sidebar.number_input("Years of Experience:", min_value=0, max_value=40, step=1, value=0)

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload your Resume (PDF format)", type=["pdf"])

# Main Dashboard Frame
if uploaded_file:
    st.subheader(f"📊 Live Analysis Dashboard for: {username if username else 'Guest'}")
    col1, col2 = st.columns([1, 1.2]) # Side-by-side display split
    
    with col1:
        st.markdown("### 📄 Converted Resume Image")
        try:
            resume_image = convert_pdf_to_image(uploaded_file)
            st.image(resume_image, caption="Visual Layout View", use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering PDF layout: {e}")
            
    with col2:
        st.markdown("### 🤖 Live AI Evaluation Metrics")
        
        # Core trigger button
        if st.sidebar.button("Generate Score", type="primary"):
            if not username or not target_role:
                st.sidebar.warning("⚠️ Please provide both a Username and a Target Role.")
            else:
                with st.spinner("Gemini is analyzing structure and scoring match criteria..."):
                    try:
                        # Enforce a strict JSON schema blueprint format
                        prompt = f"""
                        You are an elite corporate technical recruiter and automated ATS evaluation engine.
                        Examine the attached resume image critically. The candidate's reference handle is '{username}'.
                        They are targeting the role of '{target_role}' with '{experience_years}' years of industry experience.
                        
                        Return a valid JSON object matching this exact key structure:
                        {{
                            "final_score": integer_value_between_0_and_100,
                            "match_status": "Excellent" or "Good" or "Needs Improvement",
                            "role_alignment": "Your short text feedback here",
                            "experience_verification": "Your short text feedback here",
                            "visual_layout": "Your short text feedback here",
                            "missing_keywords": ["keyword1", "keyword2", "keyword3"]
                        }}
                        """
                        
                        # Call model using JSON configuration schema constraints
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[prompt, resume_image],
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json"
                            )
                        )
                        
                        # Parse JSON text string into a native Python dictionary
                        result_data = json.loads(response.text)
                        
                        # Save inside session state tracking dictionary memory
                        st.session_state['result_data'] = result_data
                        st.session_state['processed_user'] = username
                        
                    except Exception as ai_error:
                        st.error(f"Failed to communicate with AI Engine. Details: {ai_error}")

        # --- DASHBOARD VISUALIZATION RENDERING LAYER ---
        if 'result_data' in st.session_state and st.session_state.get('processed_user') == username:
            data = st.session_state['result_data']
            
            # Extract key layout values
            score = data['final_score']
            status = data['match_status']
            
            # Graphical score meters
            st.metric(label="Overall Suitability Rating", value=f"{score} / 100", delta=status)
            st.progress(score / 100) 
            
            st.markdown("---")
            
            # Dynamic Column Breakdowns
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.info(f"**💼 Role Alignment**\n\n{data['role_alignment']}")
                st.success(f"**🎨 Design & Formatting**\n\n{data['visual_layout']}")
            with metric_col2:
                st.warning(f"**⏳ Experience Check**\n\n{data['experience_verification']}")
                
                # Dynamic pill keywords mapping loop
                st.markdown("**🔍 Recommended Missing Keywords:**")
                keywords = data.get('missing_keywords', [])
                if keywords:
                    st.write(" ".join([f"`{kw}`" for kw in keywords]))
                else:
                    st.write("None! Perfect alignment.")
            
            # ==========================================
            # 🛠️ DAY 7 ADDITION: REPORT EXPORT BUTTON
            # ==========================================
            
            # Formulate the downloadable text layout template
            text_report = f"""==================================================
AI RESUME SCORE REPORT FOR: {username}
Target Job Role: {target_role}
Declared Experience Threshold: {experience_years} Years
==================================================
FINAL MATCH SUITABILITY: {score}/100 ({status})

[🔍 DETAILED EVALUATION CRITIQUE]

* Role Alignment Status:
  {data['role_alignment']}

* Professional Experience Check:
  {data['experience_verification']}

* Visual Layout & Typography Review:
  {data['visual_layout']}

* Missing Keywords Identified:
  {", ".join(keywords) if keywords else "None"}

Generated automatically via the AI Resume Analyzer & Scorer Pipeline.
=================================================="""

            st.markdown("---")
            # Create the data stream download button
            st.download_button(
                label="📥 Download Score Report",
                data=text_report,
                file_name=f"{username}_resume_score_report.txt",
                mime="text/plain",
                use_container_width=True
            )
else:
    st.info("Fill out your target profile info and upload a resume PDF to run the analyzer.")