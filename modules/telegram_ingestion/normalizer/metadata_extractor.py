import re


class MetadataExtractor:

    @staticmethod
    def extract(text: str) -> dict:
        mentions = re.findall(r"@\w+", text) if text else []
        hashtags = re.findall(r"#\w+", text) if text else []
        links = re.findall(r"https?://\S+", text) if text else []
        return {
            "mentions": mentions,
            "hashtags": hashtags,
            "links": links,
        }


extract_metadata = MetadataExtractor.extract
