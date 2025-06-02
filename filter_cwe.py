import pandas as pd
import argparse
import sys
import re

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

    # 
    language_list = [lang.strip().lower() for lang in args.languages.split(",")]

    # 读取CSV
    try:
        df = pd.read_csv(args.input, index_col=False)
        df.columns = df.columns.str.strip()
    except Exception as e:
        print(f"Error reading file {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    # 必要字段校验
    required_columns = ['CWE-ID', 'Name', 'Description', 'Applicable Platforms', 'Observed Examples']
    for col in required_columns:
        if col not in df.columns:
            print(f"Missing required column: {col}", file=sys.stderr)
            print(f"Available columns: {df.columns.tolist()}", file=sys.stderr)
            sys.exit(1)

    # 匹配方式
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

    # 输出到文件
    with open(args.output, "w", encoding="utf-8") as f:
        for idx, row in filtered.iterrows():
            f.write(f"CWE-ID: {row['CWE-ID']}\n")
            f.write(f"Name: {row['Name']}\n")
            f.write(f"Description: {row['Description']}\n")
            examples = row['Observed Examples']
            if pd.notna(examples) and examples.strip():
                items = [ex.strip() for ex in str(examples).split("::") if ex.strip()]
                if items:
                    f.write("Observed Examples:\n")
                    for i, ex in enumerate(items, 1):
                        f.write(f"  Example {i}:\n")
                        pattern = r'([A-Z_]+):\s*(.*?)(?=:[A-Z_]+:|$)'
                        matches = re.findall(pattern, ex)
                        if matches:
                            for key, val in matches:
                                f.write(f"    {key.strip()}: {val.strip()}\n")
                        else:
                            for line in ex.splitlines():
                                f.write(f"    {line.strip()}\n")
                else:
                    f.write("Observed Examples: None\n")
            else:
                f.write("Observed Examples: None\n")
            f.write("-" * 60 + "\n")
    print(f"[INFO] Output written to {args.output}")

if __name__ == "__main__":
    main()
