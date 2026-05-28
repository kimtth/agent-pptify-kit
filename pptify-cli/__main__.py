"""
pptify-cli  -  Lifecycle commands for the pptify generic coding-agent extension.

Usage (run as directory):
    uv run python pptify-cli install [--dry-run]
    uv run python pptify-cli uninstall [--dry-run]
    uv run python pptify-cli help [--designs] [--plugins] [--profile <id>]

Commands:
    install    Copy pptify skills, plugin tools, design templates, instructions,
               and policy into the local agent home (./.agent/).
    uninstall  Remove installed pptify assets from the local agent home (./.agent/).
    help       List available design profiles and plugin scripts.
               Use --designs for design profiles only.
               Use --plugins for plugin scripts only.
               Use --profile <id> to show a single profile as JSON.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_CLI_DIR = Path(__file__).parent          # pptify-cli/
_REPO_ROOT = _CLI_DIR.parent             # workspace root

_AGENTS_SRC = _REPO_ROOT / "agents"
_SKILLS_SRC = _REPO_ROOT / "skills"
_DESIGN_SRC = _REPO_ROOT / "resources" / "design"
_DESIGN_CATALOG = _DESIGN_SRC / "sources.json"
_PLUGIN_ROOT = _REPO_ROOT / "scripts"
_ENV_TEMPLATE_SRC = _REPO_ROOT / "resources" / "env.template"

_AGENT_HOME = Path.cwd() / ".agent"
_AGENTS_DST = _AGENT_HOME / "agents"
_SKILLS_DST = _AGENT_HOME / "skills"
_PLUGIN_DST = _AGENT_HOME / "scripts"
_DESIGN_DST = _AGENT_HOME / "resources" / "design"
_ENV_TEMPLATE_DST = _AGENT_HOME / "resources" / "env.template"
_POLICY_DST = _AGENT_HOME / "pptify-policy.md"
_INSTRUCTIONS_DST = _AGENT_HOME / "copilot-instruction.md"

_SKILL_PREFIX = "pptify-"

# Sentinel written into every file pptify manages. Present means safe to overwrite/delete.
_MANAGED_SENTINEL = "<!-- pptify-managed: do not edit manually -->"

# ---------------------------------------------------------------------------
# Developer-protection policy (seeded into ./.agent/pptify-policy.md)
# ---------------------------------------------------------------------------

_POLICY = """\
<!-- pptify-managed: do not edit manually -->
# pptify Developer-Protection Policy

Installed by pptify-cli. Do not edit manually; run `pptify install` to refresh.

## Secret and Credential Safety

- Never embed API keys, tokens, connection strings, or passphrases in deck
  specs, prompt assets, audit files, attempt manifests, or version-controlled
  files.
- Never collect API keys or tokens through chat or the VS Code prompt input
  dialog. Require the user to type secrets directly into a terminal or a
  managed secret environment (e.g. `az login`, `$env:OPENAI_API_KEY = ...`).
- If an image-generation helper fails due to missing credentials, persist a
  failure manifest with `provider`, `status: missing_credentials`, and `error`,
  and do not describe placeholder artwork as model-generated.

## Coordinate Contract

- All generated slides must use explicit `layout_tree` with final bboxes, font
  sizes, text colors, line endpoints/styles, shape names, and z-order.
- Prohibited obsolete shorthand keys: `pattern`, `layout_pattern`,
  `composition.pattern`, `layout`, `sections`, `bullets`, `objects`, `theme`.
- Every text-bearing object must carry explicit `style.font_size` and
  `style.color`.
- Every line object must carry `content.x1`, `content.y1`, `content.x2`,
  `content.y2` and explicit `style.line`/`style.line_width`.
- Every shape object must carry `content.shape`, `style.fill`, and
  `style.line`.

## Quality Gates

- Production-ready decks must have zero content collisions (verified by
  `scripts/audit/audit.py`).
- Production-ready decks must have zero text overflows.
- No `classification: "content"` object may use `style.font_size` below 9 pt.

## Asset and Design Boundaries

