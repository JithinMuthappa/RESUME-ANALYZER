from flask import Flask, render_template, request, send_file
from utils import extract_text_from_pdf, clean_text, extract_skills
from model import predict_role, calculate_match
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Store last result for PDF generation
last_result = {}

# Job descriptions for matching
job_descriptions = {
    "Data Scientist": "python machine learning pandas numpy statistics data analysis",
    "Web Developer": "html css javascript react frontend bootstrap",
    "Software Engineer": "java backend mysql rest api data structures",
    "AI Engineer": "machine learning deep learning nlp computer vision"
}

required_skills = {
    "Data Scientist": ["python", "pandas", "machine learning", "statistics"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Software Engineer": ["java", "mysql", "data structures", "backend"],
    "AI Engineer": ["python", "deep learning", "nlp", "computer vision"]
}


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    skills = None
    match = 0
    missing_skills = None
    feedback = None

    # Get user name sent from Android WebView
    name = request.args.get("name", "User")

    if request.method == "POST":
        file = request.files["resume"]
        file_path = "uploaded_resume.pdf"
        file.save(file_path)

        text = extract_text_from_pdf(file_path)
        text = clean_text(text)

        role = predict_role(text)
        result = role

        skills = extract_skills(text)

        job_desc = job_descriptions.get(role, "")
        match = calculate_match(text, job_desc)

        required = required_skills.get(role, [])
        missing_skills = [skill for skill in required if skill not in skills]

        if missing_skills:
            feedback = (
                "To improve your chances for the role of "
                + role
                + ", consider learning: "
                + ", ".join(missing_skills)
            )
        else:
            feedback = "Your resume matches the required skills well."

        # Store data for PDF
        global last_result
        last_result = {
            "name": name,
            "role": result,
            "skills": ", ".join(skills),
            "match": match,
            "feedback": feedback
        }

    return render_template(
        "index.html",
        name=name,
        result=result,
        skills=skills,
        match=match,
        missing_skills=missing_skills,
        feedback=feedback
    )


@app.route("/download")
def download_pdf():
    pdf_path = "result.pdf"

    c = canvas.Canvas(pdf_path)

    c.drawString(100, 800, "Resume Analysis Report")
    c.drawString(100, 770, f"Name: {last_result.get('name','')}")
    c.drawString(100, 740, f"Predicted Role: {last_result.get('role','')}")
    c.drawString(100, 710, f"Skills: {last_result.get('skills','')}")
    c.drawString(100, 680, f"Match Score: {last_result.get('match','')}%")
    c.drawString(100, 650, f"Feedback: {last_result.get('feedback','')}")

    c.save()

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
