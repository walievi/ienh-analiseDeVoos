import pandas as pd

class DataHandler:
    def __init__(self):
        self.data_empresa_1 = pd.read_excel("Files/dataset-empresa-1.xlsx")
        self.data_empresa_2 = pd.read_csv("Files/dataset-empresa-2.csv")
        self.equivalenciasOperators = pd.read_csv("Files/equivalenciasNomes.csv", sep=';')
        self._prepare_unique_ids()

    def _prepare_unique_ids(self):
        self.normalizeEmpresa1()
        self.normalizeEmpresa2()

    def normalizeEmpresa1(self):
        required_colluns = [
            'Aircraft Registration No',
            'From Airport Code ICAO',
            'To Airport Code ICAO',
            'Flight Date Time',
        ]
        self.data_empresa_1.dropna(subset=required_colluns, inplace=True)

        self.data_empresa_1['Operator Name'] = self.data_empresa_1['Operator Name'].apply(self.sanitizeNames)
        self.data_empresa_1['Flight Date'] = pd.to_datetime(self.data_empresa_1['Flight Date Time']).dt.date

        self.data_empresa_1['unique_id'] = (
            self.data_empresa_1['Flight Date'].astype(str) + "_" +
            self.data_empresa_1['Aircraft Registration No'].astype(str).str.strip().str.upper() + "_" +
            self.data_empresa_1['From Airport Code ICAO'].astype(str).str.strip().str.upper() + "_" +
            self.data_empresa_1['To Airport Code ICAO'].astype(str).str.strip().str.upper()
        )

    def normalizeEmpresa2(self):
        required_colluns = [
            'Operator',
            'Origin ICAO Code',
            'Destination ICAO Code',
            'Fir Started',
        ]
        self.data_empresa_2.dropna(subset=required_colluns, inplace=True)

        self.data_empresa_2['Operator'] = self.data_empresa_2['Operator'].apply(self.sanitizeNames)
        self.data_empresa_2['Flight Date'] = pd.to_datetime(
            self.data_empresa_2['Fir Started'],
            format='%Y-%m-%d @ %H:%M UTC',
            errors='coerce'
        ).dt.date

        self.data_empresa_2['unique_id'] = (
            self.data_empresa_2['Flight Date'].astype(str) + "_" +
            self.data_empresa_2['Aircraft Registration'].astype(str).str.strip().str.upper() + "_" +
            self.data_empresa_2['Origin ICAO Code'].astype(str).str.strip().str.upper() + "_" +
            self.data_empresa_2['Destination ICAO Code'].astype(str).str.strip().str.upper()
        )

    def sanitizeNames(self, value):
        if pd.isna(value):  # Lida com valores nulos
            return None

        value = str(value).upper()
        equivalencias = self.equivalenciasOperators
        result = equivalencias[equivalencias['value'] == value]['name']

        return result.iloc[0] if not result.empty else value

    def getEmp1(self):
        return self.data_empresa_1

    def getEmp2(self):
        return self.data_empresa_2

    def merge_data(self):
        merged_data = pd.merge(
            self.data_empresa_1,
            self.data_empresa_2,
            on='unique_id',
            how='inner',
            suffixes=('_empresa_1', '_empresa_2')
        )
        return merged_data