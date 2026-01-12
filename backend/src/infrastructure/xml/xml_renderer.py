from dicttoxml import dicttoxml
from fastapi import Response
from typing import Any

class XMLResponse(Response):
    media_type = "application/xml"

    def render(self, content: Any) -> bytes:
        if content is None:
            return b""
        
        # Converts Dict -> XML
        xml_bytes = dicttoxml(
            content, 
            custom_root='response', 
            attr_type=False,
            item_func=lambda x: 'student' # Make list items call <student>
        )
        return xml_bytes