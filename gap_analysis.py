class GapAnalysis:
    def __init__(self, discrepancy_summary):
        self.summary = discrepancy_summary

    def analyze(self):
        missing_in_empresa_2 = self.summary["missing_in_empresa_2"]
        missing_in_empresa_1 = self.summary["missing_in_empresa_1"]

        empresa_1_routes = missing_in_empresa_2.groupby(['From Airport Code ICAO', 'To Airport Code ICAO']).size().sort_values(ascending=False).head()
        empresa_2_routes = missing_in_empresa_1.groupby(['Origin ICAO Code', 'Destination ICAO Code']).size().sort_values(ascending=False).head()

        return {
            "empresa_1_routes": empresa_1_routes,
            "empresa_2_routes": empresa_2_routes
        }