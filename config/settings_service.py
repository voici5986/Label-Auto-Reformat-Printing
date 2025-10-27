import json
from pathlib import Path
from typing import Any, Dict


class SettingsService:
    def __init__(self, file_path: Path, default_settings: Dict[str, Any]):
        self.file_path = file_path
        self.default_settings = default_settings

    def load(self) -> Dict[str, Any]:
        try:
            if self.file_path.exists():
                with self.file_path.open('r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    return {**self.default_settings, **saved_settings}
        except Exception:
            pass
        return self.default_settings.copy()

    def save(self, settings: Dict[str, Any]) -> None:
        try:
            with self.file_path.open('w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