- Do not copy external fonts, icons, images, or binary assets without explicit
  license metadata and source attribution in `resources/design/sources.json` or
  `resources/design/third-party-notices.md`.
- For every new generated deck, load a profile from `resources/design/sources.json`
    unless a user-provided brand guide or reference PPTX is the primary style
    source. Do not invent a new design template.
- Production-ready decks must record selected profile IDs, source URLs, and
    style lock details in `summary.design_context`.
- Plain white, Calibri-only, bullet-heavy, default-theme PPTX output is a design
    failure even when collision and overflow audits pass.
- Keep source attribution and license metadata attached to any copied or
  adapted design context.

## Rendering Boundary

- The importable `pptify/` core renderer package and `python -m pptify` CLI
  are not present in this workspace snapshot. Use plugin scripts for
  extraction, conversion, design context, image helpers, and audit.
- Do not use obsolete renderer flags (`--provider copilot`, `--prompt`,
  `--prompt-file`, `--model`, `--spec-out`) unless a restored core CLI
  explicitly supports them.
"""

_INSTRUCTIONS = """\
<!-- pptify-managed: do not edit manually -->
# pptify Generic Coding-Agent Instructions

Use the installed `./.agent` assets as the local pptify runtime context.

## Installed Context

- Agents: `./.agent/agents/*.agent.md`
- Skills: `./.agent/skills/pptify-*`
- Design profiles and predefined templates: `./.agent/resources/design`
- Plugin tool set: `./.agent/scripts`
- Image provider environment template: `./.agent/resources/env.template`
- Developer-protection policy: `./.agent/pptify-policy.md`

## Agent Rules

- Read `./.agent/pptify-policy.md` before generating or repairing a deck.
- For every new generated deck, choose and load a `./.agent/resources/design`
    profile before authoring slides unless a user-provided brand guide or
    reference PPTX is the primary style source. Default to
    `fluent-ui-design-tokens`; for developer decks use `primer-primitives`; for
    consulting/governance decks use `likaku-mck-ppt-design-skill`; use
    `corazzon-pptx-design-styles` only when a broader modern style catalog is
    explicitly useful.
- Record selected profile IDs, source URLs, palette, typography, spacing rhythm,
    and signature elements in `summary.design_context`.
- Treat plain white, Calibri-only, bullet-heavy `python-pptx`-looking output as
    not production-ready.
- Use scripts under `./.agent/scripts` for source ingestion, design
    context loading, visual assets, PPTX extraction, and audit checks.
- When image generation needs provider configuration or credentials, create
    `./.agent/.env` from `./.agent/resources/env.template` and have the user fill secrets
    directly in that file. Do not ask for secrets in chat or prompt dialogs.
- Keep generated specs coordinate-explicit and preserve source/license metadata
    from the selected design profile.
