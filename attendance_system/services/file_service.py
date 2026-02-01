"""File service - Handle file operations (Unit 6)."""

from __future__ import annotations

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from ..exceptions import ReportGenerationError


class FileService:
    """Service to handle file operations including backups and exports."""

    def __init__(self, base_path: str = "static/reports"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.backups_path = self.base_path / "backups"
        self.backups_path.mkdir(parents=True, exist_ok=True)

    def export_to_csv(
        self,
        data: List[Dict[str, Any]],
        filename: str,
    ) -> str:
        """Export data to CSV file."""
        try:
            filepath = self.base_path / filename

            if not data:
                # Create empty CSV with headers
                with open(filepath, "w", newline="") as f:
                    f.write("")
                return str(filepath)

            # Write CSV
            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            return str(filepath)
        except Exception as e:
            raise ReportGenerationError(f"Failed to export CSV: {str(e)}")

    def export_to_json(
        self,
        data: Dict[str, Any] | List[Dict[str, Any]],
        filename: str,
    ) -> str:
        """Export data to JSON file."""
        try:
            filepath = self.base_path / filename

            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, default=str)

            return str(filepath)
        except Exception as e:
            raise ReportGenerationError(f"Failed to export JSON: {str(e)}")

    def import_from_json(self, filename: str) -> Dict[str, Any]:
        """Import data from JSON file."""
        try:
            filepath = self.base_path / filename

            with open(filepath, "r") as f:
                return json.load(f)
        except Exception as e:
            raise ReportGenerationError(f"Failed to import JSON: {str(e)}")

    def import_from_csv(self, filename: str) -> List[Dict[str, Any]]:
        """Import data from CSV file."""
        try:
            filepath = self.base_path / filename
            data = []

            with open(filepath, "r", newline="") as f:
                reader = csv.DictReader(f)
                data = list(reader)

            return data
        except Exception as e:
            raise ReportGenerationError(f"Failed to import CSV: {str(e)}")

    def create_backup(self, source_file: str, backup_name: str | None = None) -> str:
        """Create backup of a file."""
        try:
            source_path = Path(source_file)

            if not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {source_file}")

            if backup_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{source_path.stem}_{timestamp}{source_path.suffix}"

            backup_path = self.backups_path / backup_name

            # Read and write to backup
            with open(source_path, "rb") as src:
                content = src.read()

            with open(backup_path, "wb") as dst:
                dst.write(content)

            return str(backup_path)
        except Exception as e:
            raise ReportGenerationError(f"Failed to create backup: {str(e)}")

    def restore_from_backup(self, backup_name: str, restore_path: str) -> bool:
        """Restore file from backup."""
        try:
            backup_path = self.backups_path / backup_name

            if not backup_path.exists():
                raise FileNotFoundError(f"Backup not found: {backup_name}")

            # Read backup and write to restore location
            with open(backup_path, "rb") as src:
                content = src.read()

            restore_full_path = Path(restore_path)
            restore_full_path.parent.mkdir(parents=True, exist_ok=True)

            with open(restore_full_path, "wb") as dst:
                dst.write(content)

            return True
        except Exception as e:
            raise ReportGenerationError(f"Failed to restore from backup: {str(e)}")

    def get_backup_list(self) -> List[Dict[str, Any]]:
        """Get list of available backups."""
        backups = []

        for backup_file in self.backups_path.glob("*"):
            if backup_file.is_file():
                stat = backup_file.stat()
                backups.append(
                    {
                        "name": backup_file.name,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    }
                )

        return sorted(backups, key=lambda x: x["created"], reverse=True)

    def delete_old_backups(self, days_to_keep: int = 30) -> int:
        """Delete backups older than specified days."""
        try:
            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            deleted_count = 0

            for backup_file in self.backups_path.glob("*"):
                if backup_file.is_file():
                    if backup_file.stat().st_ctime < cutoff_time:
                        backup_file.unlink()
                        deleted_count += 1

            return deleted_count
        except Exception as e:
            raise ReportGenerationError(f"Failed to delete old backups: {str(e)}")

    def get_file_info(self, filename: str) -> Dict[str, Any]:
        """Get information about a file."""
        try:
            filepath = self.base_path / filename
            stat = filepath.stat()

            return {
                "name": filepath.name,
                "path": str(filepath),
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }
        except Exception as e:
            raise ReportGenerationError(f"Failed to get file info: {str(e)}")

    def list_files(self, pattern: str = "*") -> List[str]:
        """List files matching pattern."""
        files = []

        for file in self.base_path.glob(pattern):
            if file.is_file():
                files.append(file.name)

        return sorted(files)
