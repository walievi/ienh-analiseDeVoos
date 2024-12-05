from data_handler import DataHandler
from discrepancy_summary import DiscrepancySummary
from preliminary_insights import PreliminaryInsights
from gap_analysis import GapAnalysis
from discrepancy_details import DiscrepancyDetails
from fpdf import FPDF
import matplotlib.pyplot as plt


class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Comparação de Dados de Voo', align='C', ln=1)
        self.ln(5)

    def add_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, align='L', ln=1)
        self.ln(5)

    def add_paragraph(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln(5)

    def add_table(self, title, dataframe):
        self.add_title(title)
        self.set_font('Arial', '', 10)
        for i in range(len(dataframe)):
            row = dataframe.iloc[i]
            self.cell(0, 10, f'{", ".join(map(str, row.values))}', ln=1)
        self.ln(10)

    def add_image(self, title, image_path):
        self.add_title(title)
        self.image(image_path, x=10, w=180)
        self.ln(10)


def generate_graphs(preliminary_insights, gap_analysis):
    # Salvar gráficos temporários
    empresa_1_op_path = "empresa_1_operators.png"
    empresa_2_op_path = "empresa_2_operators.png"
    empresa_1_routes_path = "empresa_1_routes.png"
    empresa_2_routes_path = "empresa_2_routes.png"

    # Operadores
    plt.figure(figsize=(10, 6))
    preliminary_insights["empresa_1_summary"].plot(kind='bar', title='Operadores com maior número de voos ausentes na Empresa 2')
    plt.ylabel("Número de voos ausentes")
    plt.xlabel("Operadores - Empresa 1")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(empresa_1_op_path)
    plt.close()

    plt.figure(figsize=(10, 6))
    preliminary_insights["empresa_2_summary"].plot(kind='bar', title='Operadores com maior número de voos ausentes na Empresa 1')
    plt.ylabel("Número de voos ausentes")
    plt.xlabel("Operadores - Empresa 2")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(empresa_2_op_path)
    plt.close()

    # Rotas
    plt.figure(figsize=(10, 6))
    gap_analysis["empresa_1_routes"].plot(kind='bar', title='Rotas mais ausentes na Empresa 2 (Top 5)')
    plt.ylabel("Número de voos ausentes")
    plt.xlabel("Rotas - Empresa 1")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(empresa_1_routes_path)
    plt.close()

    plt.figure(figsize=(10, 6))
    gap_analysis["empresa_2_routes"].plot(kind='bar', title='Rotas mais ausentes na Empresa 1 (Top 5)')
    plt.ylabel("Número de voos ausentes")
    plt.xlabel("Rotas - Empresa 2")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(empresa_2_routes_path)
    plt.close()

    return empresa_1_op_path, empresa_2_op_path, empresa_1_routes_path, empresa_2_routes_path


def generate_pdf_report(discrepancy_summary, preliminary_insights, gap_analysis, discrepancy_details, image_paths, output_path="report.pdf"):
    pdf = PDFReport()
    pdf.add_page()

    # Resumo das discrepâncias
    pdf.add_title("Resumo das Discrepâncias")
    pdf.add_paragraph(f"Voos ausentes na Empresa 2: {discrepancy_summary['counts']['missing_in_empresa_2_count']}")
    pdf.add_paragraph(f"Voos ausentes na Empresa 1: {discrepancy_summary['counts']['missing_in_empresa_1_count']}")

    # Percepções preliminares
    pdf.add_title("Percepções Preliminares")
    pdf.add_paragraph("Operadores com maior número de voos ausentes:")
    pdf.add_image("Operadores - Empresa 1", image_paths[0])
    pdf.add_image("Operadores - Empresa 2", image_paths[1])

    # Análise das lacunas
    pdf.add_title("Análise das Lacunas")
    pdf.add_image("Rotas mais ausentes na Empresa 2", image_paths[2])
    pdf.add_image("Rotas mais ausentes na Empresa 1", image_paths[3])

    # Detalhamento das características
    pdf.add_title("Detalhamento das Características Comuns")
    pdf.add_table("Detalhes de Rotas - Empresa 1", discrepancy_details["empresa_1_routes_details"].reset_index())
    pdf.add_table("Detalhes de Rotas - Empresa 2", discrepancy_details["empresa_2_routes_details"].reset_index())

    # Salvar o PDF
    pdf.output(output_path)
    print(f"Relatório gerado: {output_path}")


# Inicializar a classe DataHandler
handler = DataHandler()

# Gerar resumo das discrepâncias
discrepancy_summary = DiscrepancySummary(handler).generate_summary()

# Percepções preliminares sobre voos ausentes/adicionais
preliminary_insights = PreliminaryInsights(discrepancy_summary).analyze()

# Análise das lacunas identificadas
gap_analysis = GapAnalysis(discrepancy_summary).analyze()

# Detalhamento das características comuns dos dados discrepantes
discrepancy_details = DiscrepancyDetails(gap_analysis).get_details()

# Gerar gráficos e salvar temporariamente
image_paths = generate_graphs(preliminary_insights, gap_analysis)

# Gerar o relatório em PDF
generate_pdf_report(discrepancy_summary, preliminary_insights, gap_analysis, discrepancy_details, image_paths, output_path="report.pdf")