# AI-resume-analyzer

# AI Resume Analyzer and Improver

An intelligent web application developed using Django and AI (Groq API) that evaluates resumes against job descriptions and generates a professionally improved, ATS-friendly resume.

---

## Overview

This project is designed to assist job seekers in understanding how well their resume aligns with a specific job role. It provides detailed analysis, identifies gaps, and generates a refined version of the resume in a structured and professional format.

---

## Features

* Resume Upload
  Users can upload resumes in PDF format for analysis.

* AI-Based Resume Analysis

  * Generates a match score (0–100)
  * Identifies matched and missing keywords
  * Provides personalized suggestions
  * Generates a concise summary

* Resume Improver

  * Rewrites the resume in a professional format
  * Organizes content into structured sections such as Skills, Education, Projects, and Experience
  * Optimizes the resume for Applicant Tracking Systems (ATS)

* Score Breakdown
  Provides detailed scoring based on skills, experience, education, and keyword matching.

* Download Functionality

  * Download analysis report as PDF
  * Download improved resume in a clean, formatted PDF

* History Tracking
  Maintains a record of previously analyzed resumes for quick access.

---

## Technology Stack

* Backend: Django (Python)
* Frontend: HTML, Tailwind CSS
* AI Integration: Groq API (LLaMA model)
* PDF Processing: PyMuPDF (fitz)
* PDF Generation: ReportLab
* Database: SQLite

---

## Workflow

1. Upload a resume along with a job description
2. The system analyzes the resume using AI
3. A match score and detailed insights are generated
4. Users can view suggestions and summary
5. The resume can be improved using AI
6. The improved resume can be downloaded as a formatted PDF

---

## Use Cases

* Resume enhancement for job applications
* Improving compatibility with ATS systems
* Identifying skill gaps
* Academic and portfolio projects

---

## Future Enhancements

* User authentication and personalized dashboards
* Resume comparison feature
* Multiple resume templates
* Export to Word format (.docx)
* Deployment on cloud platforms

---

## Author

Prachi Patel
MCA Student | Data Science Enthusiast
