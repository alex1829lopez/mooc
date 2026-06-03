from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from utils.youtube import get_video_id

client = OpenAI(api_key="TU_API_KEY")

def generate_modules_and_quizzes(url):

    video_id = get_video_id(url)

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    full_text = " ".join(
        [item["text"] for item in transcript]
    )

    size = len(full_text) // 3

    parts = [
        full_text[:size],
        full_text[size:size*2],
        full_text[size*2:]
    ]

    modules = []

    for idx, part in enumerate(parts):

        prompt = f"""
        Genera 15 preguntas de opción múltiple.

        Texto:
        {part}

        Formato JSON:
        [
          {{
            "question":"",
            "options":["","","",""],
            "correct":""
          }}
        ]
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"user","content":prompt}
            ]
        )

        modules.append({
            "title": f"Módulo {idx+1}",
            "content": part,
            "quiz": eval(response.choices[0].message.content)
        })

    return modules