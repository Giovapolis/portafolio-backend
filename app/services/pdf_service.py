from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

def generate_cv_pdf(data: dict) -> bytes:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("cv.html")

    html_content = template.render(**data)

    pdf = HTML(string=html_content).write_pdf()

    return pdf