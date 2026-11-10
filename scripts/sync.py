#!/usr/bin/env python3
"""Sync the FalcoSENSE integration from Home Assistant core into this HACS repo.

Copies ``homeassistant/components/falcosense/`` from a local Home Assistant core
checkout into ``custom_components/falcosense/`` and rewrites the manifest so it
passes HACS and hassfest validation as a custom integration (see
``patch_manifest``). Everything else is copied verbatim, including the generated
``translations/en.json`` (HACS has no build step to generate it). Re-run after
any change in core.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DST = REPO_ROOT / "custom_components" / "falcosense"

DEFAULT_VERSION = "0.1.5"

GITHUB_REPO = "tridonic-com/ha-falcosense"

# Packages Home Assistant ships as direct dependencies must not be listed at all
# by a custom integration.
DROP_REQUIREMENTS: frozenset[str] = frozenset({"Pillow"})
# Packages Home Assistant only constrains must be loosened from "==" to ">=" so
# they follow core instead of pinning against it.
LOOSEN_REQUIREMENTS: frozenset[str] = frozenset()
# Categories to add only when core defines none (HACS wants categories).
DEFAULT_CATEGORIES: list[str] = [
    "presence_location",
    "hubs_protocols.building_automation",
]

EXCLUDE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")


def _package_name(requirement: str) -> str:
    """Return the distribution name from a requirement like ``Pillow==1.0``."""
    return re.split(r"[=<>!~ ]", requirement, maxsplit=1)[0].strip()


def _patch_requirements(requirements: list[str]) -> list[str]:
    patched: list[str] = []
    for req in requirements:
        name = _package_name(req)
        if name in DROP_REQUIREMENTS:
            continue
        if name in LOOSEN_REQUIREMENTS:
            req = req.replace("==", ">=")
        patched.append(req)
    return patched


def patch_manifest(path: Path, version: str) -> None:
    """Rewrite the core manifest into a HACS-custom one.

    Versus the core manifest this:
    - adds a ``version`` field (required for custom integrations),
    - points ``documentation``/``issue_tracker`` at this GitHub repo (hassfest
      rejects the home-assistant.io URL for custom integrations),
    - drops/loosens requirements Home Assistant itself ships,
    - adds fallback ``categories`` when core defines none, and
    - sorts keys as hassfest expects (``domain``, ``name``, then alphabetical).
    """
    manifest = json.loads(path.read_text(encoding="utf-8"))

    manifest["version"] = version
    manifest["documentation"] = f"https://github.com/{GITHUB_REPO}"
    manifest["issue_tracker"] = f"https://github.com/{GITHUB_REPO}/issues"
    if "requirements" in manifest:
        manifest["requirements"] = _patch_requirements(manifest["requirements"])
    if DEFAULT_CATEGORIES and not manifest.get("categories"):
        manifest["categories"] = DEFAULT_CATEGORIES

    rest = sorted(key for key in manifest if key not in ("domain", "name"))
    ordered = {key: manifest[key] for key in ("domain", "name", *rest)}

    path.write_text(
        json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--core-path",
        type=Path,
        default=REPO_ROOT.parent / "core",
        help="Path to the Home Assistant core checkout (default: ../core).",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Integration version for the manifest (default: keep existing or "
        f"{DEFAULT_VERSION}).",
    )
    args = parser.parse_args()

    src = args.core_path / "homeassistant" / "components" / "falcosense"
    if not src.is_dir():
        raise SystemExit(f"FalcoSENSE integration not found at {src}")

    # Preserve the existing version unless explicitly overridden.
    version = args.version
    if version is None:
        existing = DST / "manifest.json"
        if existing.is_file():
            version = json.loads(existing.read_text(encoding="utf-8")).get(
                "version", DEFAULT_VERSION
            )
        else:
            version = DEFAULT_VERSION

    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(src, DST, ignore=EXCLUDE)

    patch_manifest(DST / "manifest.json", version)

    print(f"Synced {src} -> {DST}")
    print(f"  version: {version}")
    print("Remember to bump the version and cut a matching release tag.")


if __name__ == "__main__":
    main()
