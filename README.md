# Strip BOM

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ysskrishna/strip-bom/blob/main/LICENSE)
![Tests](https://github.com/ysskrishna/strip-bom/actions/workflows/test.yml/badge.svg)

Strip UTF-8 byte order mark (BOM) from strings, bytes, and streams. Equivalent to the Node.js [strip-bom](https://github.com/sindresorhus/strip-bom), [strip-bom-buf](https://github.com/sindresorhus/strip-bom-buf), and [strip-bom-stream](https://github.com/sindresorhus/strip-bom-stream) packages.

## Features

- Strip BOM from strings, bytes, bytearrays, and streams
- Validates UTF-8 encoding before stripping BOM from buffers
- Handles large files and streams efficiently
- Zero dependencies, minimal overhead
- Type hints for better IDE support
- Graceful error handling
- Supports Unicode characters including emojis and CJK characters

## Installation

```bash
pip install strip-bom
```

Or using `uv`:

```bash
uv add strip-bom
```

## Usage

### Strip BOM from a string

```python
from strip_bom import strip_bom

text_with_bom = '\ufeffunicorn'
clean_text = strip_bom(text_with_bom)
print(clean_text)  # 'unicorn'
```

### Strip BOM from bytes

```python
from strip_bom import strip_bom_buffer

bytes_with_bom = b'\xef\xbb\xbfunicorn'
clean_bytes = strip_bom_buffer(bytes_with_bom)
print(clean_bytes)  # b'unicorn'
```

The function only strips BOM if the bytes are valid UTF-8 encoded:

```python
# Invalid UTF-8 with BOM-like prefix - BOM is NOT stripped
invalid_utf8 = b'\xef\xbb\xbf\xff\xfe'
result = strip_bom_buffer(invalid_utf8)
print(result == invalid_utf8)  # True (unchanged)
```

### Strip BOM from a stream

```python
from strip_bom import strip_bom_stream
import io

stream = io.BytesIO(b'\xef\xbb\xbfHello World')
chunks = list(strip_bom_stream(stream))
content = b''.join(chunks)
print(content)  # b'Hello World'
```

### Strip BOM from a file

```python
from strip_bom import strip_bom_file

# Read file in text mode
content = strip_bom_file('file.txt', 'r')
print(content)

# Read file in binary mode
content = strip_bom_file('file.txt', 'rb')
print(content)
```

## API Reference

### `strip_bom(string: str) -> str`

Strip UTF-8 BOM from a string.

- **Parameters:**
  - `string`: Input string that may contain a BOM
- **Returns:** String with BOM removed if present, otherwise the original string
- **Raises:** `TypeError` if input is not a string

### `strip_bom_buffer(byte_array: Union[bytes, bytearray]) -> bytes`

Strip UTF-8 BOM from bytes or bytearray. Only strips BOM if the buffer is valid UTF-8 encoded.

- **Parameters:**
  - `byte_array`: Input bytes that may contain a UTF-8 BOM (0xEF 0xBB 0xBF)
- **Returns:** Bytes with BOM removed if present and valid UTF-8, otherwise the original bytes
- **Raises:** `TypeError` if input is not bytes or bytearray

### `strip_bom_stream(file_like: BinaryIO, chunk_size: int = 8192) -> Iterator[bytes]`

Strip UTF-8 BOM from a stream/file-like object.

- **Parameters:**
  - `file_like`: File-like object opened in binary mode
  - `chunk_size`: Size of chunks to read for subsequent reads (default: 8192)
- **Yields:** Bytes chunks with BOM removed from the first chunk
- **Raises:** `TypeError` if input is not a file-like object with read() method

### `strip_bom_file(file_path: str, mode: str = 'r') -> Union[str, bytes]`

Convenience function to read a file and strip BOM.

- **Parameters:**
  - `file_path`: Path to the file
  - `mode`: File mode ('r' or 'rt' for text, 'rb' for binary)
- **Returns:** File contents with BOM removed (string if mode='r' or 'rt', bytes if mode='rb')
- **Raises:**
  - `ValueError` if mode is not 'r', 'rt', or 'rb'
  - `FileNotFoundError` if the file does not exist

## Credits

This package is inspired by the Node.js packages:
- [strip-bom](https://github.com/sindresorhus/strip-bom) by [Sindre Sorhus](https://github.com/sindresorhus)
- [strip-bom-buf](https://github.com/sindresorhus/strip-bom-buf) by [Sindre Sorhus](https://github.com/sindresorhus)
- [strip-bom-stream](https://github.com/sindresorhus/strip-bom-stream) by [Sindre Sorhus](https://github.com/sindresorhus)

## Changelog

See [CHANGELOG.md](https://github.com/ysskrishna/strip-bom/blob/main/CHANGELOG.md) for a detailed list of changes and version history.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](https://github.com/ysskrishna/strip-bom/blob/main/CONTRIBUTING.md) for details on our code of conduct, development setup, and the process for submitting pull requests.

## Support

If you find this library useful, please consider:

- ⭐ **Starring** the repository on GitHub to help others discover it.
- 💖 **Sponsoring** to support ongoing maintenance and development.

[Become a Sponsor on GitHub](https://github.com/sponsors/ysskrishna) | [Support on Patreon](https://patreon.com/ysskrishna)

## License

MIT License - see [LICENSE](https://github.com/ysskrishna/strip-bom/blob/main/LICENSE) file for details.

## Author

**Y. Siva Sai Krishna**

- GitHub: [@ysskrishna](https://github.com/ysskrishna)
- LinkedIn: [ysskrishna](https://linkedin.com/in/ysskrishna)
