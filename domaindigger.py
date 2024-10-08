# domaindigger.py

import logging
import os
import shutil
import sys
import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, urljoin
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.edge.webdriver import WebDriver as EdgeWebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException, NoAlertPresentException, TimeoutException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from colorama import init, Fore, Style

# Color variables
RED = Style.BRIGHT + Fore.RED
GREEN = Style.BRIGHT + Fore.GREEN
CYAN = Style.BRIGHT + Fore.CYAN
YELLOW = Style.BRIGHT + Fore.YELLOW
BLUE = Style.BRIGHT + Fore.BLUE
WHITE = Style.BRIGHT + Fore.WHITE
MAGENTA = Style.BRIGHT + Fore.MAGENTA
RESET = Style.RESET_ALL

# Define hardcoded extensions
IGNORED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']

def print_banner():
    print(f"{CYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{CYAN}█                    » DomainDigger «                     █")
    print(f"{CYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")
    print(f"{CYAN}                                              - By Vigrahak{RESET}")
    print(f"{RED}Have a beer :  {CYAN}https://www.paypal.com/paypalme/SourabhS1828")
    print("")

def print_help():
    print(f"{WHITE}Usage:{RESET} {BLUE}python3 domain_digger.py{RESET}")
    print(f"{WHITE}Contact:{RESET} {CYAN}[vigrahak1828@gmail.com]{RESET}")
    print("")

def validate_and_check_url(url):
    protocol_pattern = r"^https?"
    
    # Add protocol to URL if it's not present
    if not re.match(protocol_pattern, url):
        protocol = input(f"{GREEN}Please specify the protocol (http/https) for {url}: {RESET}")
        url = f"http://{url}"
    
    try:
        response = requests.get(url, timeout=30, stream=True, allow_redirects=True, verify=False)
        print(f"{WHITE}Redirected to:{RESET} {YELLOW} {response.url}{RESET}")
        print(f"{GREEN}URL is reachable.{RESET}")
        return True
    except requests.RequestException as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {WHITE}{e}{RESET}")
        print(f"{RED}URL is not reachable.{RESET}")
        return False

