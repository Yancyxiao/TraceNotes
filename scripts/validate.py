"""Validate skill metadata, YAML syntax, and local Markdown destinations."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


IGNORED = {".git", ".venv", "__pycache__", "node_modules", "dist"}


def prose_only(text):
    return re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)


def anchors(text):
    found = set()
    counts = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", prose_only(text), re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        found.add(slug if number == 0 else f"{slug}-{number}")
    return found


def validate(root):
    source = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", source, re.S)
    assert match, "SKILL.md must start with YAML frontmatter"
    metadata = yaml.safe_load(match.group(1))
    assert metadata["name"] == "trace-notes", "Unexpected skill name"
    assert isinstance(metadata.get("description"), str) and metadata["description"].strip()
    assert len(metadata["description"]) <= 1024, "Description exceeds the skill format limit"
    ui = yaml.safe_load((root / "agents/openai.yaml").read_text(encoding="utf-8"))
    assert "$trace-notes" in ui["interface"]["default_prompt"]
    assert 25 <= len(ui["interface"]["short_description"]) <= 64

    link_count = 0
    yaml_count = 0
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORED for part in path.relative_to(root).parts):
            continue
        if path.suffix in {".yml", ".yaml"}:
            yaml.safe_load(path.read_text(encoding="utf-8"))
            yaml_count += 1
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        assert "[TODO" not in text, f"Unfinished scaffold: {path}"
        assert "C:/Users/Yancyxiaoone" not in text, f"Personal path: {path}"
        for destination in re.findall(r"\]\(([^\s)]+)\)", prose_only(text)):
            parsed = urlsplit(destination.strip("<>"))
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            assert target.is_relative_to(root.resolve()), f"Link escapes repository: {path}: {destination}"
            assert target.exists(), f"Missing link target: {path}: {destination}"
            if parsed.fragment and target.suffix == ".md":
                assert unquote(parsed.fragment) in anchors(target.read_text(encoding="utf-8")), (
                    f"Missing heading: {path}: {destination}"
                )
            link_count += 1

    workflow = yaml.safe_load((root / ".github/workflows/validate.yml").read_text(encoding="utf-8"))
    assert workflow["permissions"] == {"contents": "read"}
    assert set(workflow["jobs"]["validate"]["strategy"]["matrix"]["os"]) == {
        "ubuntu-latest", "windows-latest"
    }
    print(f"Metadata valid; {yaml_count} YAML files parsed; {link_count} local links/anchors checked.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    validate(args.root)


if __name__ == "__main__":
    main()
