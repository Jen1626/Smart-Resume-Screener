import json
import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MATCH_PROMPT = """
You are an expert AI recruitment matching assistant.

Compare a candidate resume against a job description.

Your job is to perform SEMANTIC matching.

Do NOT simply count matching keywords.

Evaluate:

- technical skills
- programming languages
- frameworks
- tools
- relevant experience
- education
- projects
- certifications
- required skills
- preferred skills
- job responsibilities
- similarity between project/experience evidence and responsibilities

Return ONLY valid JSON.

Use exactly this structure:

{
  "match_score": 0,
  "strengths": [],
  "skill_gaps": [],
  "justification": ""
}

Scoring rules:

1. match_score must be between 1 and 10.
2. You may use one decimal place.
3. Strong evidence should receive more weight than keyword mentions.
4. Do not reward unrelated keywords.
5. Do not invent candidate experience.
6. Missing required skills should reduce the score.
7. Relevant projects can count as meaningful evidence.
8. Relevant certifications can support the match.
9. Education should be considered when relevant.
10. Explain WHY the candidate matches.
11. Identify important missing or weak requirements.
12. Keep the justification concise but informative.
13. Return JSON only.
14. Do not use markdown code fences.

CANDIDATE RESUME:
"""


def match_candidate(
    resume_text: str,
    job_description: str,
) -> dict:

    if not os.getenv("GEMINI_API_KEY"):
        return {
            "match_score": 0,
            "strengths": [],
            "skill_gaps": [],
            "justification": (
                "Add GEMINI_API_KEY "
                "to enable AI matching."
            ),
        }

    prompt = (
        MATCH_PROMPT
        + "\n"
        + resume_text[:30000]
        + "\n\nJOB DESCRIPTION:\n"
        + job_description[:20000]
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
        result = json.loads(raw)

    except json.JSONDecodeError:

        start = raw.find("{")
        end = raw.rfind("}")

        if start >= 0 and end > start:
            try:
                result = json.loads(
                    raw[start:end + 1]
                )
            except json.JSONDecodeError:
                raise ValueError(
                    "Gemini returned invalid JSON "
                    "for candidate matching."
                )
        else:
            raise ValueError(
                "Gemini returned invalid JSON "
                "for candidate matching."
            )

    # Safety validation
    try:
        score = float(
            result.get("match_score", 0)
        )
    except (TypeError, ValueError):
        score = 0

    score = max(
        0,
        min(10, score),
    )

    return {
        "match_score": round(score, 1),
        "strengths": result.get(
            "strengths",
            [],
        ),
        "skill_gaps": result.get(
            "skill_gaps",
            [],
        ),
        "justification": result.get(
            "justification",
            "",
        ),
    }