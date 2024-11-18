import re
import sys

def extract_jinja_tags(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression to match Jinja2 tags
    tag_pattern = re.compile(r'({{.*?}}|{#.*?#}|{%.*?%})', re.DOTALL)
    
    # Find all matches in the file content
    tags = tag_pattern.findall(content)
    
    return tags

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file1> <file2> ... <fileN>")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        print(f"\n#Processing file: {file_path}")
        try:
            tags = extract_jinja_tags(file_path)
            if tags:
                print("#Jinja2 tags found in the file:")
                for tag in tags:
                    print(tag)
            else:
                print("#No Jinja2 tags found in the file.")
        except FileNotFoundError:
            print("#The specified file was not found. Please check the file path and try again.")

if __name__ == "__main__":
    main()
