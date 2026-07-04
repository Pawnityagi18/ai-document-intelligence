"""LLM service for answer generation"""

import logging
from typing import List, Tuple
import openai
from app.config import settings
from app.utils.errors import LLMError

logger = logging.getLogger(__name__)


class LLMService:
    """Generate answers using LLM"""

    def __init__(self):
        """Initialize LLM service"""
        openai.api_key = settings.openai_api_key
        self.model = settings.openai_model
        logger.info(f"Initialized LLMService with model: {self.model}")

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> Tuple[str, float]:
        """Generate answer based on context

        Args:
            question: User question
            context: Retrieved context from vector store

        Returns:
            Tuple of (answer, confidence_score)

        Raises:
            LLMError: If generation fails
        """
        try:
            logger.info(f"Generating answer for question: {question[:50]}...")

            system_prompt = (
                "You are a helpful assistant that answers questions based on "
                "the provided document context. "
                "\n\nRules:"
                "\n1. Be concise and direct. Start with the answer immediately."
                "\n2. If the answer is not in the context, explicitly say "
                "'I don't know' and explain what information is missing."
                "\n3. If you're uncertain, express that uncertainty."
                "\n4. Use the context to support your answer with specific details."
            )

            user_message = (
                f"Document Context:\n{context}\n\n"
                f"Question: {question}\n\n"
                f"Answer:"
            )

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )

            answer = response["choices"][0]["message"]["content"].strip()

            # Estimate confidence based on answer content
            # High confidence if answer is substantive, low if "I don't know"
            is_confident = (
                "i don't know" not in answer.lower() and 
                "cannot answer" not in answer.lower() and
                len(answer) > 50  # Substantive answer
            )
            confidence = 0.8 if is_confident else 0.2

            logger.info(
                f"Generated answer (confidence: {confidence:.2f}): "
                f"{answer[:50]}..."
            )
            return answer, confidence

        except Exception as e:
            error_msg = f"Failed to generate answer: {str(e)}"
            logger.error(error_msg)
            raise LLMError(error_msg) from e

    def count_tokens(
        self,
        text: str
    ) -> int:
        """Estimate token count for text

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Rough estimate: 1 token ≈ 4 characters
        return max(1, len(text) // 4)
