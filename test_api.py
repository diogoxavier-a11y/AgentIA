# test_api.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("INVOICEEXPRESS_API_KEY")
ACCOUNT = os.getenv("INVOICEEXPRESS_ACCOUNT")

if not API_KEY or not ACCOUNT:
    print("ERRO: configure INVOICEEXPRESS_API_KEY e INVOICEEXPRESS_ACCOUNT no .env")
    raise SystemExit(1)

def testar_busca_por_vat(vat):
    url = f"https://{ACCOUNT}.invoiceexpress.com/invoices.json"
    params = {"client_vat": vat}
    try:
        resp = requests.get(url, params=params, auth=(API_KEY, "x"), timeout=20)
        print("HTTP", resp.status_code)
        try:
            print("Response JSON preview:", resp.json())
        except Exception:
            print("Resposta não é JSON; conteúdo:", resp.text[:500])
        return resp
    except Exception as e:
        print("Erro ao chamar API:", e)
        return None

if __name__ == "__main__":
    exemplo_vat = "516154257"   # troque por um VAT válido da sua planilha
    testar_busca_por_vat(exemplo_vat)
