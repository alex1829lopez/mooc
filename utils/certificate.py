from reportlab.pdfgen import canvas
import os

def generate_certificate(name, score):

    path = f"certificates/{name}.pdf"

    c = canvas.Canvas(path)

    c.setFont("Helvetica-Bold", 28)

    c.drawString(
        120,
        700,
        "CERTIFICADO DE CONCLUSIÓN"
    )

    c.setFont("Helvetica", 18)

    c.drawString(
        120,
        620,
        f"Otorgado a: {name}"
    )

    c.drawString(
        120,
        580,
        f"Calificación: {score}"
    )

    c.save()

    return path