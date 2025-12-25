import streamlit as st
import os
import tempfile
import pandas as pd
from gemini import upload_pdf, get_gemini_response
from prompt import document_classify_prompt, doc_extraction_prompt

# Set page configuration
st.set_page_config(page_title="DocMind AI - PDF Extraction", layout="wide")

st.title("📄 DocMind AI: PDF Data Extractor")
st.markdown("---")

# Initialize session state for multi-step workflow
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'uploaded_file_id' not in st.session_state:
    st.session_state.uploaded_file_id = None
if 'doc_category' not in st.session_state:
    st.session_state.doc_category = None
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None

# Step 1: File Upload
if st.session_state.step == 1:
    st.header("Step 1: Upload your PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Uploading and analyzing document..."):
                # Save uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                try:
                    # Upload to Gemini File API
                    sample_file = upload_pdf(tmp_path)
                    st.session_state.uploaded_file_id = sample_file
                    
                    # Step 2: Classify Document
                    classify_query = document_classify_prompt()
                    classification_result = get_gemini_response(sample_file, classify_query)
                    
                    if isinstance(classification_result, list) and len(classification_result) > 0:
                        st.session_state.doc_category = classification_result[0].get("category", "Unknown")
                    elif isinstance(classification_result, dict):
                        st.session_state.doc_category = classification_result.get("category", "Unknown")
                    else:
                        st.session_state.doc_category = "Unknown"
                        
                    st.session_state.step = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

# Step 2 & 3: Display Category & Next Button
elif st.session_state.step == 2:
    st.header("Step 2 & 3: Document Classification")
    st.success(f"Document detected as: **{st.session_state.doc_category}**")
    
    if st.button("Next: Extract Data"):
        st.session_state.step = 3
        st.rerun()

# Step 4, 5 & 6: Data Extraction & Tabular Display
elif st.session_state.step == 3:
    st.header("Step 5 & 6: Extracted Data")
    
    if st.session_state.extracted_data is None:
        with st.spinner(f"Extracting details for {st.session_state.doc_category}..."):
            try:
                extraction_query = doc_extraction_prompt(st.session_state.doc_category)
                extraction_result = get_gemini_response(st.session_state.uploaded_file_id, extraction_query)
                st.session_state.extracted_data = extraction_result
            except Exception as e:
                st.error(f"Extraction failed: {e}")
                st.session_state.step = 1 # Allow restart
    
    if st.session_state.extracted_data:
        # Prepare data for tabular display
        data = st.session_state.extracted_data
        
        # If the response is a dict, convert to a list of dicts for the dataframe
        if isinstance(data, dict):
            df_data = [{"Field": k, "Value": v} for k, v in data.items()]
        elif isinstance(data, list):
            df_data = data
        else:
            df_data = [{"Result": str(data)}]
            
        df = pd.DataFrame(df_data)
        st.subheader("Results Table")
        st.dataframe(df, use_container_width=True)
        
        if st.button("Start Over"):
            for key in ['step', 'uploaded_file_id', 'doc_category', 'extracted_data']:
                st.session_state.pop(key, None)
            st.rerun()
