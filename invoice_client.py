import os
import requests
from loguru import logger

API_KEY = os.getenv("INVOICEEXPRESS_API_KEY")
ACCOUNT = os.getenv("INVOICEEXPRESS_ACCOUNT")

BASE_URL = f"https://{ACCOUNT}.invoiceexpress.com"


def buscar_cliente_por_vat(vat):
    url = f"{BASE_URL}/clients.json"
    params = {"vat": vat}

    try:
        resp = requests.get(url, params=params, auth=(API_KEY, "x"), timeout=20)
        resp.raise_for_status()

        data = resp.json()
        clients = data.get("clients", [])

        if not clients:
            logger.warning(f"Nenhum cliente encontrado para VAT {vat}")
            return None

        return clients[0]  # sempre pega o primeiro

    except Exception as e:
        logger.error(f"Erro ao buscar cliente VAT {vat}: {e}")
        return None


def buscar_faturas_por_cliente(client_id):
    url = f"{BASE_URL}/clients/{client_id}/invoices.json"

    try:
        resp = requests.get(url, auth=(API_KEY, "x"), timeout=20)
        resp.raise_for_status()

        data = resp.json()
        return data.get("invoices", [])

    except Exception as e:
        logger.error(f"Erro ao buscar faturas do cliente {client_id}: {e}")
        return []


def filtrar_rascunhos(invoices):
    drafts = [inv for inv in invoices if inv.get("state") == "draft"]
    return drafts
