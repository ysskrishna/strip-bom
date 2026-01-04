"""Tests for strip_bom package."""
import io
import pytest
import tempfile
from pathlib import Path

from strip_bom import (
    strip_bom,
    strip_bom_buffer,
    strip_bom_stream,
    strip_bom_file,
)


class TestStripBom:
    """Tests for strip_bom() function."""

    def test_strip_bom_from_string_with_bom(self):
        """Test stripping BOM from string that has BOM."""
        text_with_bom = '\ufeffunicorn'
        result = strip_bom(text_with_bom)
        assert result == 'unicorn'
        assert result != text_with_bom

    def test_strip_bom_from_string_without_bom(self):
        """Test string without BOM remains unchanged."""
        text_no_bom = 'unicorn'
        result = strip_bom(text_no_bom)
        assert result == 'unicorn'
        assert result is text_no_bom  # Should return same object

    def test_strip_bom_from_empty_string(self):
        """Test empty string handling."""
        result = strip_bom('')
        assert result == ''

    def test_strip_bom_from_string_with_only_bom(self):
        """Test string containing only BOM."""
        result = strip_bom('\ufeff')
        assert result == ''

    def test_strip_bom_raises_type_error_for_non_string(self):
        """Test that non-string input raises TypeError."""
        with pytest.raises(TypeError, match='Expected a string'):
            strip_bom(b'bytes')
        
        with pytest.raises(TypeError, match='Expected a string'):
            strip_bom(123)
        
        with pytest.raises(TypeError, match='Expected a string'):
            strip_bom(None)


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


class TestStripBomStream:
    """Tests for strip_bom_stream() function."""

    def test_strip_bom_from_stream_with_bom(self):
        """Test stripping BOM from BytesIO stream with BOM."""
        stream = io.BytesIO(b'\xef\xbb\xbfunicorn')
        chunks = list(strip_bom_stream(stream))
        result = b''.join(chunks)
        assert result == b'unicorn'

    def test_strip_bom_from_stream_without_bom(self):
        """Test stream without BOM remains unchanged."""
        stream = io.BytesIO(b'unicorn')
        chunks = list(strip_bom_stream(stream))
        result = b''.join(chunks)
        assert result == b'unicorn'

    def test_strip_bom_from_empty_stream(self):
        """Test empty stream handling."""
        stream = io.BytesIO(b'')
        chunks = list(strip_bom_stream(stream))
        assert chunks == []

    def test_strip_bom_from_stream_with_only_bom(self):
        """Test stream containing only BOM."""
        stream = io.BytesIO(b'\xef\xbb\xbf')
        chunks = list(strip_bom_stream(stream))
        result = b''.join(chunks)
        assert result == b''

    def test_strip_bom_from_large_stream(self):
        """Test stream with large content."""
        content = b'\xef\xbb\xbf' + b'x' * 10000
        stream = io.BytesIO(content)
        chunks = list(strip_bom_stream(stream))
        result = b''.join(chunks)
        assert result == b'x' * 10000
        assert len(result) == 10000

    def test_strip_bom_stream_with_custom_chunk_size(self):
        """Test stream with custom chunk size."""
        content = b'\xef\xbb\xbf' + b'x' * 20000
        stream = io.BytesIO(content)
        chunks = list(strip_bom_stream(stream, chunk_size=1024))
        result = b''.join(chunks)
        assert result == b'x' * 20000

    def test_strip_bom_raises_type_error_for_non_file_like(self):
        """Test that non-file-like input raises TypeError."""
        with pytest.raises(TypeError, match='Expected a file-like object'):
            strip_bom_stream('not a stream')
        
        with pytest.raises(TypeError, match='Expected a file-like object'):
            strip_bom_stream(123)
        
        with pytest.raises(TypeError, match='Expected a file-like object'):
            strip_bom_stream(None)


