# Contributing to Xiom

Thank you for your interest in contributing! We welcome bug reports, feature requests, and pull requests.

## Code of Conduct

Please review [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How to Report Issues

### Bug Reports
1. Check if the issue already exists in [Issues](https://github.com/yourusername/Xiom/issues)
2. Use the bug report template when opening a new issue
3. Include:
   - URL tested and expected vs. actual output
   - Python version and OS
   - Full error traceback
   - Steps to reproduce

### Feature Requests
1. Use the feature request template
2. Explain the use case and desired behavior
3. Suggest any implementation approach

## How to Contribute Code

### Setup Development Environment

```bash
# 1. Fork the repo on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Xiom.git
cd Xiom

# 3. Create a branch for your feature
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/issue-description

# 4. Install dev dependencies
pip install -r requirements.txt

# 5. Make your changes
```

### Code Style

- **Python:** Follow PEP 8 (use `black` for formatting)
- **Naming:** Use descriptive names for functions/variables
- **Docstrings:** Add docstrings to all functions and classes
- **Comments:** Only comment non-obvious logic
- **Imports:** Group standard library, third-party, local imports

Example:
```python
def fingerprint_server(url: str, timeout: int = 10) -> dict:
    """
    Analyze a target URL and extract server fingerprint information.
    
    Args:
        url: Target website URL
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary containing server details
        
    Raises:
        ConnectionError: If unable to connect to target
        ValueError: If URL is invalid
    """
    pass
```

### Testing

- Write tests for new features (test coverage preferred)
- Run tests before submitting PR: `python -m pytest`
- Ensure all tests pass

### Commit Messages

Use clear, descriptive commit messages:

```
git commit -m "Add SSL certificate analysis feature"
# NOT: "fix stuff" or "updates"
```

**Format:**
```
<type>: <subject>

<body (optional)>

Fixes #<issue-number>
```

**Types:** feat, fix, docs, refactor, test, chore

### Pull Request Process

1. **Update documentation** — If you change behavior, update README or docstrings
2. **Test thoroughly** — Run all tests and test your changes manually
3. **Push to your fork:** `git push origin feature/your-feature-name`
4. **Open a PR** — Use the pull request template
5. **Respond to reviews** — Address feedback promptly
6. **Squash commits** (if requested) — `git rebase -i main`

### Before Submitting

- [ ] Code follows PEP 8 style
- [ ] All tests pass (`python -m pytest`)
- [ ] No hardcoded API keys or secrets
- [ ] Updated README if behavior changed
- [ ] Added docstrings to new functions
- [ ] Commit messages are clear and descriptive

## Development Tips

### Running Tests
```bash
python -m pytest              # Run all tests
python -m pytest tests/test_fingerprint.py  # Single test file
python -m pytest -v           # Verbose output
```

### Debugging
```bash
python xiom.py https://example.com --verbose  # Verbose mode
```

### Documentation
- Update README.md for user-facing changes
- Add docstrings to all functions/classes
- Include examples in feature documentation

## Questions?

- Open an issue with the question label
- Check existing issues/discussions first
- Read the [README](README.md) for general usage

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making Xiom better! 🚀**
