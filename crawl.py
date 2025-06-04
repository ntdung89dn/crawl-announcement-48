import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, 
                                          args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = await browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36')
        page = await context.new_page()

        api_response = None

        # Listen to all responses and capture the target API response
        async def handle_response(response):
            nonlocal api_response
            if '/bapi/apex/v1/public/apex/cms/article/list/query' in response.url:
                try:
                    api_response = await response.json()
                except Exception as e:
                    print('Failed to parse JSON:', e)

        page.on("response", handle_response)

        await page.goto('https://www.binance.com/en/support/announcement/list/48', wait_until='networkidle')
        
        # Wait a little to ensure all API calls complete
        await asyncio.sleep(3)

        if api_response:
            import json
            print(json.dumps(api_response, indent=2))
        else:
            print("API response not found")

        await browser.close()

asyncio.run(main())
