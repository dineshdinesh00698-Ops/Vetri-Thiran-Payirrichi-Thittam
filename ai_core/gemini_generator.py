import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

        if genai and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    def build_prompt(self, document_type, parties, terms, dates):
        return f"""
You are a legal-document drafting assistant.

Create a professional, clearly structured draft for the following document.

Document type: {document_type}
Parties: {parties}
Terms and conditions: {terms}
Effective date: {dates}

Requirements:
- Use clear headings and numbered sections.
- Include the supplied parties, date, and terms.
- Do not invent personal facts that were not supplied.
- Use neutral professional language.
- Add a short notice at the end saying the document should be reviewed by a qualified legal professional before use.
- Return only the document text.
"""

    def generate_document(self, document_type, parties, terms, dates):
        prompt = self.build_prompt(document_type, parties, terms, dates)

        if not self.model:
            # Useful for testing the UI without an API key.
            return (
                f"{document_type.upper()}\n\n"
                f"Effective Date: {dates}\n\n"
                f"PARTIES\n{parties}\n\n"
                f"TERMS AND CONDITIONS\n{terms}\n\n"
                "LEGAL REVIEW NOTICE\n"
                "This is an AI-generated draft and should be reviewed by a qualified "
                "legal professional before use."
            )

        response = self.model.generate_content(prompt)
        return response.text
