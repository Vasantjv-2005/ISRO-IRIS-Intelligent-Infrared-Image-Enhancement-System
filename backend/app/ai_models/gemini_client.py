"""
Gemini Client

Production-ready Google Gemini client.
"""

from __future__ import annotations

import google.generativeai as genai

from app.core.config import GEMINI_API_KEY


class GeminiClient:
    """
    Wrapper around Google's Gemini API.
    """

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
    ) -> None:
        from app.core.settings import settings

        if not GEMINI_API_KEY and not settings.GROQ_API_KEY:
            raise ValueError(
                "Both GEMINI_API_KEY and GROQ_API_KEY are missing."
            )

        self.model = None
        if GEMINI_API_KEY:
            try:
                genai.configure(
                    api_key=GEMINI_API_KEY,
                )
                self.model = genai.GenerativeModel(
                    model_name=model_name,
                )
            except Exception as exc:
                print(f"Failed to configure Gemini: {exc}")

    # -----------------------------------------------------
    # Generate Text
    # -----------------------------------------------------

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate text using Gemini with automatic fallback to Groq AI.
        """
        # Try Gemini first
        if self.model and GEMINI_API_KEY:
            try:
                response = self.model.generate_content(prompt)
                if response.text:
                    return response.text.strip()
            except Exception as exc:
                print(f"Gemini generation failed ({exc}). Falling back to Groq AI...")

        # Fallback to Groq
        from app.core.settings import settings
        if settings.GROQ_API_KEY:
            try:
                from groq import Groq
                client = Groq(api_key=settings.GROQ_API_KEY)
                completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=settings.GROQ_MODEL or "llama-3.3-70b-versatile",
                )
                if completion.choices and completion.choices[0].message.content:
                    return completion.choices[0].message.content.strip()
            except Exception as groq_exc:
                print(f"Groq generation failed: {groq_exc}")
                raise RuntimeError(f"Both Gemini and Groq AI failed. Groq error: {groq_exc}") from groq_exc

        return ""

    # -----------------------------------------------------
    # Scene Analysis
    # -----------------------------------------------------

    def analyze_scene(
        self,
        image_name: str,
        detected_objects: list[dict],
    ) -> str:
        """
        Generate a natural-language scene analysis.
        """

        prompt = f"""
You are an expert infrared image analyst.

Image:
{image_name}

Detected Objects:
{detected_objects}

Provide:

1. Scene summary
2. Object observations
3. Possible anomalies
4. Safety concerns
5. Short conclusion

Keep the answer professional.
"""

        return self.generate(prompt)

    # -----------------------------------------------------
    # Report Summary
    # -----------------------------------------------------

    def generate_summary(
        self,
        analysis: str,
    ) -> str:
        """
        Generate a concise summary.
        """

        prompt = f"""
Summarize the following AI report
in less than 120 words.

{analysis}
"""

        return self.generate(prompt)


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

gemini_client = GeminiClient()