class DiscrepancySummary:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def generate_summary(self):
        data_empresa_1 = self.data_handler.getEmp1()
        data_empresa_2 = self.data_handler.getEmp2()

        missing_in_empresa_2 = data_empresa_1[~data_empresa_1['unique_id'].isin(data_empresa_2['unique_id'])]
        missing_in_empresa_1 = data_empresa_2[~data_empresa_2['unique_id'].isin(data_empresa_1['unique_id'])]

        return {
            "missing_in_empresa_2": missing_in_empresa_2,
            "missing_in_empresa_1": missing_in_empresa_1,
            "counts": {
                "missing_in_empresa_2_count": missing_in_empresa_2.shape[0],
                "missing_in_empresa_1_count": missing_in_empresa_1.shape[0]
            }
        }