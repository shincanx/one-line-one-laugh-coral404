"""One Line, One Laugh -- make.fun entry.

Writes a single funny line (max 200 characters) to entry.txt in the
output directory. Deterministic, no network, no randomness, no input.
"""

import os

# The entry: one line, one laugh. 114 characters, under the 200 cap.
LINE = (
    "My bank flagged my own spending as suspicious, which is honestly "
    "the most accurate fraud detection I've ever seen."
)


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(LINE) > 200:
        raise ValueError(f"line is {len(LINE)} characters, over the 200 cap")
    if "\n" in LINE:
        raise ValueError("line must be a single line")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Round-trip check: what landed on disk is exactly the line.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != LINE:
        raise ValueError("entry.txt does not match the line")

    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
