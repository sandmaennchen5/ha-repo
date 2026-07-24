import os
import json
import hashlib
import yaml
import requests
from deep_translator import GoogleTranslator
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional


class Translator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEEPL_API_KEY")
        self.deepl_available = bool(self.api_key)
        default_api = (
            "https://api-free.deepl.com/v2/translate"
            if (self.api_key or "").endswith(":fx")
            else "https://api.deepl.com/v2/translate"
        )
        self.deepl_url = os.getenv("DEEPL_API_URL", default_api)

    def deepl_translate(self, text: str, target_lang: str) -> Optional[str]:
        """Übersetzt Text mit DeepL API."""
        if not self.api_key:
            raise RuntimeError("DEEPL_API_KEY ist nicht gesetzt")

        try:
            headers = {"Authorization": f"DeepL-Auth-Key {self.api_key}"}
            data = {
                "text": text,
                "source_lang": "DE",
                "target_lang": target_lang.upper()
            }
            response = requests.post(self.deepl_url, headers=headers, data=data, timeout=10)

            if response.status_code != 200:
                raise RuntimeError(f"DeepL API Error {response.status_code}: {response.text}")

            return response.json()["translations"][0]["text"]
        except Exception as e:
            raise RuntimeError(f"DeepL-Übersetzung fehlgeschlagen: {e}") from e

    @staticmethod
    def split_text(text: str, limit: int = 4500) -> List[str]:
        """Teilt lange Texte an Zeilengrenzen für den No-Key-Fallback."""
        chunks: List[str] = []
        current = ""
        for line in text.splitlines(keepends=True):
            while len(line) > limit:
                if current:
                    chunks.append(current)
                    current = ""
                chunks.append(line[:limit])
                line = line[limit:]
            if current and len(current) + len(line) > limit:
                chunks.append(current)
                current = ""
            current += line
        if current or not chunks:
            chunks.append(current)
        return chunks

    def google_translate(self, text: str, target_lang: str) -> str:
        """Kostenloser Fallback über Google Translate ohne API-Key."""
        try:
            translator = GoogleTranslator(source="de", target=target_lang.lower())
            translated = [translator.translate(chunk) for chunk in self.split_text(text) if chunk]
            result = "".join(translated)
            if not result:
                raise RuntimeError("Google Translate hat keine Übersetzung zurückgegeben")
            return result
        except Exception as error:
            raise RuntimeError(f"No-Key-Übersetzung fehlgeschlagen: {error}") from error

    def translate_text(self, text: str, target_lang: str) -> str:
        """Nutzt DeepL und fällt ohne Key oder bei API-Fehlern auf Google zurück."""
        if self.deepl_available:
            try:
                result = self.deepl_translate(text, target_lang)
                if result:
                    return result
            except RuntimeError as error:
                self.deepl_available = False
                print(f"⚠️ {error}; verwende No-Key-Fallback")
        return self.google_translate(text, target_lang)

    def translate_dict(self, data: Any, target_lang: str) -> Any:
        """Rekursiv ein Dictionary/List übersetzen (Keys bleiben erhalten)."""
        if isinstance(data, dict):
            return {key: self.translate_dict(value, target_lang) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.translate_dict(item, target_lang) for item in data]
        elif isinstance(data, str):
            return self.translate_text(data, target_lang)
        return data

    def load_yaml(self, path: str) -> Any:
        """YAML-Datei laden."""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_json(self, path: str) -> Any:
        """JSON-Datei laden."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_text(self, path: str) -> str:
        """Text-Datei laden."""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def save_yaml(self, data: Any, path: str) -> None:
        """YAML-Datei speichern."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def save_json(self, data: Any, path: str) -> None:
        """JSON-Datei speichern."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

    def save_text(self, text: str, path: str) -> None:
        """Text-Datei speichern."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def translate_file(self, src_path: str, dest_path: str, target_lang: str) -> bool:
        """Übersetzt eine Datei basierend auf dem Format."""
        try:
            src_path = str(Path(src_path).resolve())
            dest_path = str(Path(dest_path).resolve())

            print(f"📝 Übersetze {src_path} → {dest_path}")

            if src_path.endswith((".md", ".txt")):
                text = self.load_text(src_path)
                translated = self.translate_text(text, target_lang)
                self.save_text(translated, dest_path)

            elif src_path.endswith((".yaml", ".yml")):
                data = self.load_yaml(src_path)
                translated = self.translate_dict(data, target_lang)
                self.save_yaml(translated, dest_path)

            elif src_path.endswith(".json"):
                data = self.load_json(src_path)
                translated = self.translate_dict(data, target_lang)
                self.save_json(translated, dest_path)

            else:
                print(f"⚠️ Dateiformat nicht unterstützt: {src_path}")
                return False

            print(f"✅ Erfolgreich übersetzt")
            return True

        except Exception as e:
            print(f"❌ Fehler beim Übersetzen: {e}")
            return False

    def find_source_files(self, patterns: List[str] = None, root: str = ".") -> List[Tuple[str, str]]:
        """Findet Dateien zum Übersetzen basierend auf Patterns."""
        if not patterns:
            patterns = ["de.yaml", "de.yml", "de.json", "README.md", "DOCS.md"]

        targets = []
        for root_dir, dirs, files in os.walk(root):
            dirs[:] = [directory for directory in dirs if directory not in {".git", "__pycache__"}]
            for file in files:
                path = os.path.join(root_dir, file)

                for pattern in patterns:
                    if pattern == file:
                        source = Path(path)
                        if pattern in {"README.md", "DOCS.md"}:
                            dest = str(source.with_name(f"{source.stem}.{{lang}}{source.suffix}"))
                        elif pattern in {"de.yaml", "de.yml", "de.json"}:
                            dest = str(source.with_name(f"{{lang}}{source.suffix}"))
                        else:
                            continue

                        targets.append((path, dest))
                        break

        return targets


