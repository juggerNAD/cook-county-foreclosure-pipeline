import asyncio
import pandas as pd
import json
import random
from playwright.async_api import async_playwright

PHASE3_CSV = "phase3_results.csv"
PHASE4_CSV = "phase4_results.csv"
PHASE4_JSON = "phase4_results.json"

URL = "https://casesearch.cookcountyclerkofcourt.org/CivilCaseSearchAPI.aspx"

EXCLUDED_EVENTS = [
    "CERTIFICATE OF SALE",
    "RECEIPT OF SALE",
    "REPORT OF SALE",
    "SHERIFF’S SALE APPROVED",
    "SHERIFF'S SALE APPROVED",
    "MORTGAGE FORECLOSURE DISPOSED",
    "DISMISSED",
    "VOLUNTARY DISMISSAL",
    "SALE VACATED",
    "ORDER FOR POSSESSION",
    "EVICTION",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    # Add more user agents if needed
]

def safe_str(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

async def check_case(page, case_number):
    await page.goto(URL, timeout=60000)
    await page.wait_for_selector("#MainContent_txtCaseNumber", timeout=60000)

    await page.fill("#MainContent_txtCaseNumber", "")
    await page.fill("#MainContent_txtCaseNumber", case_number)
    await page.click("#MainContent_btnSearch")

    await page.wait_for_timeout(3000)

    page_text = (await page.inner_text("body")).upper()

    for event in EXCLUDED_EVENTS:
        if event in page_text:
            return "EXCLUDED", "RED"

    if "JUDGMENT OF FORECLOSURE" in page_text:
        return "JUDGMENT OF FORECLOSURE", "GREEN"

    return "NO JUDGMENT", "NORMAL"

async def run():
    df = pd.read_csv(PHASE3_CSV)
    print(f"📄 Loaded {len(df)} rows from phase3")

    results = []

    async with async_playwright() as p:
        for idx, row in df.iterrows():
            case_number = safe_str(row.get("Case Number"))
            address = safe_str(row.get("Address"))

            if not case_number:
                print(f"⚠ Skipped empty case at row {idx}")
                continue

            user_agent = random.choice(USER_AGENTS)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()

            print(f"[{idx+1}] Checking case {case_number} with UA: {user_agent}")

            try:
                status, color = await check_case(page, case_number)
            except Exception as e:
                print(f"❌ Error {case_number}: {e}")
                status, color = "ERROR", "GRAY"

            record = {
                "Case Number": case_number,
                "Address": address,
                "Status": status,
                "Color": color
            }

            results.append(record)
            print(f"   ➜ SAVED: {status}")

            await context.close()
            await browser.close()

    if results:
        df_out = pd.DataFrame(results)
        df_out.to_csv(PHASE4_CSV, index=False)
        with open(PHASE4_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        print(f"✅ Saved {len(results)} records to CSV + JSON")
    else:
        print("❌ No results collected")

if __name__ == "__main__":
    asyncio.run(run())
