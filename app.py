from flask import Flask, render_template, request, session, redirect
from utils.youtube import get_video_id
from utils.quiz_generator import generate_modules_and_quizzes
from utils.certificate import generate_certificate

app = Flask(__name__)
app.secret_key = "curso_secret"

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        youtube_url = request.form["youtube_url"]

        modules = generate_modules_and_quizzes(youtube_url)

        session["modules"] = modules
        session["video_url"] = youtube_url
        session["current"] = 0
        session["score"] = 0

        return redirect("/module/0")

    return render_template("index.html")


@app.route("/module/<int:index>", methods=["GET", "POST"])
def module(index):

    modules = session["modules"]

    if request.method == "POST":

        score = 0

        for i, q in enumerate(modules[index]["quiz"]):

            answer = request.form.get(f"q{i}")

            if answer == q["correct"]:
                score += 1

        session["score"] += score

        if index + 1 < len(modules):
            return redirect(f"/module/{index+1}")

        return redirect("/certificate")

    return render_template(
        "module.html",
        module=modules[index],
        index=index
    )


@app.route("/certificate")
def certificate():

    score = session["score"]

    if score >= 30:
        pdf = generate_certificate(
            "Alumno",
            score
        )

        return render_template(
            "certificate.html",
            score=score,
            pdf=pdf
        )

    return f"No aprobado. Puntuación: {score}"


if __name__ == "__main__":
    app.run(debug=True)