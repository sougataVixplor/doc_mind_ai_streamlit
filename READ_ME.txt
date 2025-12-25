DocMind AI - PDF Data Extractor
================================

QUICK START:
1. Install requirements: pip install -r requirements.txt
2. Set API key: $env:GEMINI_API_KEY="your-api-key-here"
3. Run app: streamlit run streamlit_app.py

FEATURES:
- Automatic PDF document classification
- Smart data extraction using Gemini AI
- Tabular data display
- CSV export functionality
- Multi-step workflow interface

USAGE WORKFLOW:
1. Upload PDF document
2. Click "Process Document"
3. View detected category
4. Click "Next: Extract Data"
5. Review extracted data in table
6. Download as CSV (optional)
7. Click "Start Over" for new document

FILES:
- streamlit_app.py: Main Streamlit application
- gemini.py: Gemini API integration (upload_pdf, get_gemini_response)
- prompt.py: AI prompt templates (classification & extraction)
- requirements.txt: Python dependencies

SUPPORTED DOCUMENT TYPES:
- Invoice
- Medical
- Education
- Insurance

ENVIRONMENT VARIABLES:
- GEMINI_API_KEY: Your Google Gemini API key (required)

TECHNICAL DETAILS:
- AI Model: Gemini 2.5 Flash
- Response Format: JSON
- Output: Pandas DataFrame -> CSV

CUSTOMIZATION:
- Edit prompt.py to modify classification categories
- Adjust extraction prompts for different data fields
- Modify output format in doc_extraction_prompt()

TROUBLESHOOTING:
- API key error: Check environment variable is set
- Upload fails: Verify PDF is valid and not corrupted
- Extraction issues: Review prompts in prompt.py

For detailed documentation, see README.md
