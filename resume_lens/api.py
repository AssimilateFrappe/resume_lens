import os
import re
import secrets
import spacy
import docx2txt
import pypdf
import frappe
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

SITE_URL = frappe.utils.get_url()
        
# Define paths
BASE_DIR = frappe.get_app_path("resume_lens")
PRIVATE_DIR = frappe.get_site_path("private", "files")
PUBLIC_DIR = frappe.get_site_path("public", "files")
WHITELISTED_DOWNLOAD_PATHS = [PRIVATE_DIR, PUBLIC_DIR]
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

# Store tokens mapped to filepaths for secure downloads and views
TOKEN_MAP = {}

#generate token for download file 
def generate_download_token(filepath):
    """Generate a secure token for a given filepath"""
    token = secrets.token_urlsafe(16)
    TOKEN_MAP[token] = filepath
    return token

#Determine the file type and absolute path based on the resume URL.
def resolve_file_path(resume_url):
    filename = os.path.basename(resume_url)

    if resume_url.startswith("/private/files/"):
        file_type = "private"
        file_path = os.path.join(PRIVATE_DIR, filename)
    else:
        file_type = "public"
        file_path = os.path.join(PUBLIC_DIR, filename)

    return file_type, file_path, filename

#Check if the resolved path is within allowed directories
def is_path_allowed(filepath):
    abs_path = os.path.abspath(filepath)
    return any(abs_path.startswith(os.path.abspath(allowed)) for allowed in WHITELISTED_DOWNLOAD_PATHS)

#Generate a secure download URL
def get_secure_download_url(resume_url):
    file_type, file_path, filename = resolve_file_path(resume_url)
    token = generate_download_token(file_path)
          
    return f"/api/method/resume_lens.api.download_matched_resume?token={token}"

#Generates a secure view URL for a given resume URL.
def get_secure_view_url(resume_url):
    file_type, file_path, filename = resolve_file_path(resume_url)
    token = generate_download_token(file_path)
    
    return f"/api/method/resume_lens.api.view_matched_resume?token={token}"

#Download a matched resume based on a provided token.
@frappe.whitelist(allow_guest=True)
def download_matched_resume(token):
    filepath = TOKEN_MAP.get(token)
    if not filepath or not os.path.exists(filepath):
        frappe.throw("Invalid or expired link", frappe.PermissionError)

    if not is_path_allowed(filepath):
        frappe.throw("Unauthorized folder access", frappe.PermissionError)

    with open(filepath, "rb") as f:
        filecontent = f.read()

    filename = os.path.basename(filepath)
    frappe.local.response.filename = filename
    frappe.local.response.filecontent = filecontent
    frappe.local.response.type = "download"
    return

#Securely serve a resume file for viewing if the token is valid
@frappe.whitelist(allow_guest=True)
def view_matched_resume(token):
    filepath = TOKEN_MAP.get(token)
    if not filepath or not os.path.exists(filepath):
        frappe.throw("Invalid or expired link for viewing", frappe.PermissionError)

    if not is_path_allowed(filepath):
        frappe.throw("Unauthorized folder access for viewing", frappe.PermissionError)

    content_type_map = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/msword"
    }
    ext = os.path.splitext(filepath)[1].lower()
    content_type = content_type_map.get(ext, "text/plain")

    with open(filepath, "rb") as f:
        filecontent = f.read()

    return {
        "file_name": os.path.basename(filepath),
        "file_content": frappe.utils.encode(filecontent),
        "content_type": content_type,
    }

