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
        
        # Debug: Show raw data structure
        with st.expander("🔍 Debug: View Raw Data Structure"):
            st.json(data)
            st.write("Data type:", type(data).__name__)
            if isinstance(data, dict):
                st.write("Keys:", list(data.keys()))
        
        # Process data based on structure
        try:
            # Check if data has the new headers/rows format
            if isinstance(data, dict) and "headers" in data and "rows" in data:
                headers = data["headers"]
                rows = data["rows"]
                
                st.info(f"✅ Detected structured format with {len(headers)} columns and {len(rows)} rows")
                
                # Ensure headers is a list
                if isinstance(headers, list) and isinstance(rows, list):
                    df = pd.DataFrame(rows, columns=headers)
                else:
                    st.warning("⚠️ Headers/Rows not in expected list format. Falling back to key-value display.")
                    df = pd.DataFrame([{"Data": str(data)}])
                    
            elif isinstance(data, dict):
                # Old format: simple key-value pairs - flatten any nested values
                st.info("📋 Detected key-value pair format")
                df_data = []
                for k, v in data.items():
                    # Skip 'headers' and 'rows' if they're keys but don't match expected format
                    if k in ['headers', 'rows']:
                        continue
                    
                    # Convert nested objects to strings
                    if isinstance(v, (dict, list)):
                        v = str(v)
                    
                    df_data.append({"Field": k, "Value": str(v)})
                
                if df_data:
                    df = pd.DataFrame(df_data)
                else:
                    # If we filtered everything out, show raw
                    df = pd.DataFrame([{"Field": k, "Value": str(v)} for k, v in data.items()])
                
            elif isinstance(data, list):
                st.info("📊 Detected list format")
                # List of dictionaries - could be rows without explicit headers
                if len(data) > 0 and isinstance(data[0], dict):
                    df = pd.DataFrame(data)
                elif len(data) > 0 and isinstance(data[0], list):
                    # List of lists without headers
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame([{"Result": str(data)}])
            else:
                # Fallback for unexpected format
                st.warning("⚠️ Unexpected data format, showing as raw text")
                df_data = [{"Result": str(data)}]
                df = pd.DataFrame(df_data)
                
        except Exception as e:
            st.error(f"❌ Error processing data: {e}")
            df = pd.DataFrame([{"Raw Data": str(data)}])
            
        st.subheader("📊 Results Table")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Add download button for CSV export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"{st.session_state.doc_category}_data.csv",
            mime="text/csv",
        )
        
        if st.button("🔄 Start Over"):
            for key in ['step', 'uploaded_file_id', 'doc_category', 'extracted_data']:
                st.session_state.pop(key, None)
            st.rerun()
