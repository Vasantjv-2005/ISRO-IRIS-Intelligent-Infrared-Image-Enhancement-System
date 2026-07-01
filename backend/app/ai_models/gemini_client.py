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

        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing."
            )

        genai.configure(
            api_key=GEMINI_API_KEY,
        )

        self.model = genai.GenerativeModel(
            model_name=model_name,
        )

    # -----------------------------------------------------
    # Generate Text
    # -----------------------------------------------------

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate text using Gemini.
        """

        response = self.model.generate_content(
            prompt
        )

        if response.text:
            return response.text.strip()

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