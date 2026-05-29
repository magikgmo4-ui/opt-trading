from ..parser.message_schema import RawMessage, InboundMessage
from .type_detector import detect_type
from .metadata_extractor import extract_metadata


class MessageNormalizer:

    @staticmethod
    def normalize(raw: RawMessage) -> InboundMessage:
        msg_type = detect_type(raw.raw_text, raw.sender)
        metadata = extract_metadata(raw.raw_text)
        inbound = InboundMessage.from_raw(
            raw,
            normalized_type=msg_type,
        )
        inbound.metadata = metadata
        return inbound


normalize_message = MessageNormalizer.normalize
