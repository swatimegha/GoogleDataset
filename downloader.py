from dateutil import parser
from newspaper import Article, ArticleException
from newspaper.article import ArticleDownloadState

# from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
# from tools.logger import trace, Level, NliServiceException


class Downloader:
    """
    Download and process the webpage's content for a given url.
    The class also contains methods for text and dates processing and normalization.
    """

    # logger = trace.get_logger(__name__)

    @staticmethod
    def get_article(url: str, text="") -> Article:
        """
        Examine the url or text parameters.
        The method accepts text or webpage url for processing.
        If both are passed, the text is given priority, and the url is ignored.
        If only url is passed, then it tries to download and parse it into an Article object.
        If both parameters are null or empty, then an exception is thrown.
        :param url: string with the url
        :param text: string with the article's text. By default it equals empty string.
        :return: Article object from newspaper library
        """

        if text and text.strip():
            text = text.strip()
            article = Article("text_is_passed_so_no_url")
            article.download(input_html=text)
            article.set_text(text)
        elif url:
            url = f"http://{url}" if not str(url).startswith("http") else url
            article = Downloader.download_article(url)
        else:
            message = "Parameters are empty!"
            Downloader.logger.warn(message)
            # raise NliServiceException(Level.WARNING, __name__, message)
        return Downloader.parse_article(article)

    @staticmethod
    def parse_date(date: str) -> str:
        """
        Transform the date string into the required format
        :param date: string
        :return: formatted string
        """

        return parser.parse(date).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def parse_article(article: Article) -> Article:
        """
        Attempt parsing the article and throw an exception if something goes wrong
        :param article: Article object
        :return: Article object containing the parsed article ready for further processing
        """

        try:
            article.parse()
            # TODO: add parser
            # if article.text:
                # Downloader.logger.debug("Article is parsed by newspaper library.")
            # else:
                # message = f"Can not parse an article: URL = {article.url}"
                # Downloader.logger.error(message)
                # raise NliServiceException(Level.ERROR, __name__, message)
        except ArticleException as e:
            message = f"Cannot parse an article: URL = {article.url}. Error: {e}"
            # Downloader.logger.error(message)
            # raise NliServiceException(Level.ERROR, __name__, message)
        return article

    @staticmethod
    def download_article(url: str) -> Article:
        """
        Attempt to download the article using newspaper library.
        If it's unsuccesful, use chrome web driver to run the page and get html.
        Throw exception if something goes wrong.
        :param url: string
        :return: Article object
        """

        try:
            article = Article(url)
            article.download()
            if (article.download_state != ArticleDownloadState.SUCCESS or not article.html):
                html = Downloader.get_html_by_chrome(url)
                if html and html.strip():
                    article.download(input_html=html)
                    # Downloader.logger.debug("Article is downloaded by newspaper chrome web driver.")
                else:
                    message = f"HTML document is empty. URL = {url}"
                    # Downloader.logger.warn(message)
                    # raise NliServiceException(Level.WARNING, __name__, message)
            # else:
                # Downloader.logger.debug("Article is downloaded by newspaper library.")
            return article
        except ArticleException as e:
            message = f"Cannot download article. URL = {url}. Error: {e}"
            # Downloader.logger.error(message)
            # raise NliServiceException(Level.ERROR, __name__, message)
        return None

    @staticmethod
    def get_html_by_chrome(url: str) -> str:
        """
        Create chrome webdriver browser instance and attempt to download the webpage
        :param url: string
        :return: string containing html
        """

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        browser = Chrome(chrome_options=options)
        try:
            # browser = Chrome(chrome_options=options)
            browser.set_script_timeout(5)
            browser.get(url)
            # Check the browser's currenturl property for chrome-error message before returning success
            current_url = browser.current_url
            html = browser.page_source
            browser.quit()
            if "chrome-error" in current_url:
                message = f"Chrome web driver returned an error page. Url = {url}"
                # Downloader.logger.error(message)
                # raise NliServiceException(Level.ERROR, __name__, message)
            return html
        except WebDriverException as e:
            message = f"Chrome web driver cannot run correctly. URL = {url}. Error: {e}"
            browser.quit()
            # Downloader.logger.error(message)
            # raise NliServiceException(Level.ERROR, __name__, message)

        return None