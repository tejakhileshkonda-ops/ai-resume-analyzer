import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import json
from google import genai
from google.genai import types  # Import types for structured configurations
from dotenv import load_dotenv

# Load secret API key safely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Google GenAI Client
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("⚠️ GEMINI_API_KEY not found! Verify that your .env file is configured properly.")

# Configure page width and layout to wide dashboard view
st.set_page_config(page_title="Enterprise AI Resume Scorer", layout="wide")

def convert_all_pdf_pages_to_images(uploaded_file):
    """Parses ALL PDF pages in memory and returns a list of PIL Images to handle multi-page resumes."""
    pdf_bytes = uploaded_file.read()
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    images = []
    # Loop through every page dynamically
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=150)    # Crisp resolution scaling
        img_data = pix.tobytes("png")
        images.append(Image.open(io.BytesIO(img_data)))
        
    return images

# --- UI FRONTEND DASHBOARD ---
st.title("🎯 Enterprise Multimodal AI Resume Analyzer")
st.markdown("🥇 **Advanced Candidate Assessment Platform & Job Matching Engine**")
st.markdown("---")

# Left Sidebar Control Panel Form
st.sidebar.header("👤 Candidate Profile Settings")
username = st.sidebar.text_input("Enter Candidate Name/Handle:", placeholder="e.g., Alex77")
target_role = st.sidebar.text_input("Target Job Role:", placeholder="e.g., Data Scientist")
experience_years = st.sidebar.number_input("Years of Professional Experience:", min_value=0, max_value=40, step=1, value=0)

st.sidebar.markdown("---")
st.sidebar.header("📋 Job Specification")
# Upgraded Feature: Interactive Job Description Matcher Input Frame
job_description = st.sidebar.text_area("Paste Targeted Job Description text (Optional):", placeholder="Paste raw job criteria from LinkedIn/Indeed here to calculate true semantic overlap...")

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF format supported)", type=["pdf"])

# Main Dashboard Container Execution Layer
if uploaded_file:
    st.subheader(f"📊 Live ATS Evaluation Workspace for: {username if username else 'Guest'}")
    col1, col2 = st.columns([1, 1.2]) # High-impact side-by-side split
    
    # Process all pages immediately to prevent pipeline blockages
    try:
        # Save a clean reset pointer reference point
        uploaded_file.seek(0)
        resume_images_list = convert_all_pdf_pages_to_images(uploaded_file)
    except Exception as e:
        st.error(f"Error reading PDF structure: {e}")
        resume_images_list = []
        
    with col1:
        st.markdown("### 📄 Document Visual Flow")
        if resume_images_list:
            # Display page 1 preview visually on the interactive column canvas
            st.image(resume_images_list[0], caption=f"Resume Preview (Page 1 of {len(resume_images_list)})", use_container_width=True)
            if len(resume_images_list) > 1:
                st.info(f"ℹ️ Core processing pipeline has securely batched all {len(resume_images_list)} pages into the multimodal attention vector layer.")
            
    with col2:
        st.markdown("### 🤖 Real-Time Evaluation Metrics")
        
        # Central Execution Button
        if st.sidebar.button("Execute AI Analysis", type="primary"):
            if not username or not target_role:
                st.sidebar.warning("⚠️ Please fill in the Candidate Name and Target Job Role in the sidebar panel.")
            else:
                with st.spinner("Gemini is parsing multi-page visual elements & scoring semantic parameters..."):
                    try:
                        # Construct a hyper-targeted analytical prompt layout
                        prompt = f"""
                        You are an elite corporate technical recruiter and automated ATS evaluation engine.
                        Examine the attached resume images critically. The candidate's reference handle is '{username}'.
                        They are targeting the role of '{target_role}' with '{experience_years}' years of industry experience.
                        """
                        
                        # Dynamically inject the complex JD parameters if provided by the user
                        if job_description:
                            prompt += f"\nCRITICAL INSTRUCTION: Evaluate the resume strictly against this custom target job description:\n'''{job_description}'''"
                        
                        prompt += """
                        Return a valid JSON object matching this exact key structure:
                        {
                            "final_score": integer_value_between_0_and_100,
                            "match_status": "Excellent" or "Good" or "Needs Improvement",
                            "role_alignment": "Your short text feedback here",
                            "experience_verification": "Your short text feedback here",
                            "visual_layout": "Your short text feedback here",
                            "missing_keywords": ["keyword1", "keyword2", "keyword3"]
                        }
                        """
                        
                        # Pack all generated images alongside the core textual prompt array block
                        contents_payload = [prompt] + resume_images_list
                        
                        # Execute structured deep multimodal evaluation
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=contents_payload,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json"
                            )
                        )
                        
                        # Parse out data dictionary metrics safely
                        result_data = json.loads(response.text)
                        
                        # Commit data structures to local application cache storage
                        st.session_state['result_data'] = result_data
                        st.session_state['processed_user'] = username
                        
                    except Exception as ai_error:
                        st.error(f"Failed to communicate with AI Engine. Details: {ai_error}")

        # --- DYNAMIC DASHBOARD VISUALIZATION CARDS (UPGRADED UI) ---
        if 'result_data' in st.session_state and st.session_state.get('processed_user') == username:
            data = st.session_state['result_data']
            
            score = data['final_score']
            status = data['match_status']
            
            # Draw premium top-level scoreboard metrics
            st.metric(label="Overall Suitability Index Score", value=f"{score} / 100", delta=status)
            st.progress(score / 100) 
            
            st.markdown("---")
            
            # Premium Enterprise Card Containers
            with st.container(border=True):
                st.markdown("#### 📋 Core Analytic Breakdown")
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    with st.container(border=True):
                        st.markdown("💼 **Role Alignment Vector**")
                        st.write(data['role_alignment'])
                        
                    with st.container(border=True):
                        st.markdown("🎨 **Visual Formatting & Typography Criticism**")
                        st.write(data['visual_layout'])
                        
                with metric_col2:
                    with st.container(border=True):
                        st.markdown("⏳ **Domain Experience Tracking Check**")
                        st.write(data['experience_verification'])
                        
                    with st.container(border=True):
                        st.markdown("🔍 **Strategic Keyword Recommendations**")
                        keywords = data.get('missing_keywords', [])
                        if keywords:
                            st.write(" ".join([f"`{kw}`" for kw in keywords]))
                        else:
                            st.write("Perfect alignment! No critical vacancies found.")
            
            # Generate the text summary compilation matrix layout report
            text_report = f"""==================================================
AI RESUME ANALYZER EXPORT REPORT: {username}
Target Profile Intent: {target_role}
Experience Level Checked: {experience_years} Years
==================================================
OVERALL SUITABILITY VALUE: {score}/100 ({status})

- Role Alignment Analysis: {data['role_alignment']}
- Professional Background Match: {data['experience_verification']}
- Layout and Appearance Review: {data['visual_layout']}
- Identified Missing Keyword Elements: {', '.join(keywords) if keywords else 'None'}
==================================================™"""
            
            st.markdown("---")
            st.download_button(
                label="📥 Export Report Data Summary",
                data=text_report,
                file_name=f"{username}_comprehensive_score_report.txt",
                mime="text/plain",
                use_container_width=True
            )
else:
    st.info("Complete the parameter fields on the left sidebar profile template and drop a resume PDF file to populate the interactive metrics dashboard.")