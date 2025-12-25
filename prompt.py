'''
Prompt Testing
'''

def doc_extraction_prompt(doc_category):
    prompt = (
        f"Analyze the {doc_category} document data and extract all important fields.\n\n"
        f"IMPORTANT INSTRUCTIONS:\n"
        f"1. Return the data in a FLAT table structure suitable for display.\n"
        f"2. If the document contains a table, extract it with proper column headers.\n"
        f"3. For key-value pairs, create a two-column table with 'Field' and 'Value' headers.\n"
        f"4. Do NOT use nested JSON objects or arrays as values.\n"
        f"5. If there are multiple items (like line items in an invoice), return them as separate rows.\n"
        f"6. All values should be simple strings or numbers, not objects or arrays.\n\n"
        f"Return the result in the following JSON format:\n\n"
    )

    sample_output = {
        "headers": ["Field", "Value"],
        "rows": [
            ["Invoice Number", "INV-12345"],
            ["Date", "2025-12-25"],
            ["Total Amount", "$1,234.56"],
            ["Customer Name", "John Doe"]
        ]
    }

    prompt += str(sample_output)
    prompt += "\n\nOR for documents with line items:\n\n"
    
    sample_line_items = {
        "headers": ["Item", "Quantity", "Unit Price", "Amount"],
        "rows": [
            ["Product A", "2", "$10.00", "$20.00"],
            ["Product B", "1", "$15.00", "$15.00"]
        ]
    }
    
    prompt += str(sample_line_items)

    return prompt
def document_classify_prompt():
    prompt = (
        f"You are the expert on document categorization. Analyze the pdf and tell me the document class (Invoice/Medical/Education/Insurance). Return the result in below JSON Format."
        "JSON Format:\n"
    )

    sample_output = [{
        "category": "Invoice"
    }]

    prompt += str(sample_output)

    return prompt




