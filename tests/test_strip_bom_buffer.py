import pytest

from strip_bom import strip_bom_buffer


class TestStripBomBuffer:
    """Tests for strip_bom_buffer() function."""

    def test_strip_bom_from_bytes_with_bom(self):
        """Test stripping BOM from bytes that has BOM."""
        bytes_with_bom = b'\xef\xbb\xbfunicorn'
        result = strip_bom_buffer(bytes_with_bom)
        assert result == b'unicorn'
        assert len(result) == len(bytes_with_bom) - 3

    def test_strip_bom_from_bytes_without_bom(self):
        """Test bytes without BOM remains unchanged."""
        bytes_no_bom = b'unicorn'
        result = strip_bom_buffer(bytes_no_bom)
        assert result == bytes_no_bom

    def test_strip_bom_from_empty_bytes(self):
        """Test empty bytes handling."""
        result = strip_bom_buffer(b'')
        assert result == b''

    def test_strip_bom_from_bytes_with_only_bom(self):
        """Test bytes containing only BOM."""
        result = strip_bom_buffer(b'\xef\xbb\xbf')
        assert result == b''

    def test_strip_bom_from_bytearray(self):
        """Test that bytearray input is handled correctly."""
        bytearray_with_bom = bytearray(b'\xef\xbb\xbfunicorn')
        result = strip_bom_buffer(bytearray_with_bom)
        assert result == b'unicorn'
        assert isinstance(result, bytes)

    def test_strip_bom_does_not_strip_invalid_utf8(self):
        """Test that BOM is not stripped if bytes are invalid UTF-8."""
        # BOM followed by invalid UTF-8 sequence
        invalid_utf8 = b'\xef\xbb\xbf\xff\xfe'
        result = strip_bom_buffer(invalid_utf8)
        assert result == invalid_utf8  # Should remain unchanged

    def test_strip_bom_raises_type_error_for_non_bytes(self):
        """Test that non-bytes input raises TypeError."""
        with pytest.raises(TypeError, match='Expected bytes or bytearray'):
            strip_bom_buffer('string')
        
        with pytest.raises(TypeError, match='Expected bytes or bytearray'):
            strip_bom_buffer(123)
        
        with pytest.raises(TypeError, match='Expected bytes or bytearray'):
            strip_bom_buffer(None)

    def test_strip_bom_with_bom_like_prefix_but_invalid_utf8(self):
        """Test that BOM-like prefix is not stripped if not valid UTF-8."""
        # Has BOM bytes but invalid UTF-8
        invalid = b'\xef\xbb\xbf\x80\x81\x82'
        result = strip_bom_buffer(invalid)
        assert result == invalid
