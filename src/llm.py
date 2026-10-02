import os
import json

from pathlib import Path
from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiAnalyzer:

    def __init__(
        self,
        model="gemini-3.1-flash-lite"
    ):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add it to your .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

        self.prompt_dir = Path("prompts")

    # --------------------------------------------------
    # LOAD PROMPT
    # --------------------------------------------------

    def _load_prompt(
        self,
        filename,
        **kwargs
    ):

        path = self.prompt_dir / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Prompt file not found: {path}"
            )

        template = path.read_text(
            encoding="utf-8"
        )

        return template.format(
            **kwargs
        )

    # --------------------------------------------------
    # GENERATE JSON
    # --------------------------------------------------

    def _generate_json(
        self,
        prompt
    ):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": 0
            }
        )

        output = response.text.strip()

        if output.startswith("```"):

            output = output.replace(
                "```json",
                ""
            )

            output = output.replace(
                "```",
                ""
            )

            output = output.strip()

        try:

            return json.loads(output)

        except json.JSONDecodeError:

            return {
                "error": "Invalid JSON returned by Gemini",
                "raw_output": output
            }

    # --------------------------------------------------
    # BATCH CLAUSE ANALYSIS
    # --------------------------------------------------

    def analyze_clauses(
        self,
        categories,
        context
    ):

        prompt = self._load_prompt(
            "clause_classification.txt",
            categories=json.dumps(
                categories,
                indent=2
            ),
            context=context
        )

        return self._generate_json(
            prompt
        )

    # --------------------------------------------------
    # CONTRACT SUMMARY + RISK ANALYSIS
    # --------------------------------------------------

    def generate_contract_report(
        self,
        results
    ):

        prompt = self._load_prompt(
            "contract_summary.txt",
            results=json.dumps(
                results,
                indent=2
            )
        )

        return self._generate_json(
            prompt
        )

    # --------------------------------------------------
    # QUESTION ANSWERING
    # --------------------------------------------------

    def answer_question(
        self,
        question,
        context
    ):

        prompt = self._load_prompt(
            "qna.txt",
            question=question,
            context=context
        )

        return self._generate_json(
            prompt
        )