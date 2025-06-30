import os
from pathlib import Path

# Define file categories and their extensions
file_types = {
    "code": [".py", ".ipynb"],
    "docs": [".md", ".rst"],
    "config": [".yml", ".yaml", ".toml", ".json"],
    "text": [".txt", ".csv"],
    "ignore": [".gitignore"],
}

# Define top-level folders to check
important_dirs = ["docs", "src", "multiagentflow", "tests", "examples", "notebooks"]

def scan_repo(repo_path="."):
    summary = {key: [] for key in file_types}
    summary["others"] = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            filepath = Path(root) / file
            ext = filepath.suffix.lower()
            matched = False

            for category, extensions in file_types.items():
                if ext in extensions:
                    summary[category].append(str(filepath))
                    matched = True
                    break

            if not matched:
                summary["others"].append(str(filepath))

    return summary

def print_summary(summary):
    for category, files in summary.items():
        print(f"\n🗂️ {category.upper()} FILES ({len(files)}):")
        for f in files:
            print(f"  - {f}")

if __name__ == "__main__":
    repo_root = Path(__file__).parent
    print(f"📁 Scanning repository at: {repo_root.resolve()}")
    summary = scan_repo(repo_root)
    print_summary(summary)
