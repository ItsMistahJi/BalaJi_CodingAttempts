from playwright.sync_api import sync_playwright

def main():
    #start playwright
    with sync_playwright() as playwright:
        #launch a browser
        #to see UI use headless=False and vice versa for otherwise
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        #go to Youtube
        url = "https://www.youtube.com"
        #confirm navigation
        print(f"Navigation passed")
        page.goto(url)
        #page.wait_for_timeout(8000)
        #page.wait_for_selector("ytd-video-renderer", timeout=5000)

        #search the string passed
        search_box_selector = 'input[name="search_query"]'
        search_query = "vidamuyarchi"

        #handle pop up by rejecting
        reject_button_selector = 'button:has-text("Reject all")'
        if page.locator(reject_button_selector).is_visible():
          page.click(reject_button_selector)
        else:
            print(f"button not visible")
        
        #wait for loading
            page.wait_for_selector("ytd-video-renderer", timeout=10000)

        #look for visibility
        page.wait_for_selector('input[name="search_query"]')
        if page.locator(search_box_selector).is_visible():
            print(f"Search box found")
            page.fill(search_box_selector,search_query)
            page.wait_for_selector('button[title="Search"]', timeout=3000)
            page.click('button[title="Search"]')

            #wait for loading
            page.wait_for_selector("ytd-video-renderer", timeout=10000)

            #print confirmation
            print("page loaded")
            #take screenshot
            page.screenshot(path=r"C:\Users\BRU09\OneDrive - Sky\Documents\Personal\Learning\2025_Learning\Python-mini-projects\python-mini-project\CodingAttempts\Playwright-Python_project\screenshot1_yt.png")

        else:
            #print error
            print(f"cant get to search box")

        #close the browser
        page.wait_for_timeout(5000)
        browser.close()
        #confirm page close
        print(f"Browser closed")

if __name__ == "__main__":
    main()