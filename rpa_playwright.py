import asyncio
from playwright.async_api import async_playwright
from loguru import logger
import os

async def verificar_rascunho_via_web(vat):
    try:
        email = os.getenv("invoice.express@lovelystay.com")
        password = os.getenv("cag_VRP9edt@wjv0zmt")

        if not email or not password:
            logger.error("Credenciais IE_EMAIL ou IE_PASSWORD faltando no .env")
            return []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 1. Acessa o site correto
            await page.goto("https://invoicexpress.com/")

            # 2. Clicar em Login
            await page.click("text=Login")

            # 3. Preencher email e senha
            await page.fill("input[name='user[email]']", email)
            await page.fill("input[name='user[password]']", password)

            # 4. Submeter login
            await page.click("button[type='submit']")

            # 5. Ir para a área de Faturas
            await page.wait_for_load_state("networkidle")
            await page.goto("https://app.invoicexpress.com/invoices")

            # 6. Buscar pelo VAT
            await page.fill("input[name='search[query]']", vat)
            await page.press("input[name='search[query]']", "Enter")

            await page.wait_for_load_state("networkidle")

            # 7. Verificar se aparece algum item com estado "rascunho"
            rows = await page.query_selector_all("tr.invoice-row")

            drafts = []

            for r in rows:
                status = await r.query_selector("span.status")
                if status:
                    stext = (await status.inner_text()).strip().lower()
                    if "rascunho" in stext or "draft" in stext:
                        drafts.append(await r.inner_text())

            await browser.close()
            return drafts

    except Exception as e:
        logger.error(f"Playwright erro no VAT {vat}: {e}")
        return []


def verificar_rascunho_via_web_sync(vat):
    return asyncio.run(verificar_rascunho_via_web(vat))
