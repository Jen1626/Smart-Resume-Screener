import json
import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


RESUME_PROMPT = """
You are an expert resume information extraction system.

Your task is to convert the supplied resume text into structured
candidate information.

Extract ONLY information explicitly supported by the resume.

Return ONLY valid JSON.

Use exactly these keys:

{
  "name": "",
  "email": "",
  "phone": "",
  "skills": [],
  "education": [],
  "experience": [],
  "projects": [],
  "certifications": []
}

Rules:

1. Never invent information.
2. If information is unavailable, use an empty string or [].
3. Skills should contain concrete technical/professional skills.
4. Education should contain degree, institution and relevant details.
5. Experience should contain internships, jobs or relevant professional experience.
6. Projects should contain project names and useful descriptions.
7. Certifications should contain certification names.
8. Preserve important technologies and tools.
9. Do not include markdown.
10. Do not wrap the JSON in ```json fences.
11. Return JSON only.

RESUME TEXT:
"""


def parse_resume(text: str) -> dict:

    if not os.getenv("GEMINI_API_KEY"):
        return {
            "name": "Unknown Candidate",
            "email": "",
            "phone": "",
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": [],
        }

    prompt = (
        RESUME_PROMPT
        + "\n"
        + text[:30000]
    )

    response = client.models.generate_content(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        ),
        contents=prompt,
    )

    raw = response.text.strip()

    # Remove accidental markdown fences
    if raw.startswith("```"):
        raw = raw.replace(
            "```json",
            "",
            1,
        ).replace(
            "```",
            "",
        ).strip()

    try:
        return json.loads(raw)

    except json.JSONDecodeError:

        start = raw.find("{")
        end = raw.rfind("}")

        if start >= 0 and end > start:
            try:
                return json.loads(
                    raw[start:end + 1]
                )
            except json.JSONDecodeError:
                pass

        raise ValueError(
            "Gemini returned invalid JSON "
            "for resume extraction."
        )