def get_status_code(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  
        return response.status_code
    except requests.RequestException as e:
        return -1 

def print_result(code, url, folder_name):
    try:
        if code == -1:
            return  # Unknown status code ke liye kuch nahi print kiya hai
        else:
            color = GREEN if 200 <= code < 300 else YELLOW if 300 <= code < 400 else RED if 400 <= code < 500 else BLUE
            print(f"  {BLUE}Status: {color}{code}{RESET}\t : {url}")
            if code == 200:
                with open(os.path.join(folder_name, "200_urls.txt"), "a") as f:
                    f.write(f"{code}\t{url}\n")
            else:
                with open(os.path.join(folder_name, "all_urls.txt"), "a") as f:
                    f.write(f"{code}\t{url}\n")
    except OSError as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {e}{RESET}")

def create_result_folder ():
    if not os.path.exists("Results"):
        os.makedirs("Results")

def create_option_folder(option_name, url):
    try:
        folder_name = f"Results/{option_name}/{urlparse(url).netloc.replace('www.', '')}"
        shutil.rmtree(folder_name, ignore_errors=True)  # pehle wala folder delete kiya hai
        os.makedirs(folder_name, exist_ok=True)  # naya folder banaya hai
        return folder_name
    except OSError as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {e}{RESET}")
        return None

def archive_url(url):
    print(f"{CYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{CYAN}█                     » Archive URL «                     █")
    print(f"{CYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")

    folder_name = create_option_folder("Archive_URL", url)

    if folder_name is None:
        return

    try:
        response = requests.get(url, allow_redirects=True)
        redirected_url = response.url
        for line in requests.get(f"https://web.archive.org/cdx/search/cdx?url={redirected_url}/*&output=txt&collapse=urlkey&fl=original&page=/").text.splitlines():
            url_to_check = f"http://web.archive.org/web/{line}"
            code = get_status_code(url_to_check)
            print_result(code, line, folder_name)
    except requests.RequestException as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {e}{RESET}")

def parameter_url(url):
    print(f"{CYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{CYAN}█                    » Parameter URL «                    █")
    print(f"{CYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")

    folder_name = create_option_folder("Parameter_URL", url)

    if folder_name is None:
        return

    try:
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
    except requests.RequestException as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {e}{RESET}")

def crawl_website(url):
    print(f"{CYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{CYAN}█                    » Crawl Website «                    █")
    print(f"{CYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")

    folder_name = create_option_folder("Crawl_Website", url)

    if folder_name is None:
        return

    crawled_urls = set()

    # Auto-detect browser
    browser = None
    try:
        options = ChromeOptions()
        browser = ChromeWebDriver(service=ChromeService(ChromeDriverManager().install()), options=options)
    except WebDriverException:
        try:
            options = FirefoxOptions()
            browser = FirefoxWebDriver(service=FirefoxService(GeckoDriverManager().install()), options=options)
        except WebDriverException:
            try:
                options = EdgeOptions()
                browser = EdgeWebDriver(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            except WebDriverException:
                logging.error("Error: Unable to detect browser. Please install a supported browser.")
                sys.exit(1)

    print(f"{WHITE} Opening {browser.name}...{RESET}")

    try:
        browser.get(url)
    except TimeoutException:
        logging.error(f"Error: Failed to load URL {url}. Please check the URL and try again.")
        print(f"{RED}Error: {WHITE}Failed to load URL {url}. Please check the URL and try again.{RESET}")
        browser.quit()
        sys.exit(1)
    except WebDriverException as e:
        if "RemoteError" in str(e) or "UnknownError" in str(e):
            print(f"{RED}Error: {WHITE}Failed to connect to the website. Please check your internet connection and try again.{RESET}")
            browser.quit()
            sys.exit(1)
        else:
            print(f"{RED}Error: {WHITE}{e}{RESET}")
            browser.quit()
            sys.exit(1)

    # Get the redirected URL
    redirected_url = browser.current_url

    while True:
        print(f"{YELLOW} {browser.name} opened. Do you want to login or register in the website? (y/n) {RESET}")
        choice = input().lower()
        if choice == 'y' or choice == 'n':
            break
        else:
            print(f"{RED}Invalid choice. Please enter 'y' or 'n'.{RESET}")

    cookies = None
    if choice == 'y':
        print(f"{YELLOW} Please login or register. Type 'go' when you're done. {RESET}")
        input()
        cookies = browser.get_cookies()
        for cookie in cookies:
            print(f"{GREEN}Cookies captured:{RESET} {YELLOW}{cookie['name']} = {cookie['value']}{RESET}")
    else:
        print(f"{YELLOW} Proceeding without login or registration... {RESET}")

    # Crawl the website
    max_iterations = 100
    iteration = 0
    while iteration < max_iterations:
        soup = BeautifulSoup(browser.page_source, "html.parser")

        new_urls = []
        for link in soup.find_all("a", href=True):
            href = link["href"]

            if href.startswith("tel:") or href.startswith("mailto:") or href.startswith("javascript:"):
                continue

            if href.startswith("http://") or href.startswith("https://"):
                crawled_url = href
            else:
                crawled_url = urljoin(redirected_url, href)

            if crawled_url not in crawled_urls and urlparse(crawled_url).netloc == urlparse(redirected_url).netloc:
                new_urls.append(crawled_url)

        if not new_urls:
            break

        for new_url in new_urls:
            crawled_urls.add(new_url )
            print(f"{GREEN} Crawled URL: {RESET}{WHITE}{new_url}{RESET}")
            with open(os.path.join(folder_name, f"{urlparse(redirected_url).netloc}_crawled_urls.txt"), "a") as f:
                f.write(new_url + "\n")

            try:
                browser.get(new_url)
            except TimeoutException:
                logging.error(f"Error: Failed to crawl {new_url}")
            except WebDriverException as e:
                if "RemoteError" in str(e) or "UnknownError" in str(e):
                    print(f"{RED}Error: {WHITE}Failed to connect to the website. Please check your internet connection and try again.{RESET}")
                    browser.quit()
                    sys.exit(1)
                else:
                    print(f"{RED}Error: {WHITE}{e}{RESET}")
                    browser.quit()
                    sys.exit(1)

        iteration += 1

    # Close the browser
    browser.quit()
    print(f"{GREEN} Browser closed.{RESET}")

    crawled_urls_file = os.path.join(folder_name, urlparse(redirected_url).netloc + '_crawled_urls.txt')
    print(f"{GREEN} CRAWLED URLs : {RESET}{CYAN}{crawled_urls_file}{RESET}")
    print(f"{GREEN} Total URLs crawled: {len(crawled_urls)}{RESET}")


def subdomains_enum(url):
    print(f"{CYAN}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█")
    print(f"{CYAN}█                   » SubDomains Enum «                   █")
    print(f"{CYAN}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RESET}")
    print("")

    url = url.replace("www.", "")

    folder_name = create_option_folder("SubDomains_Enum", url)
    domain_folder = os.path.join(folder_name, url)
    try:
        os.makedirs(domain_folder, exist_ok=True)
    except OSError as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {e}{RESET}")
        return

    try:
        response = requests.get(f"https://crt.sh?q=%.{url}&output=json")
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {e}{RESET}")
        return

    try:
        results = [item["common_name"] for item in response.json()]
    except json.JSONDecodeError as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {e}{RESET}")
        return

    for result in results:
        code = get_status_code(f"http://{result}")
        print_result(code, result, domain_folder)

    try:
        with open(os.path.join(domain_folder, f"{url}.txt"), "w") as f:
            for result in results:
                f.write(f"{result}\n")
    except OSError as e:
        logging.error(f"Error: {e}")
        print(f"{RED}Error: {e}{RESET}")

    print(f"{GREEN} Total URLs retrieved: {len(results)}{RESET}")
    print(
        f"{GREEN}[+] Output saved in {os.path.join(domain_folder, url)}.txt{RESET}")


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
                        url = input(
                            f"{GREEN}Enter the URL (e.g. https://example.com/abc){RESET}: ")
                        if not url.startswith("http://") and not url.startswith("https://"):
                            print(
                                f"{RED}Error: Please provide the full URL with protocol (http/https).{RESET}")
                            continue
                        if validate_and_check_url(url):
                            archive_url(url)
                            break
                        else:
                            print(
                                f"{WHITE}Please ensure the URL is correct and your internet connection is stable.{RESET}")
                elif choice == "2":
                    while True:
                        url = input(
                            f"{GREEN}Enter the URL (e.g. https://example.com/abc){RESET}: ")
                        if not url.startswith("http://") and not url.startswith("https://"):
                            print(
                                f"{RED}Error: Please provide the full URL with protocol (http/https).{RESET}")
                            continue
                        if validate_and_check_url(url):
                            parameter_url(url)
                            break
                        else:
                            print(
                                f"{WHITE}Please ensure the URL is correct and your internet connection is stable.{RESET}")
                elif choice == "3":
                    while True:
                        url = input(
                            f"{GREEN}Enter the URL (e.g. https://example.com){RESET}: ")
                        if not url.startswith("http://") and not url.startswith("https://"):
                            print(
                                f"{RED}Error: Please provide the full URL with protocol (http/https).{RESET}")
                            continue
                        parsed_url = urlparse(url)
                        if parsed_url.fragment:
                            url = urlunparse(
                                (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, ''))
                        if validate_and_check_url(url):
                            crawl_website(url)
                            break
                        else:
                            print(
                                f"{WHITE}Please ensure the URL is correct and your internet connection is stable.{RESET}")
                elif choice == "4":
                    while True:
                        url = input(
                            f"{GREEN}Enter the domain (e.g. example.com){RESET}: ")
                        if url.startswith("http://") or url.startswith("https://"):
                            print(
                                f"{RED}Error: Please provide the domain only (without http/https protocol).{RESET}")
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
