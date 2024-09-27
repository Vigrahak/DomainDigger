# domaindigger.py

import os
import shutil
import sys
import requests
import json
import re
import os
import sys
from selenium import webdriver
from urllib.parse import urlparse, urlunparse, urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException, NoAlertPresentException, TimeoutException
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define colors
RED = '\033[1;31m'
GREEN = '\033[1;32m'
LTCYAN = '\033[1;36m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
WHITE = '\033[1;37m'
RESET = '\033[0m'

# Define HTTP status code ranges
HTTP_STATUS_CODE_SUCCESS = 200
HTTP_STATUS_CODE_REDIRECT = 300
HTTP_STATUS_CODE_CLIENT_ERROR = 400
HTTP_STATUS_CODE_SERVER_ERROR = 500

# Define hardcoded extensions
IGNORED_EXTENSIONS = ['txt', 'pdf', 'doc',
    'docx', 'xls', 'xlsx', 'ppt', 'pptx']


def print_banner():
    print(f"{BLUE}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{BLUE}█                    » DomainDigger «                     █")
    print(f"{BLUE}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")
    print(f"{LTCYAN}                                              - By Vigrahak{RESET}")
    print(f"{RED}Have a beer :  {LTCYAN}https://www.paypal.com/paypalme/SourabhS1828")
    print("")
    
def print_help():    
    print(f"{WHITE}Usage:{RESET} {BLUE}python3 domain_digger.py{RESET}")
    print(f"{WHITE}Contact:{RESET} {LTCYAN}[vigrahak1828@gmail.com]{RESET}")
    print("")


def validate_and_check_url(url):
    protocol_pattern = r"^https?://"

    # Add protocol to URL if it's not present
    if not re.match(protocol_pattern, url):
        url = f"http://{url}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers, timeout=5, stream=True, allow_redirects=True, verify=False)
        print(f"{WHITE}Redirected to:{RESET} {YELLOW} {response.url}{RESET}")
        print(f"{GREEN}URL is reachable.{RESET}")
        return True
    except requests.RequestException:
        print(f"{RED}URL is not reachable.{RESET}")
        return False


def get_status_code(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=5, stream=True, allow_redirects=True, verify=False)
        return response.status_code
    except requests.RequestException:
        return None


def create_result_folder():
    if not os.path.exists("Results"):
        os.makedirs("Results")


def create_option_folder(option_name, url):
    folder_name = f"Results/{option_name}/{urlparse(url).netloc.replace('www.', '')}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


def print_result(code, url, folder_name):
    if code is None:
        color = RED
        code = "Unknown"
        filename = "unknown.txt"
    else:
        color = GREEN if 200 <= code < 300 else YELLOW if 300 <= code < 400 else RED if 400 <= code < 500 else BLUE
        filename = f"{code}.txt"
    print(f"  {BLUE}Status: {color}{code}{RESET}\t : {url}")
    with open(os.path.join(folder_name, filename), "a") as f:
        f.write(f"{code}\t{url}\n")


def archive_url(url):
    print(f"{LTCYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{LTCYAN}█                     » Archive URL «                     █")
    print(f"{LTCYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")

    folder_name = create_option_folder("Archive_URL", url)

    for line in requests.get(f"https://web.archive.org/cdx/search/cdx?url={url}/*&output=txt&collapse=urlkey&fl=original&page=/").text.splitlines():
        url_to_check = f"http://web.archive.org/web/{line}"
        code = get_status_code(url_to_check)
        print_result(code, line, folder_name)


def parameter_url(url):
    print(f"{LTCYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{LTCYAN}█                    » Parameter URL «                    █")
    print(f"{LTCYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")

    folder_name = create_option_folder("Parameter_URL", url)

    url = f"https://web.archive.org/cdx/search/cdx?url={url}/*&output=txt&collapse=urlkey&fl=original&page=/"

    for line in requests.get(url).text.splitlines():
        if "?" not in line and "=" not in line:
            continue
        for ext in IGNORED_EXTENSIONS:
            if line.endswith(f".{ext}"):
                continue
        url_to_check = f"http://web.archive.org/web/{line}"
        code = get_status_code(url_to_check)
        print_result(code, line, folder_name)


