import signal
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BrowserService

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--ignore-certificates-errors")

# chrome_service = BrowserService(executable_path="/usr/local/bin/chromedriver")
chrome_service = BrowserService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())


required_scripts = [
    "http://127.0.0.1:8080/dpd/res/family_compound_json.js",
    "http://127.0.0.1:8080/dpd/res/family_idiom_json.js",
    "http://127.0.0.1:8080/dpd/res/family_root_json.js",
    "http://127.0.0.1:8080/dpd/res/family_set_json.js",
    "http://127.0.0.1:8080/dpd/res/family_word_json.js",
    "http://127.0.0.1:8080/dpd/res/family_compound_template.js",
    "http://127.0.0.1:8080/dpd/res/family_idiom_template.js",
    "http://127.0.0.1:8080/dpd/res/family_root_template.js",
    "http://127.0.0.1:8080/dpd/res/family_set_template.js",
    "http://127.0.0.1:8080/dpd/res/family_word_template.js",
    "http://127.0.0.1:8080/dpd/res/feedback_template.js",
    "http://127.0.0.1:8080/dpd/res/main.js",
]

def create_driver():
    print("Creating driver")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get("data:text/html,charset=utf-8,")

    for script in required_scripts:
        driver.execute_script(
            f"""
            if (!document.querySelector('script[src="{script}"]')) {{
                var scriptElement = document.createElement('script');
                scriptElement.src = '{script}';
                scriptElement.defer = true;
                document.head.appendChild(scriptElement);
            }}
        """
        )

    driver.execute_script(
        """var js_already_loaded = true; var progName = "tipitakapali.org";"""
    )

    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return typeof loadData === 'function';")
    )

    return driver


def fill_dpd_str(driver, html_string):
    driver.execute_script("document.body.innerHTML = arguments[0];", html_string)

    soup = BeautifulSoup(html_string, "lxml")
    meta_tags = soup.find_all("meta", attrs={"data_key": True})

    for meta_tag in meta_tags:
        data_key = meta_tag["data_key"]
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and data_key in script.string:
                modified_script = script.string.replace(
                    f"var {data_key}", f"window.{data_key}"
                )
                script.string.replace_with(modified_script)
                driver.execute_script(
                    """
                var scriptElement = document.createElement('script');
                scriptElement.text = arguments[0];
                document.head.appendChild(scriptElement);
                return scriptElement;
                """,
                    script.string,
                )
            else:
                driver.execute_script(
                    """
                var scriptElement = document.createElement('script');
                scriptElement.text = arguments[0];
                document.head.appendChild(scriptElement);
                return scriptElement;
                """,
                    script.string,
                )

    del soup

    driver.execute_script(
        """try {loadData()} catch (error) {console.error("An error occurred:", error);}"""
    )

    all_html = driver.page_source
    minified_html = " ".join(all_html.split())

    parts = minified_html.rsplit("</script><div", 1)

    if len(parts) == 2:
        body_html = "<div" + parts[1]
        body_html = body_html.replace("</body></html>", "")
    else:
        body_html = minified_html
        print(f"--------------Unexpected number of parts: {len(parts)}")

    body_html = body_html.strip()

    return body_html.strip()


def process_html_files(html_files, batch_size=100):
    driver = create_driver()
    results = []

    for idx, html_string in enumerate(html_files):
        body_html = fill_dpd_str(driver, html_string)
        results.append(body_html)

        if (idx + 1) % batch_size == 0:
            driver.quit()
            driver = create_driver()

    driver.quit()
    return results

def quit_driver(driver):
    try:
        driver.quit()
    except Exception as e:
        print(f"Error while quitting driver: {e}")
        try:
            # Try to kill the process forcefully
            pid = driver.service.process.pid
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)  # Give it some time to terminate
            if os.kill(pid, 0):  # Check if process still exists
                os.kill(pid, signal.SIGKILL)  # Force kill if still running
        except Exception as kill_error:
            print(f"Error while forcefully terminating driver: {kill_error}")
        finally:
            print("Attempting to create a new driver...")


if __name__ == "__main__":
    x = create_driver()
    print(x)
    quit_driver(x)
    print("Done")