def main():
    """Hauptfunktion für CLI-Verwendung."""
    import argparse

    parser = argparse.ArgumentParser(description="Übersetzt Dateien mit DeepL")
    parser.add_argument("--source", type=str, help="Quell-Datei")
    parser.add_argument("--dest", type=str, help="Ziel-Datei")
    parser.add_argument("--lang", type=str, default="en", help="Zielsprache (default: en)")
    parser.add_argument("--auto-find", action="store_true", help="Automatisch deutsche Dateien finden")
    parser.add_argument("--root", type=str, default=".", help="Root-Verzeichnis für auto-find")

    args = parser.parse_args()

    translator = Translator()

    if args.auto_find:
        root = Path(args.root).resolve()
        language = args.lang.lower()
        state_path = root / ".github" / "translation-state.json"
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            state = {}
        language_state = state.setdefault(language, {})

        print("🔍 Suche nach deutschen Dateien...")
        files = translator.find_source_files(root=str(root))
        pending = []
        for src, dest_pattern in files:
            source = Path(src).resolve()
            destination = Path(dest_pattern.format(lang=language)).resolve()
            relative = source.relative_to(root).as_posix()
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            if destination.is_file() and language_state.get(relative) == digest:
                print(f"⏭️ Unverändert: {relative}")
                continue
            pending.append((source, destination, relative, digest))

        print(f"📂 {len(files)} gefunden, {len(pending)} zu übersetzen")
        successful = 0
        for source, destination, relative, digest in pending:
            if not translator.translate_file(str(source), str(destination), args.lang):
                break
            language_state[relative] = digest
            successful += 1

        if successful != len(pending):
            print(f"❌ {successful}/{len(pending)} ausstehende Dateien erfolgreich übersetzt")
            raise SystemExit(1)

        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"✅ {successful}/{len(pending)} ausstehende Dateien erfolgreich übersetzt")

    elif args.source and args.dest:
        if not translator.translate_file(args.source, args.dest, args.lang):
            raise SystemExit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