"""

# ---------------------------------------------------------------------------
# Plugin catalogue
# ---------------------------------------------------------------------------

_PLUGINS: list[dict] = [
    {
        "id": "audit",
        "path": "scripts/audit/audit.py",
        "description": "Check content-region collisions and text overflows in layout-tree JSON specs.",
        "usage": "uv run python scripts/audit/audit.py <spec.json> --json",
    },
    {
        "id": "design-context-catalog",
        "path": "scripts/design/design_context_catalog.py",
        "description": "List or load source-backed design context profiles from resources/design.",
        "usage": "uv run python scripts/design/design_context_catalog.py --list --pretty",
    },
    {
        "id": "document-to-markdown",
        "path": "scripts/documents/document_to_markdown.py",
        "description": "Convert documents (PDF, DOCX, HTML) to Markdown using MarkItDown.",
        "usage": "uv run python scripts/documents/document_to_markdown.py --source doc.pdf --output-path doc.md",
    },
    {
        "id": "document-to-raptor-tree",
        "path": "scripts/documents/document_to_raptor_tree.py",
        "description": "Build a RAPTOR-style summary tree from a Markdown corpus, using local ONNX embeddings when available.",
        "usage": "uv run python scripts/documents/document_to_raptor_tree.py --markdown '# Source' --output-path tree.json --pretty",
    },
    {
        "id": "iconify-search",
        "path": "scripts/images/iconfy_search.py",
        "description": "Search Iconify for SVG icon candidates (Fluent, Material, etc.).",
        "usage": "uv run python scripts/images/iconfy_search.py --query governance --collection fluent --color 0078D4 --pretty",
    },
    {
        "id": "web-image-search",
        "path": "scripts/images/web_image_search.py",
        "description": "Return web image candidates for a search query.",
        "usage": "uv run python scripts/images/web_image_search.py --query 'cloud governance' --pretty",
    },
    {
        "id": "raster-image-to-svg",
        "path": "scripts/images/raster_image_to_svg.py",
        "description": "Wrap a raster image as SVG or vector-trace it using vtracer.",
        "usage": "uv run python scripts/images/raster_image_to_svg.py --source image.png --output-path image.svg --pretty",
    },
    {
        "id": "text-prompt-to-infographic",
        "path": "scripts/images/text_prompt_to_infographic.py",
        "description": (
            "Generate infographic images via OpenAI or Azure OpenAI. "
            "No local fallback provider. Create .env from resources/env.template "
            "when credentials or provider settings are required; never pass API keys as CLI arguments."
        ),
        "usage": (
            "uv run python scripts/images/text_prompt_to_infographic.py "
            "--provider azure-openai --azure-endpoint <endpoint> "
            "--model <deployment> --prompt 'Cloud governance roadmap' "
            "--output-path infographic.png --pretty"
        ),
    },
    {
        "id": "pptx-extractor",
        "path": "scripts/extraction/pptx_extractor.py",
        "description": "Importable PPTX extraction helper (load with importlib; not a CLI script).",
        "usage": (
            "importlib.util.spec_from_file_location("
            "'pptx_extractor', 'scripts/extraction/pptx_extractor.py')"
        ),
    },
    {
        "id": "pptx-style-master",
        "path": "scripts/extraction/pptx_style_master.py",
        "description": "Importable PPTX style-master analysis helper (load with importlib; not a CLI script).",
        "usage": (
            "importlib.util.spec_from_file_location("
            "'pptx_style_master', 'scripts/extraction/pptx_style_master.py')"
        ),
    },
]

# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------


def _is_pptify_managed(path: Path) -> bool:
    """Return True if the file was written by pptify-cli (contains the sentinel)."""
    try:
        return _MANAGED_SENTINEL in path.read_text(encoding="utf-8")
    except OSError:
        return False


def _copy_tree(src: Path, dst: Path) -> None:
    if src.resolve() == dst.resolve():
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )


def _install(dry_run: bool = False, agent_home: Path | None = None) -> None:
    """Copy pptify agents, skills, tools, design context, instructions, and policy."""
    home = agent_home or _AGENT_HOME
    agents_dst = home / "agents"
    skills_dst = home / "skills"
    plugin_dst = home / "scripts"
    design_dst = home / "resources" / "design"
    env_template_dst = home / "resources" / "env.template"
    policy_dst = home / "pptify-policy.md"
    instructions_dst = home / "copilot-instruction.md"

    if not _AGENTS_SRC.is_dir():
        print(f"ERROR: Agents source not found: {_AGENTS_SRC}", file=sys.stderr)
        sys.exit(1)
    if not _SKILLS_SRC.is_dir():
        print(f"ERROR: Skills source not found: {_SKILLS_SRC}", file=sys.stderr)
        sys.exit(1)
    if not _PLUGIN_ROOT.is_dir():
        print(f"ERROR: Plugin source not found: {_PLUGIN_ROOT}", file=sys.stderr)
        sys.exit(1)
    if not _DESIGN_SRC.is_dir():
        print(f"ERROR: Design source not found: {_DESIGN_SRC}", file=sys.stderr)
        sys.exit(1)
    if not _ENV_TEMPLATE_SRC.is_file():
        print(f"ERROR: Env template source not found: {_ENV_TEMPLATE_SRC}", file=sys.stderr)
        sys.exit(1)

    if not dry_run:
        agents_dst.mkdir(parents=True, exist_ok=True)
        skills_dst.mkdir(parents=True, exist_ok=True)

    installed_agents: list[str] = []
    installed_skills: list[str] = []

    for agent_file in sorted(_AGENTS_SRC.glob("*.agent.md")):
        dst = agents_dst / agent_file.name
        if dry_run:
            print(f"  [dry-run] Would install agent: {agent_file.name}  ->  {dst}")
        else:
            shutil.copy2(agent_file, dst)
            print(f"  Installed agent: {agent_file.name}  ->  {dst}")
        installed_agents.append(agent_file.name)

    for skill_dir in sorted(_SKILLS_SRC.iterdir()):
        if not skill_dir.is_dir() or not skill_dir.name.startswith(_SKILL_PREFIX):
            continue
        dst = skills_dst / skill_dir.name
        if dry_run:
            print(f"  [dry-run] Would install skill: {skill_dir.name}  ->  {dst}")
        else:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(skill_dir, dst)
            print(f"  Installed skill: {skill_dir.name}  ->  {dst}")
        installed_skills.append(skill_dir.name)

    # Plugin tool set and predefined design context
    for label, src, dst in (
        ("plugin tool set", _PLUGIN_ROOT, plugin_dst),
        ("design context", _DESIGN_SRC, design_dst),
    ):
        if dry_run:
            print(f"  [dry-run] Would install {label}: {src}  ->  {dst}")
        else:
            _copy_tree(src, dst)
            print(f"  Installed {label}: {src}  ->  {dst}")

    # Image provider env template
    if dry_run:
        print(f"  [dry-run] Would write env template if missing: {env_template_dst}")
    elif env_template_dst.exists():
        print(f"  SKIP env template (already exists): {env_template_dst}")
    else:
        env_template_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_ENV_TEMPLATE_SRC, env_template_dst)
        print(f"  Installed env template: {env_template_dst}")

    # Developer-protection policy
    if dry_run:
        print(f"  [dry-run] Would write policy: {policy_dst}")
    elif not policy_dst.exists() or _is_pptify_managed(policy_dst):
        policy_dst.write_text(_POLICY, encoding="utf-8")
        print(f"  Seeded policy: {policy_dst}")
    else:
        print(f"  SKIP policy (user-owned, no sentinel): {policy_dst}")

    # Generic coding-agent instructions
    if dry_run:
        print(f"  [dry-run] Would write instructions: {instructions_dst}")
    elif not instructions_dst.exists() or _is_pptify_managed(instructions_dst):
        instructions_dst.write_text(_INSTRUCTIONS, encoding="utf-8")
        print(f"  Seeded instructions: {instructions_dst}")
    else:
        print(f"  SKIP instructions (user-owned, no sentinel): {instructions_dst}")

    msg = f"pptify installed: {len(installed_agents)} agent(s) to {agents_dst}; {len(installed_skills)} skill(s) to {skills_dst}"
    print(f"\n{('[dry-run] ' if dry_run else '')}{msg}")


# ---------------------------------------------------------------------------
# Uninstall
# ---------------------------------------------------------------------------


def _uninstall(dry_run: bool = False, agent_home: Path | None = None) -> None:
    """Remove installed pptify assets from the user's agent home."""
    home = agent_home or _AGENT_HOME
    agents_dst = home / "agents"
    skills_dst = home / "skills"
    plugin_dst = home / "scripts"
    design_dst = home / "resources" / "design"
    env_template_dst = home / "resources" / "env.template"
    policy_dst = home / "pptify-policy.md"
    instructions_dst = home / "copilot-instruction.md"

    removed: list[str] = []
    removed_assets = 0

    if agents_dst.is_dir():
        installed_agent_names = {
            p.name for p in _AGENTS_SRC.glob("*.agent.md")
        } if _AGENTS_SRC.is_dir() else set()
        for agent_file in sorted(agents_dst.iterdir()):
            if agent_file.is_file() and agent_file.name in installed_agent_names:
                if dry_run:
                    print(f"  [dry-run] Would remove agent: {agent_file}")
                else:
                    agent_file.unlink()
                    print(f"  Removed agent: {agent_file}")
                removed_assets += 1
        if not dry_run and agents_dst.is_dir() and not any(agents_dst.iterdir()):
            agents_dst.rmdir()

    if skills_dst.is_dir():
        for skill_dir in sorted(skills_dst.iterdir()):
            if skill_dir.is_dir() and skill_dir.name.startswith(_SKILL_PREFIX):
                if dry_run:
                    print(f"  [dry-run] Would remove skill: {skill_dir}")
                else:
                    shutil.rmtree(skill_dir)
                    print(f"  Removed skill: {skill_dir}")
                removed.append(skill_dir.name)
                removed_assets += 1

    if policy_dst.exists():
        if _is_pptify_managed(policy_dst):
            if dry_run:
                print(f"  [dry-run] Would remove policy: {policy_dst}")
            else:
                policy_dst.unlink()
                print(f"  Removed policy: {policy_dst}")
            removed_assets += 1
        else:
            print(f"  SKIP policy (user-owned, no sentinel): {policy_dst}")

    if instructions_dst.exists():
        if _is_pptify_managed(instructions_dst):
            if dry_run:
                print(f"  [dry-run] Would remove instructions: {instructions_dst}")
            else:
                instructions_dst.unlink()
                print(f"  Removed instructions: {instructions_dst}")
            removed_assets += 1
        else:
            print(f"  SKIP instructions (user-owned, no sentinel): {instructions_dst}")

    for label, dst in (
        ("plugin tool set", plugin_dst),
        ("design context", design_dst),
    ):
        if dst.exists():
            if dry_run:
                print(f"  [dry-run] Would remove {label}: {dst}")
            else:
                shutil.rmtree(dst)
                print(f"  Removed {label}: {dst}")
            removed_assets += 1

    if env_template_dst.exists():
        if dry_run:
            print(f"  [dry-run] Would remove env template: {env_template_dst}")
        else:
            env_template_dst.unlink()
            print(f"  Removed env template: {env_template_dst}")
        removed_assets += 1

    resources_dst = home / "resources"
    if resources_dst.is_dir() and not any(resources_dst.iterdir()) and not dry_run:
        resources_dst.rmdir()

    if removed_assets == 0 and not removed:
        print(f"pptify is not installed in {home}.")
        return

    msg = f"pptify uninstalled: {len(removed)} skill(s) removed from {skills_dst}"
    print(f"\n{('[dry-run] ' if dry_run else '')}{msg}")

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------


