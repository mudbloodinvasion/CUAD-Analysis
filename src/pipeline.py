import yaml

from .retriever import ContractRetriever
from .llm import GeminiAnalyzer
from .risk_analyzer import RiskAnalyzer


# --------------------------------------------------
# CUAD CLAUSE CATEGORIES
# --------------------------------------------------

CUAD_CATEGORIES = [

    "Document Name",
    "Parties",
    "Agreement Date",
    "Effective Date",
    "Expiration Date",
    "Renewal Term",
    "Notice Period To Terminate Renewal",
    "Governing Law",

    "Most Favored Nation",
    "Non-Compete",
    "Exclusivity",
    "No-Solicit Of Customers",
    "Competitive Restriction Exception",
    "No-Solicit Of Employees",
    "Non-Disparagement",

    "Termination For Convenience",
    "Rofr/Rofo/Rofn",
    "Change Of Control",
    "Anti-Assignment",

    "Revenue/Profit Sharing",
    "Price Restrictions",
    "Minimum Commitment",
    "Volume Restriction",

    "Ip Ownership Assignment",
    "Joint Ip Ownership",
    "License Grant",
    "Non-Transferable License",
    "Affiliate License-Licensor",
    "Affiliate License-Licensee",
    "Unlimited/All-You-Can-Eat-License",
    "Irrevocable Or Perpetual License",

    "Source Code Escrow",
    "Post-Termination Services",
    "Audit Rights",
    "Uncapped Liability",
    "Cap On Liability",
    "Liquidated Damages",
    "Warranty Duration",
    "Insurance",
    "Covenant Not To Sue",
    "Third Party Beneficiary"
]


# --------------------------------------------------
# CONTRACT RISK PIPELINE
# --------------------------------------------------

