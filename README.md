# CWE Filter for DevOps

This project provides a Python-based tool to automatically filter CWE (Common Weakness Enumeration) data by programming language, designed for integration into CI/CD pipelines.
It helps teams generate up-to-date lists of relevant software weaknesses as part of their automated build process.

## Features

- **CI/CD integration:** Outputs language-specific weakness lists during build (via GitHub Action)
- **Multi-language filtering** (e.g. Java, Python)
- **Flexible logic:** Use "or" (any language) or "and" (all languages required) for filtering.
- **Easy-to-use artifacts:** Output .txt and .csv with automatically named with language(s),mode, and timestamp
- **Configuration file support:** Default parameters for automated builds can be managed via .github/cwe_languages.txt.
- **Unit tests**

## Quick Start

### Typical CI usage (Recommended)

- The script runs automatically as part of your build pipeline, using parameters either from:
    - CI workflow inputs (manual trigger), or
    - .github/cwe_languages.txt for builds automatically on each push.

### Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run the script locally for validation:
```bash
python filter_cwe.py --languages "Python,Java"
```
### Command-line usage (for local testing)

```bash
python filter_cwe.py --languages "Python,Java" --mode or
python filter_cwe.py --languages "Python,Java" --mode and --output my_cwe.txt
python filter_cwe.py --languages "Python,Java" --csv my_cwe.csv
```
## Output
- **Text(.txt):** For direct reading or review in CI
- **CSV(.csv):** each CWE with multi-line Observed Examples
Both files are automatically named with language, mode, and timestamp

## Data File
Place the CWE CSV (e.g. 699.csv) as default in the repo root

## Configuration
- Used by automatic build on each push
- .github/cwe_languages.txt
Example:
```bash
Java,Python
and 
```
(First line: language(s), Second line: mode)

## Testing
```bash
pytest tests/
```
## Project Structure
- `.github/workflows/` - GitHub Actions workflow files
- `.github/cwe_languages.txt` - Languages and mode for automation
- `filter_cwe.py` - Main script
- `699.csv` - CWE data input
- `tests/` - Automated tests
- `filtered_cwe_java_python_and_20250602_110032` - Artefacts example