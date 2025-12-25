'''
Prompt Testing
'''

def doc_extraction_prompt(doc_category):
    prompt = (
        f"Analyze the {doc_category} document data."
        "Then Extract the importent field in JSON Format"
        "Identify these parameter names(Available in Price table) along with their possible options and return the result in the following JSON format:\n\n"
    )

    sample_output = {
        "Parameter_1": "Value_1",
        "Parameter_2": "Value_2"
    }

    prompt += str(sample_output)

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




