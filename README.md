# Strip BOM

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ysskrishna/strip-bom/blob/main/LICENSE)
![Tests](https://github.com/ysskrishna/strip-bom/actions/workflows/test.yml/badge.svg)

Strip UTF-8 byte order mark (BOM) from strings, bytes, streams, and files. Inspired by the popular [strip-bom](https://github.com/sindresorhus/strip-bom) npm package.

## Features

- Strip BOM from strings, bytes, bytearrays, streams, and files
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

## Credits

This package is inspired by the [strip-bom](https://github.com/sindresorhus/strip-bom) ([npm](https://www.npmjs.com/package/strip-bom)) npm package by [Sindre Sorhus](https://github.com/sindresorhus).

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
