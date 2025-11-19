import json
from pathlib import Path
from typing import Any, Dict


class SettingsService:
    def __init__(self, file_path: Path, default_settings: Dict[str, Any]):
        self.file_path = file_path
        self.default_settings = default_settings

    def validate_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """验证并修正设置值，确保所有参数在有效范围内"""
        validated = self.default_settings.copy()
        
        # 验证语言
        if settings.get('language') in ['zh', 'th']:
            validated['language'] = settings['language']
        
        # 验证行数和列数 (1-10)
        if isinstance(settings.get('rows'), int) and 1 <= settings.get('rows', 0) <= 10:
            validated['rows'] = settings['rows']
        
        if isinstance(settings.get('cols'), int) and 1 <= settings.get('cols', 0) <= 10:
            validated['cols'] = settings['cols']
        
        # 验证边距 (0-30mm)
        if isinstance(settings.get('margin'), (int, float)) and 0 <= settings.get('margin', -1) <= 30:
            validated['margin'] = settings['margin']
        
        # 验证间距 (0-20mm)
        if isinstance(settings.get('spacing'), (int, float)) and 0 <= settings.get('spacing', -1) <= 20:
            validated['spacing'] = settings['spacing']
        
        # 验证方向
        if settings.get('orientation') in ['landscape', 'portrait']:
            validated['orientation'] = settings['orientation']
        
        return validated

    def load(self) -> Dict[str, Any]:
        try:
            if self.file_path.exists():
                with self.file_path.open('r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    # 验证加载的设置
                    return self.validate_settings(saved_settings)
        except Exception:
            pass
        return self.default_settings.copy()

    def save(self, settings: Dict[str, Any]) -> None:
        try:
            with self.file_path.open('w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