def crawl_website(url):
    print(f"{LTCYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{LTCYAN}█                    » Crawl Website «                    █")
    print(f"{LTCYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")

    folder_name = create_option_folder("Crawl_Website", url)

    crawled_urls = set()

    options = webdriver.FirefoxOptions()
    options.headless = False  # Run the browser in non-headless mode

    try:
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(options=options, service=service)
    except WebDriverException as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"{WHITE} Opening Firefox...{RESET}")

    driver.get(url)

    while True:
        print(f"{YELLOW} Firefox opened. Do you want to login or register in the website? (y/n) {RESET}")
        choice = input().lower()
        if choice == 'y' or choice == 'n':
            break
        else:
            print(f"{RED} Invalid choice. Please enter 'y' or 'n'. {RESET}")

    cookies = None
    if choice == 'y':
        print(f"{YELLOW} Please login or register. Type 'go' when you're done. {RESET}")
        input()
        cookies = driver.get_cookies()
        for cookie in cookies:
            print(f"{GREEN}Cookies captured:{RESET} {WHITE}{cookie['name']} = {cookie['value']}{RESET}")
    else:
        print(f"{YELLOW} Proceeding without login or registration... {RESET}")

    # Crawl the website
    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")

        new_urls = []
        for link in soup.find_all("a", href=True):
            href = link["href"]

            if href.startswith("tel:") or href.startswith("mailto:") or href.startswith("javascript:"):
                continue

            if href.startswith("http://") or href.startswith("https://"):
                crawled_url = href
            else:
                crawled_url = urljoin(url, href)

            if crawled_url not in crawled_urls and urlparse(crawled_url).netloc == urlparse(url).netloc:
                new_urls.append(crawled_url)

        if not new_urls:
            break

        for new_url in new_urls:
            crawled_urls.add(new_url)
            with open(os.path.join(folder_name, f"{urlparse(url).netloc}_crawled_urls.txt"), "a") as f:
                f.write(new_url + "\n")

            code = get_status_code(new_url)
            print_result(code, new_url, folder_name)

            try:
                driver.get(new_url)
            except TimeoutException:
                print(f"Error: Failed to crawl {new_url}", file=sys.stderr)

    # Close the browser
    driver.quit()
    print(f"{GREEN} Browser closed.{RESET}")

    crawled_urls_file = os.path.join(folder_name, urlparse(url).netloc + '_crawled_urls.txt')
    print(f"{GREEN} CRAWLED URLs : {RESET}{LTCYAN}{crawled_urls_file}{RESET}")
    print(f"{GREEN} Total URLs crawled: {len(crawled_urls)}{RESET}")
    
    
def subdomains_enum(url):
    print(f"{LTCYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{LTCYAN}█                   » SubDomains Enum «                   █")
    print(f"{LTCYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")

    url = url.replace("www.", "")

    folder_name = create_option_folder("SubDomains_Enum", url)
    domain_folder = os.path.join(folder_name, url)
    os.makedirs(domain_folder, exist_ok=True)

    response = requests.get(f"https://crt.sh?q=%.{url}&output=json")

    if response.status_code != 200:
        print(f"Failed to retrieve results for url {url}. Status code: {response.status_code}")
        return

    results = [item["common_name"] for item in response.json()]

    for result in results:
        code = get_status_code(f"http://{result}")
        print_result(code, result, domain_folder)

    with open(os.path.join(domain_folder, f"{url}.txt"), "w") as f:
        for result in results:
            f.write(f"{result}\n")

    print(f"{GREEN} Total URLs retrieved: {len(results)}{RESET}")
    print(f"{GREEN}[+] Output saved in {os.path.join(domain_folder, url)}.txt{RESET}")

def main():
    create_result_folder()
    try:
        if len(sys.argv) == 1:
            print_banner()
            while True:
                print(f"{GREEN}Choose an option:{RESET}")
                print(f"{RED}1. {RESET}{WHITE}Archive URL{RESET}")
                print(f"{RED}2. {RESET}{WHITE}Parameter URL{RESET}")
                print(f"{RED}3. {RESET}{WHITE}Crawl Website{RESET}")
                print(f"{RED}4. {RESET}{WHITE}SubDomains Enum{RESET}")
                print(f"{RED}5. {RESET}{WHITE}Print Help{RESET}")
                print(f"{RED}6. {RESET}{WHITE}Quit{RESET}")
                choice = input(f"{GREEN}Enter your choice{RESET}: ")

                if choice == "1":
                    while True:
                        url = input(f"{GREEN}Enter the URL (e.g. https://example.com/abc){RESET}: ")
                        if not url.startswith("http://") and not url.startswith("https://"):
                            print(f"{RED}Error: Please provide the full URL with protocol (http/https).{RESET}")
                            continue
                        if validate_and_check_url(url):
                            archive_url(url)
                            break
                        else:
                            print("Invalid URL. Please try again.")
                elif choice == "2":
                    while True:
                        url = input(f"{GREEN}Enter the URL (e.g. https://example.com/abc){RESET}: ")
                        if not url.startswith("http://") and not url.startswith("https://"):
                            print(f"{RED}Error: Please provide the full URL with protocol (http/https).{RESET}")
                            continue
                        if validate_and_check_url(url):
                            parameter_url(url)
                            break
                        else:
                            print("Invalid URL. Please try again.")
                elif choice == "3":
                    while True:
                        url = input(f"{GREEN}Enter the URL (e.g. https://example.com){RESET}: ")
                        if not url.startswith("http://") and not url.startswith("https://"):
                            print(f"{RED}Error: Please provide the full URL with protocol (http/https).{RESET}")
                            continue
                        parsed_url = urlparse(url)
                        if parsed_url.fragment:
                            url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, ''))
                        if validate_and_check_url(url):
                            crawl_website(url)
                            break
                        else:
                            print("Invalid URL. Please try again.")
                elif choice == "4":
                    while True:
                        url = input(f"{GREEN}Enter the domain (e.g. example.com){RESET}: ")
                        if url.startswith("http://") or url.startswith("https://"):
                            print(f"{RED}Error: Please provide the domain only (without http/https protocol).{RESET}")
                            continue
                        if validate_and_check_url(f"https://{url}"):
                            subdomains_enum(url)
                            break
                        else:
                            print("Invalid domain. Please try again.")
                elif choice == "5":
                    print_help()
                elif choice == "6":
                    sys.exit(0)
                else:
                    print("Invalid choice. Please choose a valid option.")
        else:
            url = sys.argv[1]
            if validate_and_check_url(url):
                archive_url(url)
    except KeyboardInterrupt:
        print("\nForce close detected. Exiting...")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
