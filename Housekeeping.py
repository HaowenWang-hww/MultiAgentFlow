import os
import shutil
from pathlib import Path

# --- Define file categories and where to move them ---
CATEGORY_MAP = {
    "code": {
        "extensions": [".py", ".ipynb"],
        "target": "src"
    },
    "docs": {
        "extensions": [".md", ".rst"],
        "target": "docs"
    },
    "config": {
        "extensions": [".yml", ".yaml", ".json", ".toml"],
        "target": "config"
    },
    "data": {
        "extensions": [".csv", ".txt", ".tsv"],
        "target": "data"
    },
    "notebooks": {
        "extensions": [".ipynb"],
        "target": "notebooks"
    },
    "tests": {
        "contains": "test",
        "target": "tests"
    },
    "other": {
        "extensions": [],
        "target": "misc"
    }
}

# --- Create folder structure ---
def create_folders(base_path):
    for cat in CATEGORY_MAP.values():
        folder = Path(base_path) / cat["target"]
        folder.mkdir(parents=True, exist_ok=True)

# --- Move files to appropriate folders ---
def organize_files(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = Path(root) / file
            # Skip if already in a target folder
            if any(Path(file_path).parts[0] == cat["target"] for cat in CATEGORY_MAP.values()):
                continue

            moved = False
            for cat, details in CATEGORY_MAP.items():
                if "extensions" in details and file_path.suffix in details["extensions"]:
                    move_file(file_path, base_path / details["target"])
                    moved = True
                    break
                elif "contains" in details and details["contains"] in file.lower():
                    move_file(file_path, base_path / details["target"])
                    moved = True
                    break

            if not moved:
                move_file(file_path, base_path / CATEGORY_MAP["other"]["target"])

# --- Move helper ---
def move_file(src, dst_folder):
    dst_folder.mkdir(exist_ok=True, parents=True)
    dst = dst_folder / src.name
    print(f"📦 Moving {src} -> {dst}")
    shutil.move(str(src), str(dst))

# --- Main ---
if __name__ == "__main__":
    repo_path = Path(__file__).parent.resolve()
    print(f"🔍 Organizing project at: {repo_path}\n")
    create_folders(repo_path)
    organize_files(repo_path)
    print("\n✅ Housekeeping complete.")
