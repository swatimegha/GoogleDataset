import unicodedata

class Formatter:

    @staticmethod
    def to_html_string(response: str) -> str:
        return f'<pre><code style="font-size: 20">{response}</code></pre>'

    @staticmethod
    def to_string(value: str) -> str:
        value = str(unicodedata.normalize('NFKD', value).encode('ascii', 'ignore'), 'utf-8')
        return value.strip()