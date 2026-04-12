from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
ANIMATION_OUTPUT_DIR = OUTPUT_DIR / "animation"


def get_run_output_dir(output_suffix: str) -> Path:
    suffix = (output_suffix or "").strip()
    return OUTPUT_DIR / suffix if suffix else OUTPUT_DIR


def get_animation_output_dir(output_suffix: str) -> Path:
    return get_run_output_dir(output_suffix) / "animation"
