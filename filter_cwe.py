import pandas as pd
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Filter CWE data by programming language(s)")
    parser.add_argument('--languages', type=str, required=True,
                        help='Comma-separated language names (e.g. "Python,C#,PHP")')
    parser.add_argument('--input', type=str, default='699.csv',
                        help='Input CWE csv file (default: 699.csv)')
    parser.add_argument('--mode', type=str, default='or', choices=['or', 'and'],
                        help="Filter mode: 'or' (default) matches any language; 'and' matches only if all languages are present")
    args = parser.parse_args()

    # 解析语言参数，去除首尾空格
    language_list = [lang.strip().lower() for lang in args.languages.split(",")]

    # 读取CSV数据
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

    # 输出每条记录，格式友好
    for idx, row in filtered.iterrows():
        print(f"CWE-ID: {row['CWE-ID']}")
        print(f"Name: {row['Name']}")
        print(f"Description: {row['Description']}")
        examples = row['Observed Examples']
        if pd.notna(examples):
            print("Observed Examples:")
            for ex in str(examples).split("::"):
                if ex.strip():
                    print(f"    - {ex.strip()}")
        else:
            print("Observed Examples: None")
        print("-" * 60)

if __name__ == "__main__":
    main()
