import re


class TypeDetector:

    @staticmethod
    def detect(raw_text: str, sender: str | None = None) -> str:
        if sender and "media" in sender.lower():
            return "image"
        if sender and "poll" in sender.lower():
            return "poll"
        if raw_text and re.search(r"https?://\S+", raw_text):
            return "link"
        if raw_text and raw_text.strip().startswith("Poll"):
            return "poll"
        return "text"


detect_type = TypeDetector.detect
