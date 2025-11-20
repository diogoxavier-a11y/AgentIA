import os
from dotenv import load_dotenv
from loguru import logger
import pandas as pd

from sheet_reader import read_excel_vats
from invoice_client import (
    buscar_cliente_por_vat,
    buscar_faturas_por_cliente,
    filtrar_rascunhos,
)
from rpa_playwright import verificar_rascunho_via_web

load_dotenv()

def process_vat(vat):
    logger.info(f"Processando VAT {vat}")

    # 1 — Buscar cliente
    cliente = buscar_cliente_por_vat(vat)

    if not cliente:
        logger.warning(f"Sem cliente para VAT {vat}")
        return []

    client_id = cliente["id"]

    # 2 — Buscar faturas desse cliente
    invoices = buscar_faturas_por_cliente(client_id)

    # 3 — Filtrar rascunhos
    drafts = filtrar_rascunhos(invoices)

    return drafts

def main():
    google_sheet_url = "https://docs.google.com/spreadsheets/d/1OoD3nli7GrYXXZBnFAVVHOSkV1D2pqlQ/export?format=xlsx"
    vats, df = read_excel_vats(google_sheet_url)

    resultados = []

    for vat in vats:
        drafts = process_vat(vat)
        resultados.append({"VAT": vat, "rascunhos": len(drafts)})

    # Criar DataFrame
    out_df = pd.DataFrame(resultados)

    # Ordenar do maior para o menor número de rascunhos
    out_df = out_df.sort_values(by="rascunhos", ascending=False)

    # Salvar em Excel com filtro automático
    with pd.ExcelWriter("resultado_final.xlsx", engine="openpyxl") as writer:
        out_df.to_excel(writer, index=False, sheet_name="Resultados")
        sheet = writer.sheets["Resultados"]

        # Adicionar filtro
        sheet.auto_filter.ref = sheet.dimensions

        # Ajustar automaticamente a largura das colunas
        for column_cells in sheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            col_letter = column_cells[0].column_letter
            sheet.column_dimensions[col_letter].width = length + 2


if __name__ == "__main__":
    main()
