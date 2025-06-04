import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True,
                                          args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        )
        page = await context.new_page()

        try:
            while True:
                api_response = None

                # Define listener inside the loop to capture current API response
                async def handle_response(response):
                    nonlocal api_response
                    if '/bapi/apex/v1/public/apex/cms/article/list/query' in response.url:
                        try:
                            api_response = await response.json()
                        except Exception as e:
                            print("Failed to parse JSON:", e)

                page.on("response", handle_response)

                # Reload or navigate to the page to trigger API calls again
                await page.goto('https://www.binance.com/en/support/announcement/list/48', wait_until='networkidle')

                # Wait up to 5 seconds for the API response to be captured
                for _ in range(50):  # 50*0.1 = 5 seconds max
                    if api_response is not None:
                        break
                    await asyncio.sleep(0.1)

                # Remove listener after response captured or timeout
                page.remove_listener("response", handle_response)

                if api_response:
                    print(json.dumps(api_response, indent=2))
                else:
                    print("API response not found or failed to parse.")

                # Wait 0.2 seconds before next iteration
                await asyncio.sleep(0.2)

        except KeyboardInterrupt:
            print("Stopped by user")

        await browser.close()

asyncio.run(main())
