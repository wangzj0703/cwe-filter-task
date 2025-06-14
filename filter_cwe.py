import pandas as pd
import argparse
import sys
import re

def split_examples(examples_str):
    # split and format each Observed Examples
    if pd.isna(examples_str) or not str(examples_str).strip():
        return []
    items = [ex.strip() for ex in str(examples_str).split("::") if ex.strip()]
    pretty_examples = []
    for ex in items:
        parts = []
        pattern = r'([A-Z_]+):\s*(.*?)(?=:[A-Z_]+:|$)'
        matches = re.findall(pattern, ex)
        if matches:
            for key, val in matches:
                parts.append(f"{key.strip()}: {val.strip()}")
            pretty_examples.append(" | ".join(parts))
        else:
            pretty_examples.append(ex)
    return pretty_examples

def main():
    parser = argparse.ArgumentParser(description="Filter CWE data by programming language(s)")
    parser.add_argument('--languages', type=str, required=True,
                        help='Comma-separated language names (e.g. "Python,C#,PHP")')
    parser.add_argument('--input', type=str, default='699.csv',
                        help='Input CWE csv file (default: 699.csv)')
    parser.add_argument('--mode', type=str, default='or', choices=['or', 'and'],
                        help="Filter mode: 'or' (default) matches any language; 'and' matches only if all languages are present")
    parser.add_argument('--output', type=str, default="filtered_cwe.txt", help="Output file path")
    args = parser.parse_args()

    # Parse and trim
    language_list = [lang.strip().lower() for lang in args.languages.split(",")]

    # read CSV
    try:
        df = pd.read_csv(args.input, index_col=False)
        df.columns = df.columns.str.strip()
    except Exception as e:
        print(f"Error reading file {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    # validate
    required_columns = ['CWE-ID', 'Name', 'Description', 'Applicable Platforms', 'Observed Examples']
    for col in required_columns:
        if col not in df.columns:
            print(f"Missing required column: {col}", file=sys.stderr)
            print(f"Available columns: {df.columns.tolist()}", file=sys.stderr)
            sys.exit(1)

    # match mode
    if args.mode == 'and':
        def language_match(cell):
            if pd.isna(cell):
                return False
            cell_content = str(cell).lower()
            return all(lang in cell_content for lang in language_list)
    else:
        def language_match(cell):
            if pd.isna(cell):
                return False
            cell_content = str(cell).lower()
            return any(lang in cell_content for lang in language_list)

    filtered = df[df['Applicable Platforms'].apply(language_match)]

    if filtered.empty:
        print("No records found for the specified languages.", file=sys.stderr)
        sys.exit(0)

    # for txt output
    with open(args.output, "w", encoding="utf-8") as f:
        for idx, row in filtered.iterrows():
            f.write(f"CWE-ID: {row['CWE-ID']}\n")
            f.write(f"Name: {row['Name']}\n")
            f.write(f"Description: {row['Description']}\n")
            examples = row['Observed Examples']
            if pd.notna(examples) and examples.strip():
                items = split_examples(examples)
                if items:
                    f.write("Observed Examples:\n")
                    for i, ex in enumerate(items, 1):
                        f.write(f"  Example {i}: {ex}\n")
                else:
                    f.write("Observed Examples: None\n")
            else:
                f.write("Observed Examples: None\n")
            f.write("-" * 60 + "\n")
    print(f"[INFO] Output written to {args.output}")

    # for CSV output
    # 1. example column
    examples_column = []
    for ex in filtered["Observed Examples"]:
        ex_list = split_examples(ex)
        joined = "\n".join(ex_list) if ex_list else ""
        examples_column.append(joined)

    #
    csv_df = pd.DataFrame({
        "CWE-ID": filtered["CWE-ID"],
        "Name": filtered["Name"],
        "Description": filtered["Description"],
        "Observed Examples": examples_column
    })

    # csv file name
    if args.output.endswith('.txt'):
        csv_outfile = args.output[:-4] + '.csv'
    else:
        csv_outfile = args.output + '.csv'

    #
    csv_df.to_csv(csv_outfile, index=False, encoding="utf-8")
    print(f"[INFO] CSV Output written to {csv_outfile} ")

if __name__ == "__main__":
    main()