class ContractRiskPipeline:

    def __init__(self):

        # ------------------------------------------
        # LOAD CONFIGURATION
        # ------------------------------------------

        with open(
            "config/config.yaml",
            "r",
            encoding="utf-8"
        ) as file:

            self.config = yaml.safe_load(
                file
            )

        # ------------------------------------------
        # INITIALIZE RETRIEVER
        # ------------------------------------------

        self.retriever = ContractRetriever(
            self.config["embeddings"]["model"]
        )

        # ------------------------------------------
        # INITIALIZE GEMINI
        # ------------------------------------------

        self.llm = GeminiAnalyzer(
            self.config["llm"]["model"]
        )

    # --------------------------------------------------
    # PREPARE DOCUMENT
    # --------------------------------------------------

    def prepare_document(
        self,
        text
    ):

        self.retriever.create_chunks(
            text,

            chunk_size=self.config[
                "document"
            ]["chunk_size"],

            chunk_overlap=self.config[
                "document"
            ]["chunk_overlap"]
        )

        self.retriever.build_index()

    # --------------------------------------------------
    # ANALYZE CONTRACT
    # --------------------------------------------------

    def analyze_contract(
        self,
        text,
        categories=None
    ):

        # ------------------------------------------
        # PREPARE DOCUMENT
        # ------------------------------------------

        self.prepare_document(
            text
        )

        # ------------------------------------------
        # USE ALL CUAD CATEGORIES BY DEFAULT
        # ------------------------------------------

        if categories is None:

            categories = CUAD_CATEGORIES

        # ------------------------------------------
        # RETRIEVE RELEVANT CONTRACT PASSAGES
        # ------------------------------------------

        retrieval_queries = [

            "contract parties dates term renewal termination",

            "non-compete exclusivity non-solicitation restrictions",

            "assignment change of control termination rights",

            "intellectual property ownership licenses",

            "pricing payment commitments volume restrictions",

            "liability indemnification damages warranties insurance",

            "audit rights confidentiality governing law dispute resolution"
        ]

        retrieved_passages = []

        for query in retrieval_queries:

            results = self.retriever.search(
                query,
                top_k=3
            )

            retrieved_passages.extend(
                results
            )

        # ------------------------------------------
        # REMOVE DUPLICATE PASSAGES
        # ------------------------------------------

        seen = set()

        unique_passages = []

        for result in retrieved_passages:

            passage = result["text"]

            if passage not in seen:

                seen.add(
                    passage
                )

                unique_passages.append(
                    passage
                )

        # ------------------------------------------
        # BUILD GEMINI CONTEXT
        # ------------------------------------------

        context_parts = []

        for i, passage in enumerate(
            unique_passages,
            start=1
        ):

            context_parts.append(
                f"[PASSAGE {i}]\n{passage}"
            )

        context = "\n\n".join(
            context_parts
        )

        # ------------------------------------------
        # GEMINI CALL #1
        #
        # Analyze ALL CUAD categories in one call
        # ------------------------------------------

        clause_response = (
            self.llm.analyze_clauses(
                categories,
                context
            )
        )

        # ------------------------------------------
        # HANDLE GEMINI ERROR
        # ------------------------------------------

        if "error" in clause_response:

            return {
                "contract_report": clause_response,
                "clause_results": []
            }

        # ------------------------------------------
        # EXTRACT CLAUSE RESULTS
        # ------------------------------------------

        clause_results = clause_response.get(
            "results",
            []
        )

        # ------------------------------------------
        # ADD BASELINE RISK
        # ------------------------------------------

        for item in clause_results:

            category = item.get(
                "category",
                ""
            )

            baseline_risk = (
                RiskAnalyzer.get_baseline_risk(
                    category
                )
            )

            item["baseline_risk"] = (
                baseline_risk
            )

        # ------------------------------------------
        # GEMINI CALL #2
        #
        # Overall contract risk report
        # ------------------------------------------

        report = (
            self.llm.generate_contract_report(
                clause_results
            )
        )

        # ------------------------------------------
        # FORMAT RESULTS FOR STREAMLIT
        # ------------------------------------------

        formatted_results = []

        for item in clause_results:

            category = item.get(
                "category",
                "Unknown"
            )

            present = item.get(
                "present",
                False
            )

            baseline_risk = item.get(
                "baseline_risk",
                "MEDIUM"
            )

            # --------------------------------------
            # Risk is NONE if clause is absent
            # Otherwise use category baseline
            # --------------------------------------

            if present:

                risk_level = baseline_risk

            else:

                risk_level = "NONE"

            # --------------------------------------
            # Build result
            # --------------------------------------

            formatted_results.append({

                "category": category,

                "clause_analysis": {

                    "category": category,

                    "present": present,

                    "evidence": item.get(
                        "evidence",
                        ""
                    ),

                    "summary": item.get(
                        "summary",
                        ""
                    ),

                    "confidence": item.get(
                        "confidence",
                        0
                    )
                },

                "risk_analysis": {

                    "category": category,

                    "risk_level": risk_level,

                    "risk_reason": (
                        "Baseline risk assigned "
                        "based on the CUAD category."
                        if present
                        else
                        "Clause was not identified "
                        "in the retrieved passages."
                    ),

                    "problematic_elements": [],

                    "review_recommendation": (
                        "Human review recommended."
                        if (
                            present
                            and risk_level in [
                                "HIGH",
                                "MEDIUM"
                            ]
                        )
                        else ""
                    ),

                    "confidence": item.get(
                        "confidence",
                        0
                    )
                }
            })

        # ------------------------------------------
        # RETURN COMPLETE RESULT
        # ------------------------------------------

        return {

            "contract_report": report,

            "clause_results": formatted_results
        }

    # --------------------------------------------------
    # CONTRACT QUESTION ANSWERING
    # --------------------------------------------------

    def answer_question(
        self,
        question
    ):

        # ------------------------------------------
        # Retrieve relevant passages
        # ------------------------------------------

        context = (
            self.retriever.get_context(
                question,
                self.config[
                    "retrieval"
                ]["top_k"]
            )
        )

        # ------------------------------------------
        # Send retrieved context to Gemini
        # ------------------------------------------

        return self.llm.answer_question(
            question,
            context
        )

    # --------------------------------------------------
    # BUILD CATEGORY QUERY
    # --------------------------------------------------

    @staticmethod
    def _build_query(
        category
    ):

        return (
            f"Find passages related to the "
            f"contract clause category: "
            f"{category}"
        )