"""Resume parsing utilities using OpenAI"""
import openai
import os
import base64
import json

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY") or None)

def parse_resume_text(resume_text: str) -> dict:
    """
    Parse resume text to extract profile information using OpenAI
    
    Args:
        resume_text: The text content of the resume
    
    Returns:
        Dictionary with extracted information:
        - bio: Professional summary/bio
        - company: Current company
        - role: Current role/title
        - linkedin_profile: LinkedIn URL if found
        - talking_points: List of key achievements/points
    """
    system_prompt = """
    You are a resume parser. Extract the following information from the resume:
    
    1. bio: A professional summary or bio (2-3 sentences summarizing the person's background and expertise)
    2. company: Current company name (if available)
    3. role: Current job title/role (if available)
    4. linkedin_profile: LinkedIn profile URL if mentioned
    5. talking_points: List of 5-8 key achievements, experiences, or talking points (as an array of strings)
    
    Return ONLY a JSON object with these exact fields. If a field cannot be determined, use null.
    
    Example output:
    {
        "bio": "Software engineer with 5 years of experience building scalable web applications using React and Node.js. Passionate about user experience and data-driven product development.",
        "company": "Google",
        "role": "Senior Software Engineer",
        "linkedin_profile": "https://linkedin.com/in/johndoe",
        "talking_points": [
            "Led development of a microservices architecture serving 1M+ users",
            "Reduced page load time by 40% through performance optimization",
            "Mentored 3 junior developers and established code review practices"
        ]
    }
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini for cost efficiency
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Parse this resume:\n\n{resume_text}"}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        parsed_data = json.loads(content)
        
        # Ensure all fields are present
        result = {
            "bio": parsed_data.get("bio"),
            "company": parsed_data.get("company"),
            "role": parsed_data.get("role"),
            "linkedin_profile": parsed_data.get("linkedin_profile"),
            "talking_points": parsed_data.get("talking_points", [])
        }
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {
            "bio": None,
            "company": None,
            "role": None,
            "linkedin_profile": None,
            "talking_points": []
        }
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return {
            "bio": None,
            "company": None,
            "role": None,
            "linkedin_profile": None,
            "talking_points": []
        }

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file
    
    Args:
        file_content: PDF file bytes
    
    Returns:
        Extracted text string
    """
    try:
        import PyPDF2
        import io
        
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from DOCX file
    
    Args:
        file_content: DOCX file bytes
    
    Returns:
        Extracted text string
    """
    try:
        from docx import Document
        import io
        
        doc_file = io.BytesIO(file_content)
        doc = Document(doc_file)
        
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
        return ""

def parse_resume_file(file_content: bytes, filename: str) -> dict:
    """
    Parse resume file and extract profile information
    
    Args:
        file_content: File bytes
        filename: Original filename
    
    Returns:
        Dictionary with extracted information
    """
    # Extract text based on file type
    if filename.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(file_content)
    elif filename.lower().endswith(('.doc', '.docx')):
        resume_text = extract_text_from_docx(file_content)
    else:
        # Try to decode as plain text
        try:
            resume_text = file_content.decode('utf-8')
        except:
            resume_text = ""
    
    if not resume_text.strip():
        return {
            "bio": None,
            "company": None,
            "role": None,
            "linkedin_profile": None,
            "talking_points": [],
            "error": "Could not extract text from resume file"
        }
    
    # Parse the extracted text
    return parse_resume_text(resume_text)

