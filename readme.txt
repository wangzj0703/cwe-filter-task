# CWE Filter Script for DevOps

This project provides a Python command-line tool for filtering CWE (Common Weakness Enumeration) data by programming language.  
The script is purpose-built for automation in DevOps and CI/CD workflows.

## Features

- Automation-friendly CLI tool—ideal for CI/CD pipelines
- Supports filtering by one or multiple programming languages
- Flexible logic: OR (any) or AND (all) mode for language matching
- Output is human-readable and CI/CD artifact-ready
- Simple integration with GitHub Actions, GitLab CI, Jenkins, etc.

## Requirements

- Python 3.6+
- pandas

Install dependencies:

```bash
pip install -r requirements.txt

## Usage

### Filter by any language (OR mode, default)

Outputs all CWE records that are applicable to **at least one** of the specified languages.

```bash
python filter_cwe.py --languages "Python,Java"

### Filter by all languages (AND mode)

Outputs only CWE records that are applicable to all specified languages.

```bash
python filter_cwe.py --languages "Python,Java" --mode and

### Save output to file (for use as a CI/CD artefact)

```bash
python filter_cwe.py --languages "Python,Java" > filtered_cwe.txt
