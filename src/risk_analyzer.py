class RiskAnalyzer:

    HIGH_RISK = {
        "Non-Compete",
        "Exclusivity",
        "Uncapped Liability",
        "Liquidated Damages",
        "Irrevocable Or Perpetual License",
        "Unlimited/All-You-Can-Eat-License"
    }

    MEDIUM_RISK = {
        "Anti-Assignment",
        "Change Of Control",
        "Termination For Convenience",
        "Minimum Commitment",
        "Volume Restriction",
        "Audit Rights",
        "Insurance",
        "Source Code Escrow"
    }

    LOW_RISK = {
        "Document Name",
        "Parties",
        "Agreement Date",
        "Effective Date",
        "Governing Law"
    }

    @classmethod
    def get_baseline_risk(
        cls,
        category
    ):

        if category in cls.HIGH_RISK:
            return "HIGH"

        if category in cls.MEDIUM_RISK:
            return "MEDIUM"

        if category in cls.LOW_RISK:
            return "LOW"

        return "MEDIUM"