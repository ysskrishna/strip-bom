"""
Strip UTF-8 byte order mark (BOM) from strings, bytes, and streams.

This package provides functions equivalent to the Node.js packages:
- strip-bom: Strip BOM from strings
- strip-bom-buf: Strip BOM from byte arrays (only if valid UTF-8)
- strip-bom-stream: Strip BOM from streams/file-like objects
"""

from strip_bom.core import (
    strip_bom,
    strip_bom_buffer,
    strip_bom_stream,
    strip_bom_file,
)

__all__ = [
    'strip_bom',
    'strip_bom_buffer',
    'strip_bom_stream',
    'strip_bom_file',
]