def _cmd_help(show_designs: bool, show_plugins: bool, profile_id: str | None) -> None:
    """List available design profiles and/or plugin scripts."""
    if not show_designs and not show_plugins:
        show_designs = True
        show_plugins = True

    if profile_id:
        _show_profile(profile_id)
        return

    if show_designs:
        _print_designs()

    if show_plugins:
        if show_designs:
            print()
        _print_plugins()


def _load_catalog() -> dict | None:
    if not _DESIGN_CATALOG.is_file():
        return None
    with _DESIGN_CATALOG.open(encoding="utf-8") as fh:
        return json.load(fh)


def _print_designs() -> None:
    catalog = _load_catalog()
    if not catalog:
        print(f"ERROR: Design catalog not found: {_DESIGN_CATALOG}", file=sys.stderr)
        return

    profiles: list[dict] = catalog.get("profiles", [])
    print(f"Design Profiles  ({len(profiles)} available)")
    print("=" * 60)

    for p in profiles:
        print(f"\n  {p['id']}")
        print(f"    Name:     {p.get('name', '')}")
        print(f"    Kind:     {p.get('kind', '')}")
        best_for: list[str] = p.get("best_for", [])
        if best_for:
            print(f"    Best for: {', '.join(best_for)}")
        src: dict = p.get("source", {})
        if src.get("repo"):
            print(f"    Source:   {src['repo']}")
        lic: dict = p.get("license", {})
        if lic.get("spdx"):
            print(f"    License:  {lic['spdx']}")

    print()
    print("Load a profile:")
    print("  uv run python scripts/design/design_context_catalog.py \\")
    print("      --profile <id> --include-context --pretty")
    print()
    print("Show detail:  pptify help --profile <id>")


