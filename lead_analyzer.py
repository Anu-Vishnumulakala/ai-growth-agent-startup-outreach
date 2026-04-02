import json
from openai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
    BadRequestError,
)
from src.openai_client import get_openai_client


def analyze_companies(companies: list[dict]) -> list[dict]:
    client = get_openai_client()

    company_lines = []
    for i, company in enumerate(companies, start=1):
        company_lines.append(
            f"{i}. Company Name: {company['company_name']}\n"
            f"   Website: {company['website']}\n"
            f"   Industry: {company['industry']}"
        )

    companies_text = "\n".join(company_lines)

    prompt = f"""
You are an AI growth analyst ranking startup leads for outreach.

Below is a list of companies. You must compare them directly and rank them against each other.

Companies:
{companies_text}

Evaluation criteria:
1. Market attractiveness
2. B2B value
3. Scalability
4. Outreach potential

Scoring rules:
- Use integer scores only.
- Use the range 5 to 10 realistically.
- Do NOT give every company the same score.
- If multiple companies are close, still rank them comparatively.
- Only truly exceptional companies should get 9 or 10.
- Strong companies should get 7 or 8.
- Moderate companies should get 5 or 6.
- Be selective and practical, not generous.

Writing rules:
- Keep summaries concise.
- Keep reasons concise and specific.
- Avoid generic phrases like "strong potential" or "great opportunity" unless followed by a concrete reason.
- Do NOT use placeholders like [Name], [Your Company], [specific area], etc.

Outreach message rules:
- Write like a real human, not robotic.
- Start naturally, for example: "Hi Qonto team," and not "Hello Qonto".
- Mention one specific strength of the company.
- Explain in one clear reason why collaboration or outreach makes sense.
- Keep it short and practical, around 2 to 3 lines.
- Avoid vague phrases like "your innovative approach" unless you explain what is innovative.
- Each message must include one specific detail about the company, such as its industry, product, business model, or market.

Language rules:
- Use SME or SMEs correctly for Small and Medium Enterprises.
- Never use "SMD".

Important output rules:
- Return EVERY input company EXACTLY ONCE.
- Do NOT duplicate company names.
- Do NOT invent new companies.
- Use the exact same company_name spelling as the input.

Return ONLY valid JSON.
Do not include markdown fences.
Do not include any extra text.

JSON format:
[
  {{
    "company_name": "exact company name from input",
    "summary": "1-2 concise lines",
    "score": 8,
    "reason": "clear practical reason",
    "message": "complete outreach message"
  }}
]
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        text = response.output_text.strip()
        parsed = json.loads(text)

        if not isinstance(parsed, list):
            raise Exception("Model did not return a list.")

        return parsed

    except AuthenticationError:
        raise Exception("Authentication failed. Check your OpenAI API key.")

    except RateLimitError:
        raise Exception("Rate limit reached or billing issue. Check OpenAI usage/billing.")

    except APITimeoutError:
        raise Exception("Request timed out. Please try again.")

    except APIConnectionError:
        raise Exception("Connection error. Check your internet and try again.")

    except BadRequestError as e:
        raise Exception(f"Bad request: {e}")

    except json.JSONDecodeError:
        raise Exception("Model returned invalid JSON. Please try again.")

    except Exception as e:
        raise Exception(f"Unexpected OpenAI error: {e}")
