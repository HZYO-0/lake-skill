"""WeChat CSV adapter."""

from typing import Any

from .generic_csv import GenericCSVAdapter


class WeChatCSVAdapter(GenericCSVAdapter):
    """Adapter specifically for WeChat CSV exports."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize WeChat CSV adapter."""
        super().__init__(**kwargs)
        # WeChat specific column mappings
        self.wechat_column_mappings = {
            "CreateTime": "timestamp",
            "StrContent": "text",
            "StrTalker": "sender",
            "Type": "message_type",
            "IsSender": "is_sender",
        }
