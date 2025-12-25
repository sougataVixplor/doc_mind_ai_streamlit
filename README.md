# 📄 DocMind AI - PDF Data Extractor

A powerful Streamlit application that uses Google's Gemini AI to automatically classify PDF documents and extract structured data from them.

## 🌟 Features

- **Automatic Document Classification**: Intelligently categorizes PDFs into types (Invoice, Medical, Education, Insurance, etc.)
- **Smart Data Extraction**: Extracts relevant fields and data based on document type
- **Structured Output**: Presents extracted data in clean, tabular format
- **CSV Export**: Download extracted data as CSV files
- **Multi-step Workflow**: Intuitive step-by-step process for document processing
- **Gemini 2.5 Flash Integration**: Leverages Google's latest AI model for accurate extraction

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/doc_mind_ai_streamlit.git
   cd doc_mind_ai_streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variable**
   
   Set your Gemini API key as an environment variable:
   
   **Windows (PowerShell):**
   ```powershell
   $env:GEMINI_API_KEY="your-api-key-here"
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   set GEMINI_API_KEY=your-api-key-here
   ```
   
   **Linux/Mac:**
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📖 Usage

1. **Upload PDF**: Click "Choose a PDF file" and select your document
2. **Process Document**: Click "Process Document" to upload and classify
3. **View Classification**: See the detected document category
4. **Extract Data**: Click "Next: Extract Data" to extract structured information
5. **View Results**: Browse the extracted data in table format
6. **Download**: Export results as CSV using the download button
7. **Start Over**: Process another document with the "Start Over" button

## 🏗️ Project Structure

```
doc_mind_ai_streamlit/
├── streamlit_app.py    # Main Streamlit application
├── gemini.py           # Gemini API integration
├── prompt.py           # AI prompt templates
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── READ_ME.txt        # Quick reference guide
```

## 📋 File Descriptions

- **`streamlit_app.py`**: Main application with UI and workflow logic
- **`gemini.py`**: Functions for PDF upload and Gemini API interaction
- **`prompt.py`**: Prompt engineering templates for classification and extraction
- **`requirements.txt`**: All required Python packages

## 🔧 Configuration

### Supported Document Types

Currently supports automatic classification for:
- Invoices
- Medical documents
- Educational documents
- Insurance documents

### Customizing Prompts

Edit `prompt.py` to customize:
- Document classification categories
- Extraction field mappings
- Output format structures

## 🛠️ Technical Details

### Dependencies

Key packages used:
- `streamlit` - Web application framework
- `google-genai` - Google Gemini API client
- `pandas` - Data manipulation and CSV export
- `httpx` - HTTP client for API requests

### AI Model

- **Model**: Gemini 2.5 Flash
- **Response Format**: JSON
- **File API**: Uses Google's File API for PDF upload

## 📊 Data Output Formats

The application supports two output formats:

1. **Key-Value Pairs**: For simple documents
   ```json
   {
     "headers": ["Field", "Value"],
     "rows": [
       ["Invoice Number", "INV-12345"],
       ["Date", "2025-12-25"]
     ]
   }
   ```

2. **Tabular Data**: For documents with line items
   ```json
   {
     "headers": ["Item", "Quantity", "Price"],
     "rows": [
       ["Product A", "2", "$10.00"],
       ["Product B", "1", "$15.00"]
     ]
   }
   ```

## 🔒 Security Notes

- API keys should never be committed to version control
- Use environment variables for sensitive credentials
- Uploaded PDFs are temporarily stored and deleted after processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Common Issues

**Issue**: "GEMINI_API_KEY not found"
- **Solution**: Ensure you've set the environment variable correctly

**Issue**: PDF upload fails
- **Solution**: Check file size and format (must be valid PDF)

**Issue**: Extraction returns unexpected format
- **Solution**: Review and adjust prompts in `prompt.py`

## 📧 Support

For issues and questions, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)