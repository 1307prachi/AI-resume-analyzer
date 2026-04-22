from django.shortcuts import render, redirect
from .models import Resume, AnalysisResult
from django.conf import settings
from django.http import HttpResponse
import fitz
from groq import Groq
import json

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def upload_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')
        job_description = request.POST.get('job_description')

        resume = Resume.objects.create(
            name=name,
            file=file,
            job_description=job_description
        )


        resume_text = ""
        try:
            pdf = fitz.open(resume.file.path)
            for page in pdf:
                resume_text += page.get_text()
        except:
            resume_text = "Could not read PDF"

    
        try:
            client = Groq(api_key=settings.GROQ_API_KEY)

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "user",
                    "content": f"""
Return ONLY JSON:

{{
 "score": 0-100,
 "score_breakdown": {{
    "skills": 0-30,
    "experience": 0-20,
    "education": 0-10,
    "keywords": 0-40
 }},
 "matched_keywords": [],
 "missing_keywords": [],
 "suggestions": [],
 "summary": ""
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""
                }]
            )

            raw = response.choices[0].message.content.strip()

            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            result_data = json.loads(raw)

        except Exception as e:
            print("AI Error:", e)
            result_data = {
                "score": 0,
                "score_breakdown": {},
                "matched_keywords": [],
                "missing_keywords": [],
                "suggestions": ["Error analyzing resume"],
                "summary": "Analysis failed"
            }

        AnalysisResult.objects.create(
            resume=resume,
            score=result_data.get('score', 0),
            score_breakdown=result_data.get('score_breakdown', {}),
            matched_keywords=result_data.get('matched_keywords', []),
            missing_keywords=result_data.get('missing_keywords', []),
            suggestions=result_data.get('suggestions', []),
            summary=result_data.get('summary', "")
        )

        return redirect('result_page', pk=resume.pk)

    resumes = Resume.objects.all().order_by('-uploaded_at')
    return render(request, 'upload.html', {'resumes': resumes})


def result_page(request, pk):
    resume = Resume.objects.get(pk=pk)
    result = AnalysisResult.objects.filter(resume=resume).first()

    return render(request, 'result.html', {
        'resume': resume,
        'result': result
    })


def history_page(request):
    resumes = Resume.objects.all().order_by('-uploaded_at')
    return render(request, 'history.html', {'resumes': resumes})


def improve_resume(request, pk):
    resume = Resume.objects.get(pk=pk)

    pdf = fitz.open(resume.file.path)
    resume_text = ""
    for page in pdf:
        resume_text += page.get_text()

    client = Groq(api_key=settings.GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
Rewrite this resume in proper professional format.

Use:
- * for main bullet points
- + for sub points
- UPPERCASE headings

FORMAT:
NAME
CONTACT
SUMMARY
SKILLS
EDUCATION
PROJECTS
EXPERIENCE

RESUME:
{resume_text}
"""
        }]
    )

    improved_text = response.choices[0].message.content

    return render(request, 'improve.html', {
        'resume': resume,
        'improved_text': improved_text
    })


def download_report(request, pk):
    resume = Resume.objects.get(pk=pk)
    result = AnalysisResult.objects.filter(resume=resume).first()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, f"Name: {resume.name}")
    p.drawString(100, 780, f"Score: {result.score if result else 0}%")

    y = 750
    p.drawString(100, y, "Suggestions:")
    y -= 20

    if result:
        for s in result.suggestions:
            p.drawString(100, y, f"- {s}")
            y -= 20

    p.save()
    return response


def download_improved_resume(request, pk):
    resume = Resume.objects.get(pk=pk)

    pdf = fitz.open(resume.file.path)
    resume_text = ""
    for page in pdf:
        resume_text += page.get_text()

    client = Groq(api_key=settings.GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
Rewrite this resume in proper professional format.

Use:
- * for main bullet points
- + for sub points
- UPPERCASE headings

RESUME:
{resume_text}
"""
        }]
    )

    improved_text = response.choices[0].message.content

    response_pdf = HttpResponse(content_type='application/pdf')
    response_pdf['Content-Disposition'] = 'attachment; filename="improved_resume.pdf"'

    doc = SimpleDocTemplate(
        response_pdf,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    for line in improved_text.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 10))
            continue

        if line == line.upper() and " " in line and len(line) < 30:
            story.append(Paragraph(f"<b><font size=16>{line}</font></b>", styles["Title"]))
            story.append(Spacer(1, 12))

        elif line.isupper():
            story.append(Paragraph(f"<b><font size=13>{line}</font></b>", styles["Heading2"]))
            story.append(Spacer(1, 8))

        elif line.startswith("*"):
            clean = line.replace("*", "").strip()
            story.append(Paragraph(f"• {clean}", styles["Normal"]))

        elif line.startswith("+"):
            clean = line.replace("+", "").strip()
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;◦ {clean}", styles["Normal"]))

        else:
            story.append(Paragraph(line, styles["Normal"]))

        story.append(Spacer(1, 5))

    doc.build(story)

    return response_pdf