# ResumeLens - AI-Powered Resume Screening & Job Matching "Shortlist candidates"

### 📌 Repository: [GitHub - ResumeLens](https://github.com/AssimilateFrappe/resume_lens)
### 📌 Technologies: Python (Frappe), React (Frontend)
### 📌 License: MIT

---

## 📖 Index
1. Introduction
2. System Requirements
3. Installation & Setup
4. Features Overview
5. API Documentation
6. Backend (Frappe) API Implementation
7. Frontend (React) Implementation
8. Security & Permissions
9. Performance Optimization
10. Error Handling & Debugging
11. Contributing
12. License

---

## 1. Introduction

ResumeLens is an AI-powered resume screening and job matching tool designed to automate and enhance the hiring process. It extracts and analyzes resumes and job descriptions (JDs), ranks candidates based on skills and experience, and integrates seamlessly with the Frappe framework for job applicant tracking.

### Key Features:
- ✅ AI-driven resume screening based on job descriptions.
- ✅ Secure document handling (resume upload, view & download).
- ✅ Automated candidate ranking using AI algorithms.
- ✅ Frappe integration for job & applicant management.
- ✅ React-based frontend for an intuitive user experience.
- ✅ Token-based authentication for secure resume access.
- ✅ User-friendly dashboard with resume analytics.
- ✅ Multi-language support for international recruitment.
- ✅ Customizable scoring algorithms to fit diverse hiring needs.

---

## 2. System Requirements

### Backend (Frappe Framework)
- Python 3.10+
- Frappe Framework 14+
- MariaDB 10.3+
- Redis (for caching and queue processing)
- Node.js 16+ (for Frappe assets)
- npm 7+

### Frontend (React)
- React 18+
- TypeScript (recommended)
- Node.js & npm

---
<img width="680" alt="img1" src="https://github.com/user-attachments/assets/0b6b5f0f-0f18-450e-92fb-317925827139" />
<img width="679" alt="img2" src="https://github.com/user-attachments/assets/5822d5ee-1729-4830-9ac1-79c30b4f5603" />


## 3. Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AssimilateFrappe/resume_lens.git
cd resume_lens
```

### 2️⃣ Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup & Install Frappe App
```bash
bench get-app resume_lens
bench install-app resume_lens
bench start
```

### 4️⃣ Frontend Setup (React)
Navigate to the frontend directory:
```bash
cd frontend
npm install
npm start
```

---
<img width="585" alt="img3" src="https://github.com/user-attachments/assets/85ac329d-1185-4f74-b7cd-e02f2e2d3058" />
<img width="453" alt="img4" src="https://github.com/user-attachments/assets/0d51c832-9317-4f17-98ce-b3f44959aae4" />
<img width="882" alt="img5" src="https://github.com/user-attachments/assets/1020cd63-f98b-4f48-817e-2c1b11b0ba47" />
<img width="568" alt="img6" src="https://github.com/user-attachments/assets/53d66eea-81ac-499f-8e42-e77ac338ed6d" />
<img width="591" alt="img7" src="https://github.com/user-attachments/assets/b3009e8e-3efa-4743-a255-98fcfd6df22a" />

## 4. Features Overview

### 1️⃣ Resume & Job Description Parsing
- ✅ Extracts text from PDF, DOC, and DOCX resumes & job descriptions.
- ✅ Identifies required skills, experience levels, and key competencies.
- ✅ Supports multiple file formats with seamless parsing.

### 2️⃣ Secure File Handling
- ✅ Generates secure download/view URLs for resumes.
- ✅ Implements token-based authentication for access control.
- ✅ Ensures file type validation before processing.
- ✅ Encrypts stored resumes for added security.

### 3️⃣ AI-Driven Resume Screening & Matching
- ✅ Uses cosine similarity and NLP-based algorithms to score resumes.
- ✅ Filters candidates based on skills, experience range, and job requirements.
- ✅ Categorizes resumes into Perfect, Top, Good, Poor, & Not Good matches.
- ✅ Provides detailed analytics and reporting on candidate matching.

### 4️⃣ Job & Applicant Management (Frappe Integration)
- ✅ Fetches job openings & applicants from Frappe.
- ✅ Identifies open applications and retrieves relevant resumes.
- ✅ Automates shortlisting of top candidates based on AI scores.
- ✅ Enables recruiters to track hiring progress efficiently.

---

## 5. API Documentation

### 1️⃣ Process Resumes
- **Endpoint:** `/api/method/resume_lens.api.process_resumes`
- **Method:** `POST`
- **Description:** Parses job descriptions & resumes, evaluates them, and ranks candidates.
- **Request Parameters:**
```json
{
    "job_title_select": "Software Engineer",
    "jd_text": "Python, Django, REST API experience required"
}
```
- **Response Example:**
```json
{
    "status": "success",
    "Matched_Resumes": {
        "PerfectMatched": [
            {
                "applicant_name": "John Doe",
                "resume_name": "john_doe_resume.pdf",
                "score": "85.5%",
                "experience_years": 5,
                "resume_skills": ["Python", "Django", "REST API"],
                "view_url": "/api/method/resume_lens.api.view_matched_resume?token=xyz"
            }
        ]
    },
    "jd_required_skills": ["Python", "Django", "REST API"]
}
```

### 2️⃣ Secure Resume Download
- **Endpoint:** `/api/method/resume_lens.api.download_matched_resume?token={token}`
- **Method:** `GET`
- **Description:** Securely downloads the matched resume using a token-based URL.

### 3️⃣ View Matched Resume
- **Endpoint:** `/api/method/resume_lens.api.view_matched_resume?token={token}`
- **Method:** `GET`
- **Description:** Securely serves a resume file for viewing.

---

## 6. Backend (Frappe) API Implementation

The Frappe backend handles resume parsing, job description processing, and secure file handling.

### ✅ Key Functions: 
- `generate_download_token(filepath)` – Generates secure tokens for resume downloads.
- `get_secure_download_url(resume_url)` – Creates a secure download URL.
- `download_matched_resume(token)` – Serves a resume file for download.
- `process_resumes()` – Parses JDs & resumes, calculates matching scores, and ranks candidates.

---

## 7. Frontend (React) Implementation

### ✅ Key Features:
- Fetches job openings from the backend API.
- Allows users to upload job descriptions (text or file).
- Uploads resumes and submits them for processing.
- Displays ranked resumes based on AI scoring.
- Provides secure viewing & downloading of resumes.

---

## 8. Security & Permissions

- 🔹 Token-based security ensures that only authorized users can access resumes.
- 🔹 Access control mechanisms prevent unauthorized downloads and data leaks.
- 🔹 Whitelisted API methods enforce secure backend operations.
- 🔹 All resume processing is performed securely within the Frappe framework.

---

## 9. Performance Optimization
- ✅ Optimized resume parsing for faster processing.
- ✅ Implemented caching mechanisms for frequent queries.
- ✅ Asynchronous job processing for large-scale screening.

---

## 10. Error Handling & Debugging
- ✅ Implemented structured logging for backend events.
- ✅ Added detailed error messages for API responses.
- ✅ Exception handling for file upload and parsing errors.

---

## 11. Contributing

1️⃣ Fork the repository:
```bash
git clone https://github.com/AssimilateFrappe/resume_lens.git
```

2️⃣ Create a new feature branch:
```bash
git checkout -b feature-name
```

3️⃣ Commit your changes:
```bash
git commit -m "Added new feature"
```

4️⃣ Push to GitHub and open a pull request.

---

## 12. License

📜 **MIT License** – Open-source and free to use. Feel free to contribute and enhance ResumeLens!
