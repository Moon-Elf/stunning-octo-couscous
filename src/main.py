# ----------------------------------------------
# File: main.py
# ----------------------------------------------

import logging
import os
import shutil
import sys
from pathlib import Path

from utils import generate_pages_recursive

# --------------------------------------------------------------------------- #
# 1. Logging configuration – very small so you see the copy actions.          #
# --------------------------------------------------------------------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


# --------------------------------------------------------------------------- #
# 2. Core helper – copy everything from `static` to `docs` cleanly.            #
# --------------------------------------------------------------------------- #
def copy_static(src: str = "static", dst: str = "docs") -> None:
    """
    Recursively copy the contents of `src` to `dst`.

    The destination directory is first cleaned (removed entirely) so that
    the copy is guaranteed to be a fresh, up‑to‑date snapshot of the source.
    Every file that is copied is logged at INFO level.

    Parameters
    ----------
    src : str, optional
        Path to the source directory.  Defaults to "static".
    dst : str, optional
        Path to the destination directory.  Defaults to "docs".
    """

    src_path = Path(src)
    dst_path = Path(dst)

    # 1️⃣  Validate the source exists.
    if not src_path.is_dir():
        raise FileNotFoundError(f"Source directory '{src_path}' does not exist")

    # 2️⃣  Clean the destination.
    if dst_path.exists():
        logging.info(f"Removing existing destination: {dst_path}")
        shutil.rmtree(dst_path)

    # 3️⃣  Re‑create the destination directory.
    logging.info(f"Creating destination: {dst_path}")
    dst_path.mkdir(parents=True, exist_ok=True)

    # 4️⃣  Walk the source tree and copy everything.
    for root, dirs, files in os.walk(src_path):
        # Compute the relative path from the source root.
        rel_root = Path(root).relative_to(src_path)

        # Ensure that each sub‑directory exists in the destination.
        dest_subdir = dst_path / rel_root
        if not dest_subdir.exists():
            logging.info(f"Creating sub‑directory: {dest_subdir}")
            dest_subdir.mkdir(parents=True, exist_ok=True)

        # Copy files in the current directory.
        for fname in files:
            src_file = Path(root) / fname
            dest_file = dest_subdir / fname
            shutil.copy2(src_file, dest_file)  # copy2 preserves metadata
            logging.info(f"Copied: {src_file} -> {dest_file}")


# --------------------------------------------------------------------------- #
# 5. Entry‑point – simply invoke the copy routine.                          #
# --------------------------------------------------------------------------- #
def main() -> None:
    """
    Main function that is called when you run `python main.py` or the
    helper script `main.sh`. It copies the static assets into the `docs`
    folder and prints a friendly message when finished.
    """
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    try:
        copy_static()
        print("\n✅  Static assets copied successfully to 'docs/'.")
        generate_pages_recursive(
            dir_path_content="content",
            template_path="template.html",
            dest_dir_path="docs",
            basepath=basepath,
        )
    except Exception as exc:
        logging.error(f"An error occurred while copying: {exc}")
        raise


if __name__ == "__main__":
    main()