class TestStripBomFile:
    """Tests for strip_bom_file() function."""

    def test_strip_bom_file_text_mode_with_bom(self):
        """Test reading file in text mode with BOM."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('\ufeffunicorn')
            temp_path = f.name
        
        try:
            result = strip_bom_file(temp_path, 'r')
            assert result == 'unicorn'
        finally:
            Path(temp_path).unlink()

    def test_strip_bom_file_text_mode_without_bom(self):
        """Test reading file in text mode without BOM."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('unicorn')
            temp_path = f.name
        
        try:
            result = strip_bom_file(temp_path, 'r')
            assert result == 'unicorn'
        finally:
            Path(temp_path).unlink()

    def test_strip_bom_file_binary_mode_with_bom(self):
        """Test reading file in binary mode with BOM."""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b'\xef\xbb\xbfunicorn')
            temp_path = f.name
        
        try:
            result = strip_bom_file(temp_path, 'rb')
            assert result == b'unicorn'
        finally:
            Path(temp_path).unlink()

    def test_strip_bom_file_binary_mode_without_bom(self):
        """Test reading file in binary mode without BOM."""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b'unicorn')
            temp_path = f.name
        
        try:
            result = strip_bom_file(temp_path, 'rb')
            assert result == b'unicorn'
        finally:
            Path(temp_path).unlink()

    def test_strip_bom_file_with_rt_mode(self):
        """Test reading file with 'rt' mode (same as 'r')."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('\ufeffunicorn')
            temp_path = f.name
        
        try:
            result = strip_bom_file(temp_path, 'rt')
            assert result == 'unicorn'
        finally:
            Path(temp_path).unlink()

    def test_strip_bom_file_raises_value_error_for_invalid_mode(self):
        """Test that invalid mode raises ValueError."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write('test')
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Mode must be 'r', 'rt', or 'rb'"):
                strip_bom_file(temp_path, 'w')
            
            with pytest.raises(ValueError, match="Mode must be 'r', 'rt', or 'rb'"):
                strip_bom_file(temp_path, 'x')
        finally:
            Path(temp_path).unlink()

    def test_strip_bom_file_with_empty_file(self):
        """Test reading empty file."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            temp_path = f.name
        
        try:
            result = strip_bom_file(temp_path, 'r')
            assert result == ''
        finally:
            Path(temp_path).unlink()


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_strip_bom_with_unicode_characters(self):
        """Test stripping BOM from string with Unicode characters."""
        text_with_bom = '\ufeffHello 世界 🌍'
        result = strip_bom(text_with_bom)
        assert result == 'Hello 世界 🌍'

    def test_strip_bom_buffer_with_unicode_bytes(self):
        """Test stripping BOM from bytes containing Unicode."""
        unicode_text = 'Hello 世界 🌍'
        bytes_with_bom = b'\xef\xbb\xbf' + unicode_text.encode('utf-8')
        result = strip_bom_buffer(bytes_with_bom)
        assert result.decode('utf-8') == unicode_text

    def test_strip_bom_buffer_with_partial_bom(self):
        """Test bytes with partial BOM sequence."""
        # Only first byte of BOM
        partial_bom = b'\xefunicorn'
        result = strip_bom_buffer(partial_bom)
        assert result == partial_bom

        # Only first two bytes of BOM
        partial_bom2 = b'\xef\xbbunicorn'
        result2 = strip_bom_buffer(partial_bom2)
        assert result2 == partial_bom2

    def test_strip_bom_stream_multiple_chunks(self):
        """Test stream that requires multiple reads."""
        content = b'\xef\xbb\xbf' + b'x' * 20000
        stream = io.BytesIO(content)
        chunks = list(strip_bom_stream(stream, chunk_size=1000))
        result = b''.join(chunks)
        assert result == b'x' * 20000
        assert len(chunks) > 1  # Should have multiple chunks

    def test_strip_bom_buffer_with_large_buffer(self):
        """Test stripping BOM from large buffer."""
        large_content = b'x' * 1000000
        bytes_with_bom = b'\xef\xbb\xbf' + large_content
        result = strip_bom_buffer(bytes_with_bom)
        assert result == large_content
        assert len(result) == 1000000

    def test_strip_bom_stream_with_very_large_stream(self):
        """Test stream with very large content."""
        large_content = b'\xef\xbb\xbf' + b'y' * 5000000
        stream = io.BytesIO(large_content)
        chunks = list(strip_bom_stream(stream, chunk_size=8192))
        result = b''.join(chunks)
        assert result == b'y' * 5000000
        assert len(result) == 5000000

    def test_strip_bom_with_various_unicode_sequences(self):
        """Test stripping BOM with various Unicode sequences."""
        test_cases = [
            '\ufeff',  # Just BOM
            '\ufeffa',  # BOM + ASCII
            '\ufeff\u00e9',  # BOM + Latin-1
            '\ufeff\u4e2d',  # BOM + CJK
            '\ufeff\U0001f600',  # BOM + Emoji
            '\ufeff\u200b',  # BOM + Zero-width space
        ]
        
        for text_with_bom in test_cases:
            result = strip_bom(text_with_bom)
            assert result == text_with_bom[1:] if text_with_bom.startswith('\ufeff') else text_with_bom

    def test_strip_bom_buffer_with_various_unicode_sequences(self):
        """Test stripping BOM from bytes with various Unicode sequences."""
        test_cases = [
            ('Hello', b'Hello'),
            ('Hello 世界', 'Hello 世界'.encode('utf-8')),
            ('Hello 🌍', 'Hello 🌍'.encode('utf-8')),
            ('\u00e9\u00e8\u00e0', '\u00e9\u00e8\u00e0'.encode('utf-8')),
        ]
        
        for text, expected_bytes in test_cases:
            bytes_with_bom = b'\xef\xbb\xbf' + expected_bytes
            result = strip_bom_buffer(bytes_with_bom)
            assert result == expected_bytes
            assert result.decode('utf-8') == text

    def test_strip_bom_stream_with_small_chunk_size(self):
        """Test stream with very small chunk size."""
        content = b'\xef\xbb\xbf' + b'x' * 1000
        stream = io.BytesIO(content)
        chunks = list(strip_bom_stream(stream, chunk_size=10))
        result = b''.join(chunks)
        assert result == b'x' * 1000
        assert len(chunks) > 1  # Should have multiple chunks

    def test_strip_bom_stream_with_large_chunk_size(self):
        """Test stream with large chunk size."""
        content = b'\xef\xbb\xbf' + b'x' * 5000
        stream = io.BytesIO(content)
        chunks = list(strip_bom_stream(stream, chunk_size=100000))
        result = b''.join(chunks)
        assert result == b'x' * 5000

    def test_strip_bom_file_with_nonexistent_file(self):
        """Test that FileNotFoundError is raised for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            strip_bom_file('/nonexistent/file/path.txt', 'r')

    def test_strip_bom_buffer_with_bom_in_middle(self):
        """Test that BOM in the middle is not stripped (only at start)."""
        # BOM-like sequence in the middle should not be stripped
        bytes_with_bom_middle = b'hello\xef\xbb\xbfworld'
        result = strip_bom_buffer(bytes_with_bom_middle)
        assert result == bytes_with_bom_middle  # Should remain unchanged

    def test_strip_bom_with_bom_followed_by_newline(self):
        """Test BOM followed by newline characters."""
        text_with_bom = '\ufeff\n\r\nHello'
        result = strip_bom(text_with_bom)
        assert result == '\n\r\nHello'

    def test_strip_bom_buffer_with_bom_followed_by_newline(self):
        """Test BOM followed by newline bytes."""
        bytes_with_bom = b'\xef\xbb\xbf\n\r\nHello'
        result = strip_bom_buffer(bytes_with_bom)
        assert result == b'\n\r\nHello'

    def test_strip_bom_stream_preserves_stream_position_behavior(self):
        """Test that stream position is handled correctly."""
        content = b'\xef\xbb\xbf' + b'x' * 100
        stream = io.BytesIO(content)
        
        # Consume the stream
        list(strip_bom_stream(stream))
        
        # Stream should be at end
        assert stream.tell() == len(content)

    def test_strip_bom_buffer_with_empty_after_bom(self):
        """Test bytes with only BOM."""
        result = strip_bom_buffer(b'\xef\xbb\xbf')
        assert result == b''

    def test_strip_bom_stream_with_single_byte_after_bom(self):
        """Test stream with single byte after BOM."""
        stream = io.BytesIO(b'\xef\xbb\xbfx')
        chunks = list(strip_bom_stream(stream))
        result = b''.join(chunks)
        assert result == b'x'

    def test_strip_bom_buffer_performance_with_repeated_calls(self):
        """Test that repeated calls work correctly (performance-related)."""
        test_bytes = b'\xef\xbb\xbf' + b'x' * 1000
        
        # Call multiple times
        for _ in range(100):
            result = strip_bom_buffer(test_bytes)
            assert result == b'x' * 1000

    def test_strip_bom_with_surrogate_pairs(self):
        """Test handling of surrogate pairs in Unicode."""
        # Surrogate pairs are not valid in UTF-8, but test edge case
        text = '\ufeffHello'
        result = strip_bom(text)
        assert result == 'Hello'
