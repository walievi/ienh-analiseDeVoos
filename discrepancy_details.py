class DiscrepancyDetails:
    def __init__(self, gap_analysis):
        self.gap_analysis = gap_analysis

    def get_details(self):
        empresa_1_routes = self.gap_analysis["empresa_1_routes"]
        empresa_2_routes = self.gap_analysis["empresa_2_routes"]

        return {
            "empresa_1_routes_details": empresa_1_routes,
            "empresa_2_routes_details": empresa_2_routes
        }