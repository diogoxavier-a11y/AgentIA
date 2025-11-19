import os
import requests
from loguru import logger

API_KEY = os.getenv("INVOICEEXPRESS_API_KEY")
ACCOUNT = os.getenv("INVOICEEXPRESS_ACCOUNT")

def buscar_faturas_por_vat(vat):
    if not API_KEY or not ACCOUNT:
        logger.error("API_KEY ou ACCOUNT não configurados no .env")
        return None

    url = f"https://{ACCOUNT}.invoiceexpress.com/invoices.json"
    params = {"client_vat": vat}

    try:
        resp = requests.get(url, params=params, auth=(API_KEY, "x"), timeout=20)
        resp.raise_for_status()
        data = resp.json()

        invoices = data.get("invoices", [])
        return invoices

    except Exception as e:
        logger.error(f"Erro ao consultar InvoiceExpress para VAT {vat}: {e}")
        return None


def filtrar_rascunhos(invoices):
    if not invoices:
        return []
    drafts = [inv for inv in invoices if inv.get("status") in ("draft", "rascunho")]
    return drafts
