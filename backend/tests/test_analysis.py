"""
Tests for AI Analysis Service.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from app.middleware.error_handler import AIModelException
from app.services.ai.analysis_service import analysis_service


class TestAnalysisService(unittest.TestCase):
    """
    Tests for AnalysisService.
    """

    @patch("google.generativeai.GenerativeModel")
    def test_analyze_success(self, mock_model_class: MagicMock) -> None:
        """
        Verify that analysis_service successfully generates content using Gemini.
        """
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Mocked scene analysis summary."
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        # Reset service model for mock test
        with patch.object(analysis_service, "model", mock_model):
            result = analysis_service.analyze(
                detected_objects=[{"class_id": 0, "class_name": "human", "confidence": 0.9, "bbox": [10, 10, 50, 50]}],
                image_name="test_scene.jpg",
            )

            self.assertTrue(result["success"])
            self.assertEqual(result["image"], "test_scene.jpg")
            self.assertEqual(result["analysis"], "Mocked scene analysis summary.")

    @patch("app.services.ai.analysis_service.settings")
    @patch("google.generativeai.GenerativeModel")
    def test_analyze_failure_raises_ai_exception(self, mock_model_class: MagicMock, mock_settings: MagicMock) -> None:
        """
        Verify that exceptions raised by Gemini are caught and re-raised as AIModelException when no fallback is available.
        """
        mock_settings.GEMINI_API_KEY = "test"
        mock_settings.GROQ_API_KEY = ""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API connection error")
        mock_model_class.return_value = mock_model

        with patch.object(analysis_service, "model", mock_model):
            with self.assertRaises(AIModelException):
                analysis_service.analyze(
                    detected_objects=[],
                    image_name="test_scene.jpg",
                )

    @patch("app.services.ai.analysis_service.settings")
    @patch("groq.Groq")
    @patch("google.generativeai.GenerativeModel")
    def test_analyze_groq_fallback_success(self, mock_model_class: MagicMock, mock_groq: MagicMock, mock_settings: MagicMock) -> None:
        """
        Verify that when Gemini fails, analysis falls back to Groq successfully.
        """
        mock_settings.GEMINI_API_KEY = "test"
        mock_settings.GROQ_API_KEY = "test_groq"
        mock_settings.GROQ_MODEL = "llama-3.3-70b-versatile"

        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("Gemini Quota Exceeded")
        mock_model_class.return_value = mock_model

        mock_groq_instance = MagicMock()
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Groq fallback analysis."
        mock_completion.choices = [mock_choice]
        mock_groq_instance.chat.completions.create.return_value = mock_completion
        mock_groq.return_value = mock_groq_instance

        with patch.object(analysis_service, "model", mock_model):
            result = analysis_service.analyze(
                detected_objects=[],
                image_name="test_scene.jpg",
            )
            self.assertTrue(result["success"])
            self.assertEqual(result["analysis"], "Groq fallback analysis.")