#Extract text form html content
def strip_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    
    for tag in soup.find_all(['p', 'br', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        tag.insert_before('\n')

    return ' '.join(soup.get_text().split())

#Get All Job Opening From Frappe
@frappe.whitelist(allow_guest=True)
def get_all_records():
    try: 
        data = frappe.get_all("Job Opening", filters={"status": "Open"}, fields=["job_title", "description"])
        cleaned_data = [{"job_title": item["job_title"], "description": strip_html(item["description"])} for item in data]
        return cleaned_data
    except Exception as e:
        frappe.throw(f"Error fetching job openings: {str(e)}")

#This function fetches job applicants, processes their resume URLs, and constructs a list of file data objects.
def get_applicant_files(): 
    applicants = get_job_applicants() 
    if isinstance(applicants, str):
        return applicants 
    files_data = []
    for applicant in applicants:
        resume_url = applicant.get("resume_attachment")
        if not resume_url:
            continue  

        filename = os.path.basename(resume_url)
        
        if resume_url.startswith("/private/files/"):
            file_type = "private"
            file_path = frappe.get_site_path("private", "files", filename)
        else:
            file_type = "public"
            file_path = frappe.get_site_path("public", "files", filename)

        file_object = {
            "applicant_name": applicant.get("applicant_name"),
            "email": applicant.get("email_id"),
            "file_type": file_type,
            "file_url": resume_url,  
            "file_path": file_path,  
            "filename": filename 
        }

        files_data.append(file_object)

    return files_data

#Get Job Applicant whose status is open from frappe
@frappe.whitelist(allow_guest=True)
def get_job_applicants():
    applicants = frappe.get_all(
        "Job Applicant", 
        filters={"status": "Open"},
        fields=["applicant_name", "email_id", "resume_attachment","resume_link"]
    )

    if not applicants:
        return "No Job Applicants Found"

    return applicants 

#Process resumes by parsing job descriptions and resumes, scoring them, and categorizing them based on match percentage.
@frappe.whitelist(allow_guest=True)
def process_resumes():   
    jd_job_title = frappe.local.form_dict.get('job_title_select') 
    jd_text = frappe.local.form_dict.get('jd_text')
    resumes_files = get_applicant_files()
  
    if frappe.request.method == "OPTIONS":
        frappe.local.response.headers['Access-Control-Allow-Origin'] = '*'
        frappe.local.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        frappe.local.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Frappe-CSRF-Token'
        return {}

    try:
        if jd_text:
            jd_parsed = parse_jd(jd_text=jd_text)
    except Exception as e:
        return {'Error': f"Failed to parse job description: {str(e)}"}

    resume_scores = []
    
    for resume_file in resumes_files:
        if not allowed_file(resume_file['filename']):
            continue

        resume_path = resume_file['file_path']
        try:
            resume_parsed = parse_resume(resume_path)
            score = score_resume(jd_parsed, resume_parsed)
            percentage_score = score * 100
         
            experience_years = resume_parsed.get('total_experience', 0)
            resume_scores.append({
                'applicant_name': resume_file['applicant_name'],
                'resume_name': resume_file['filename'],
                'score': f"{percentage_score:.2f}%",
                'experience_years': experience_years,
                'resume_skills': resume_parsed.get('resume_skills', []),
                'file_url': resume_file['file_url'],
                'file_path': resume_path

            })
            
        except Exception as e:
            print(f"Error processing resume {resume_file['filename']}: {e}")
            continue

    experience_range = jd_parsed.get('experience', [])
    if experience_range:
        min_experience = min(exp[0] for exp in experience_range)
        max_experience = max(exp[1] for exp in experience_range)
    else:
        return {'Error': 'Experience range not found in job description'}

    filtered_resumes = filter_resumes_by_experience(resume_scores, min_experience, max_experience,
                                                    jd_parsed['jd_required_skills'])

    matched_resumes = {
        "PerfectMatched": [],
        "TopMatched": [],
        "GoodMatched": [],
        "PoorMatched": [],
        "NotGood": []
    }

    for resume in filtered_resumes:
        score = float(resume['score'].strip('%'))
        if score >= 80:
            matched_resumes["PerfectMatched"].append(resume)
        elif 70 <= score < 80:
            matched_resumes["TopMatched"].append(resume)
        elif 60 <= score < 70:
            matched_resumes["GoodMatched"].append(resume)
        elif 50 <= score < 60:
            matched_resumes["PoorMatched"].append(resume)
        elif score < 50:
            matched_resumes["NotGood"].append(resume)

    jd_required_skills = jd_parsed['jd_required_skills']
    save_shortlisted_candidates(matched_resumes, jd_job_title, jd_required_skills)
    
    return {
        'Matched_Resumes': matched_resumes,
        'jd_required_skills': jd_required_skills
    }

# check file extention with ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to save shortlisted candidates for a job opening
@frappe.whitelist()
def save_shortlisted_candidates(candidate_score_list, job_opening, jd_required_skills):
    if not job_opening or not candidate_score_list:
        return {"status": "error", "message": "Job Opening and Candidate Score List are required."}

    job_opening_id = frappe.db.get_value("Job Opening", {"job_title": job_opening, "status": "Open"}, "name")
    
    if not job_opening_id:
        return {"status": "error", "message": f"Job Opening '{job_opening}' not found or not open."}

    shortlisted_candidates = []

    allowed_categories = ["PerfectMatched", "TopMatched", "GoodMatched"]
    for category in allowed_categories:
        if category in candidate_score_list:
            for candidate in candidate_score_list[category]:
                job_applicant = frappe.db.get_value("Job Applicant", {"applicant_name": candidate["applicant_name"]}, "name")

                if job_applicant:
                    shortlisted_candidates.append({
                        "job_applicant": job_applicant,
                        "resume_name": candidate["resume_name"],
                        "experience_year": candidate["experience_years"],
                        "skills_count": candidate["matched_count"],
                        "matched_skills": ", ".join(candidate["matched_skills"]),
                        "score": candidate["score"]
                    })

    if not shortlisted_candidates:
        return {"status": "error", "message": "No valid candidates found for shortlisting."}

    shortlisted_doc = frappe.get_doc({
        "doctype": "Shortlisted Candidates",
        "job_opening": job_opening_id,
        "candidate_score_list": shortlisted_candidates,
        "jd_required_skills": ", ".join(jd_required_skills)
    })

    shortlisted_doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {"status": "success", "message": "Shortlisted candidates saved successfully."}

# Extract experience ranges from text using regex patterns
def extract_experience(text):
    experience_patterns = [
        r'(?i)(?:Work Experience|Professional Experience|Experience|Experience range|Min Experience|Max Experience|Exp|Min Exp|Max Exp|Experience:|Experience :)\s*[:\-]?\s*(\d+(\.\d+)?)\s*(?:to|-|–)\s*(\d+(\.\d+)?)\s*(?:years|Years)|\b(\d+(\.\d+)?)\+\s*(?:years|Years)|\b(\d+(\.\d+)?)\s*(?:\+)?\s*(?:years|Years)|\b(\d+(\.\d+)?)\s*-\s*(\d+(\.\d+)?)\s*(?:yrs|Years)'
    ]
    
    extracted_experience = []
    for pattern in experience_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if match[0] and match[2]:
                start = float(match[0])
                end = float(match[2])
                extracted_experience.append((start, end))
            elif match[4]:
                extracted_experience.append((float(match[4]), float(match[4]) + 5))
            elif match[6]:
                extracted_experience.append((float(match[6]), float(match[6]) + 5))
            elif match[8] and match[10]:
                start = float(match[8])
                end = float(match[10])
                extracted_experience.append((start, end))

    return extracted_experience

#Extract Text From PDF File
def extract_text_from_pdf(file_path):
    text = ""
    
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    try:
        with open(file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

    return text

#Extract Text from doc, docx files
def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

#Extract Skills From text 
def extract_skills(skills_text):
    skills_text = re.sub(r'[•\-–]', '', skills_text)
    skills_text = re.sub(r'\s+', ' ', skills_text)
    doc = nlp(skills_text)
    excluded_tokens = ['NOUN', 'ADJ', 'PRON', 'CONJ', 'SCONJ', 'ADP', 'AUX', 'VERB', 'DET', 'CCONJ']
    excluded_symbols = ['etc','to','to', '(', ')', '-', '_', '.', '/', ',', 'e.g.', '\n', ':', '’s',
                        'to', 'hands','indepth','+', '2', 'complete','master', 'bachelor’s/', 'bachelor',
                        'engineering/',' ','3','', 'independently', 'ip', 'identity', 'closely', 'http',
                        'framework', 'one', 'highly', 'pipeline', 'serverless', 'strong', 'compute', 'code',
                        'experience', 'web', 'storage', 'also', 'lambda', 'access', 'simple',
                        'quickly', 'especially', 'certification', 'elastic', 'developer', 'information',
                        'infrastructure', 'iam', 'service', 'effectively','management', 'dependency', 'entity',
                        '10', 'core', 'parallel', 'async', 'basics', 'security', 'patterns', 'json','good',
                        '!','~','`','@','$','%','^','*',]

    excluded_symbols.extend(str(num) for num in range(1, 100001))
    skills = [token.text.lower() for token in doc if token.pos_ not in excluded_tokens and token.text.lower() not in excluded_symbols]
    return list(set(skills))

#Parse Job Description file like [pdf,doc,docx] and return text
def parse_jd(jd_file=None, jd_text=None):
    if jd_text:
        text = jd_text
    elif jd_file:
        if jd_file.endswith('.pdf'):
            text = extract_text_from_pdf(jd_file)
        elif jd_file.endswith('.doc'):
            text = extract_text_from_docx(jd_file)
        elif jd_file.endswith('.docx'):
            text = extract_text_from_docx(jd_file)
        else:
            with open(jd_file, 'r') as f:
                text = f.read()
    else:
        return {'error': 'No input provided'}

    doc = nlp(text)
    experience = extract_experience(text)
    
    required_skills = re.search(r"(Skills :|Skills:|Requisite Skills:|Required Skills:|Must Have:)([\s\S]*?)(?=Preferred Skills|Education|Soft Skills|Roles and Responsibilities|$)", text, re.IGNORECASE)
    required_skills_text = required_skills.group(2).strip() if required_skills else ''

    jd_required_skills = extract_skills(required_skills_text)

    return {
        'raw_text': text,
        'experience': experience if experience else [(0, 0)],
        "jd_required_skills": jd_required_skills
    }

# This Function Extracts Text From Resume
def extract_experience_from_resume(text):
    experience_years = []

    experience_patterns = [
        r'(\d+(?:\.\d+)?\+?)\s*(?:years?|yr|yrs|years of experience|years\' experience)',
    ]

    for pattern in experience_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            years = match.strip('+')
            if years.isdigit() or years.replace('.', '', 1).isdigit():
                experience_years.append(float(years))

    return max(experience_years) if experience_years else 0

#This method pars resume file [pdf,doc, docx] and return extracted details in [raw_text,total_experience,resume_skills]
def parse_resume(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.doc') or file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        with open(file_path, 'r') as f:
            text = f.read()

    total_experience = extract_experience_from_resume(text)
    resume_skills = extract_skills(text)
    
    return {
        'raw_text': text,
        'total_experience': total_experience,
        'resume_skills': resume_skills
    }

#Extract Resume Score from Resume Text match with jd & resume text using sklearn.metrics.pairwise
def score_resume(jd_parsed, resume_parsed):
    jd_embedding = model.encode(jd_parsed['raw_text'])
    resume_embedding = model.encode(resume_parsed['raw_text'])
    similarity_score = cosine_similarity([jd_embedding], [resume_embedding])[0][0]
    return similarity_score

#This Method is Filter Resumes by Experience
def filter_resumes_by_experience(resume_scores, min_exp, max_exp, jd_required_skills):
    filtered_resumes = []
    for resume in resume_scores:
        exp_years = resume['experience_years']
        if min_exp <= exp_years <= max_exp:
            matched_skills = set(jd_required_skills).intersection(set(map(str.lower, resume['resume_skills'])))
            matched_count = len(matched_skills)
            total_jd_skills = len(jd_required_skills)
            list_matched_skills = list(matched_skills)

            filtered_resumes.append({
                'applicant_name': resume['applicant_name'],
                'resume_name': resume['resume_name'],
                'score': resume['score'],
                'experience_years': resume['experience_years'],
                'matched_skills': list_matched_skills,
                'matched_count': f'{matched_count} out of {total_jd_skills}',
                'view_url': get_secure_view_url(resume['file_url']),
            })
    return filtered_resumes
