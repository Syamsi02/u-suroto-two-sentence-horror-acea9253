#!/usr/bin/env python3
"""Two-Sentence Horror entry for make.fun.

Writes one original two-sentence horror story to /output/entry.txt
(the program/v1 harness artifact path). Pure standard library.
"""

import os
import sys

STORY = (
    "When the coroner handed me my brother's effects, the watch was "
    "still ticking, though its battery had died three years before he did. "
    "It stopped the moment I wound it, and from inside the case came the "
    "sound of someone exhaling, relieved."
)


def count_sentences(text):
    """Count sentences by terminal punctuation followed by space or end."""
    stripped = text.strip()
    count = 0
    for i, ch in enumerate(stripped):
        if ch in ".!?":
            if i + 1 == len(stripped) or stripped[i + 1] in " \t\n\"'":
                count += 1
    return count


def validate(text):
    if not text or not text.strip():
        raise ValueError("story is empty or only whitespace")
    if len(text) > 400:
        raise ValueError("story is %d characters, over the 400 limit" % len(text))
    if count_sentences(text) != 2:
        raise ValueError(
            "story has %d sentences, must be exactly 2" % count_sentences(text)
        )
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("story is not valid UTF-8 text: %s" % exc)


def output_path():
    preferred = "/output/entry.txt"
    try:
        os.makedirs("/output", exist_ok=True)
        probe = os.path.join("/output", ".write-test")
        with open(probe, "w", encoding="utf-8") as fh:
            fh.write("ok")
        os.remove(probe)
        return preferred
    except OSError:
        local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(local, exist_ok=True)
        return os.path.join(local, "entry.txt")


def main():
    validate(STORY)
    path = output_path()
    # The file holds exactly the story, no trailing newline: the gate
    # counts every character in /output/entry.txt.
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(STORY)
    print(STORY)
    print("characters: %d" % len(STORY))
    print("sentences: %d" % count_sentences(STORY))
    print("wrote: %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