def _show_profile(profile_id: str) -> None:
    catalog = _load_catalog()
    if not catalog:
        print(f"ERROR: Design catalog not found: {_DESIGN_CATALOG}", file=sys.stderr)
        sys.exit(1)

    profiles: dict[str, dict] = {p["id"]: p for p in catalog.get("profiles", [])}
    if profile_id not in profiles:
        available = ", ".join(profiles)
        print(
            f"ERROR: Profile '{profile_id}' not found.\n"
            f"Available: {available}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(json.dumps(profiles[profile_id], indent=2))


def _print_plugins() -> None:
    print(f"Plugin Scripts  ({len(_PLUGINS)} available)")
    print("=" * 60)
    for plugin in _PLUGINS:
        print(f"\n  {plugin['id']}")
        print(f"    Path:    {plugin['path']}")
        print(f"    {plugin['description']}")
        print(f"    Usage:   {plugin['usage']}")


def _resolve_agent_home(home_arg: str | None) -> Path | None:
    if not home_arg:
        return None
    base = Path(home_arg).expanduser().resolve()
    if base.name.lower() == ".agent":
        return base
    return base / ".agent"


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pptify",
        description="pptify lifecycle and discovery commands.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # install
    install_p = subparsers.add_parser(
        "install",
        help="Install pptify agents, skills, tools, design context, instructions, and policy into ./.agent/.",
        description=(
            "Copy pptify agents from agents/ into ./.agent/agents/, "
            "copy all pptify-* skills from skills/ into ./.agent/skills/, "
            "copy scripts/ and resources/design/ "
            "into ./.agent/, and seed the developer-protection policy and "
            "agent instruction file."
        ),
    )
    install_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without making any changes.",
    )
    install_p.add_argument(
        "--home",
        metavar="<dir>",
        help="Install under <dir>/.agent instead of ./.agent. If <dir> already ends with .agent, use it directly.",
    )

    # uninstall
    uninstall_p = subparsers.add_parser(
        "uninstall",
        help="Remove installed pptify assets from ./.agent/.",
        description=(
            "Remove installed pptify agents from ./.agent/agents/, "
            "remove all pptify-* skill directories from ./.agent/skills/, "
            "delete "
            "./.agent/pptify-policy.md and ./.agent/copilot-instruction.md, "
            "and remove ./.agent/scripts/ and ./.agent/resources/design/."
        ),
    )
    uninstall_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without making any changes.",
    )
    uninstall_p.add_argument(
        "--home",
        metavar="<dir>",
        help="Uninstall from <dir>/.agent instead of ./.agent. If <dir> already ends with .agent, use it directly.",
    )

    # help
    help_p = subparsers.add_parser(
        "help",
        help="List available design profiles and plugin scripts.",
        description=(
            "Show available pptify design profiles (from resources/design/sources.json) "
            "and plugin scripts (from scripts/). "
            "With no flags, both sections are shown."
        ),
    )
    help_p.add_argument(
        "--designs",
        action="store_true",
        help="Show design profiles only.",
    )
    help_p.add_argument(
        "--plugins",
        action="store_true",
        help="Show plugin scripts only.",
    )
    help_p.add_argument(
        "--profile",
        metavar="<id>",
        help="Print the full JSON record for a single design profile.",
    )

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "install":
        home = _resolve_agent_home(args.home)
        _install(dry_run=args.dry_run, agent_home=home)
    elif args.command == "uninstall":
        home = _resolve_agent_home(args.home)
        _uninstall(dry_run=args.dry_run, agent_home=home)
    elif args.command == "help":
        _cmd_help(
            show_designs=args.designs,
            show_plugins=args.plugins,
            profile_id=args.profile,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
