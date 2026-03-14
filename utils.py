"""
utils.py — I/O and helper utilities for clinical AI evaluation pipeline.
"""

import json
import os
from pathlib import Path


def load_json(filepath: str):
    """Load and return parsed JSON from a file path."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, filepath: str, indent: int = 2):
    """Write data as formatted JSON to filepath, creating dirs if needed."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def get_qa_relations(qa: dict) -> list[dict]:
    """Safely extract the relations list from a metadata_from_qa dict."""
    if not qa or not isinstance(qa, dict):
        return []
    return qa.get("relations", []) or []


def discover_input_files(test_data_dir: str) -> list[tuple[str, str]]:
    """
    Walk test_data_dir and return list of (json_path, file_name) tuples.
    Handles both flat and nested folder structures.
    """
    results = []
    base = Path(test_data_dir)
    for path in sorted(base.rglob("*.json")):
        results.append((str(path), path.name))
    return results


def find_json_in_folder(folder_path: str):
    """Find the primary JSON file inside a chart folder (name matches folder)."""
    folder = Path(folder_path)
    folder_name = folder.name
    candidate = folder / f"{folder_name}.json"
    if candidate.exists():
        return str(candidate)
    # Fallback: any JSON in the folder
    jsons = list(folder.glob("*.json"))
    return str(jsons[0]) if jsons else None
