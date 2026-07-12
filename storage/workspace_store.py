"""
Athena AI

Workspace Store

Responsible for persisting workspaces.

No UI.
No business logic.
Only storage.
"""

from __future__ import annotations

import json
from pathlib import Path

from models.workspace import Workspace


class WorkspaceStore:

    def __init__(self):

        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.file_path = self.data_dir / "workspaces.json"

        if not self.file_path.exists():
            self._save_all([])

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _load_all(self):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

        except Exception:

            data = []

        return [
            Workspace.from_dict(item)
            for item in data
        ]

    def _save_all(self, workspaces):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                [
                    ws.to_dict()
                    for ws in workspaces
                ],
                f,
                indent=4,
                ensure_ascii=False
            )

    # --------------------------------------------------
    # CRUD
    # --------------------------------------------------

    def list(self):

        return self._load_all()

    def get(self, workspace_id):

        for workspace in self._load_all():

            if workspace.id == workspace_id:

                return workspace

        return None

    def save(self, workspace):

        workspaces = self._load_all()

        for i, ws in enumerate(workspaces):

            if ws.id == workspace.id:

                workspaces[i] = workspace
                self._save_all(workspaces)
                return

        workspaces.append(workspace)

        self._save_all(workspaces)

    def delete(self, workspace_id):

        workspaces = [

            ws

            for ws in self._load_all()

            if ws.id != workspace_id

        ]

        self._save_all(workspaces)

    def exists(self, workspace_id):

        return self.get(workspace_id) is not None

    def count(self):

        return len(
            self._load_all()
        )


workspace_store = WorkspaceStore()