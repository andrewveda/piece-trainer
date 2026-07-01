import json
from pathlib import Path

OUTPUT_DIR = Path("output")

for piece_dir in OUTPUT_DIR.iterdir():
    if not piece_dir.is_dir():
        continue

    print(f"Processing {piece_dir.name}...")

    # Read the existing index.json
    index_file = piece_dir / "index.json"
    with open(index_file, "r", encoding="utf-8") as f:
        index = json.load(f)

    # Support both formats:
    # ["part0001.json", ...]
    # or {"files":[...]}
    if isinstance(index, list):
        files = index
    else:
        files = index["files"]

    total_puzzles = 0

    for filename in files:
        with open(piece_dir / filename, "r", encoding="utf-8") as f:
            puzzles = json.load(f)
        total_puzzles += len(puzzles)

    # Preserve existing structure
    if isinstance(index, list):
        index = {
            "totalPuzzles": total_puzzles,
            "files": files
        }
    else:
        index["totalPuzzles"] = total_puzzles

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"  {total_puzzles:,} puzzles")

print("\nDone!")
