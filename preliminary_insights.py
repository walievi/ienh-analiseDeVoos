class PreliminaryInsights:
    def __init__(self, discrepancy_summary):
        self.summary = discrepancy_summary

    def analyze(self):
        missing_in_empresa_2 = self.summary["missing_in_empresa_2"]
        missing_in_empresa_1 = self.summary["missing_in_empresa_1"]

        empresa_1_discrepancy_summary = missing_in_empresa_2.groupby(['Operator Name']).size().sort_values(ascending=False).head()
        empresa_2_discrepancy_summary = missing_in_empresa_1.groupby(['Operator']).size().sort_values(ascending=False).head()

        return {
            "empresa_1_summary": empresa_1_discrepancy_summary,
            "empresa_2_summary": empresa_2_discrepancy_summary
        }