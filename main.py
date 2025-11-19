import os
from dotenv import load_dotenv
from loguru import logger
import pandas as pd

from sheet_reader import read_excel_vats
from invoice_client import buscar_faturas_por_vat, filtrar_rascunhos
from rpa_playwright import verificar_rascunho_via_web

load_dotenv()

def process_vat(vat):
    logger.info(f"Processando VAT {vat}")

    invoices = buscar_faturas_por_vat(vat)

    # API falhou → usar fallback Playwright
    if invoices is None:
        logger.warning("API falhou, usando automação web")
        from rpa_playwright import verificar_rascunho_via_web_sync
        return verificar_rascunho_via_web_sync(vat)


    drafts = filtrar_rascunhos(invoices)
    return drafts

def main():
    google_sheet_url = "https://docs.google.com/spreadsheets/d/1OoD3nli7GrYXXZBnFAVVHOSkV1D2pqlQ/export?format=xlsx"
    vats, df = read_excel_vats(google_sheet_url)

    resultados = []

    for vat in vats:
        drafts = process_vat(vat)
        resultados.append({"VAT": vat, "rascunhos": len(drafts)})

    out_df = pd.DataFrame(resultados)
    out_df.to_excel("resultado_final.xlsx", index=False)

    logger.info("Processo concluído. Arquivo salvo como resultado_final.xlsx")


if __name__ == "__main__":
    main()
