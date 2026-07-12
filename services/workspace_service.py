"""
Athena AI

Workspace Service

Business logic for workspaces.

Responsibilities
----------------
- Create workspaces
- Rename workspaces
- Delete workspaces
- Archive workspaces
- Manage conversations inside workspaces
- Track active workspace

No UI.
No file dialogs.
No widgets.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from models.workspace import Workspace
from storage.workspace_store import workspace_store


class WorkspaceService:

    def __init__(self):

        self.store = workspace_store

        self._active_workspace_id: Optional[str] = None

        self._ensure_default_workspace()

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    def _ensure_default_workspace(self):

        workspaces = self.store.list()

        if workspaces:
            self._active_workspace_id = workspaces[0].id
            return

        default = Workspace(
            name="General",
            description="Default Athena workspace",
            icon="💬"
        )

        self.store.save(default)

        self._active_workspace_id = default.id

    # --------------------------------------------------
    # Workspace CRUD
    # --------------------------------------------------

    def create_workspace(
        self,
        name: str,
        description: str = "",
        icon: str = "📁"
    ) -> Workspace:

        workspace = Workspace(
            name=name,
            description=description,
            icon=icon
        )

        self.store.save(workspace)

        return workspace

    def list_workspaces(self) -> List[Workspace]:

        return self.store.list()

    def get_workspace(
        self,
        workspace_id: str
    ) -> Optional[Workspace]:

        return self.store.get(workspace_id)

    def rename_workspace(
        self,
        workspace_id: str,
        new_name: str
    ) -> bool:

        workspace = self.store.get(workspace_id)

        if workspace is None:
            return False

        workspace.name = new_name.strip()

        workspace.updated_at = datetime.now().isoformat()

        self.store.save(workspace)

        return True

    def archive_workspace(
        self,
        workspace_id: str
    ) -> bool:

        workspace = self.store.get(workspace_id)

        if workspace is None:
            return False

        workspace.archived = True

        workspace.updated_at = datetime.now().isoformat()

        self.store.save(workspace)

        return True

    def delete_workspace(
        self,
        workspace_id: str
    ) -> bool:

        if not self.store.exists(workspace_id):
            return False

        self.store.delete(workspace_id)

        if self._active_workspace_id == workspace_id:

            workspaces = self.store.list()

            self._active_workspace_id = (
                workspaces[0].id
                if workspaces
                else None
            )

        return True

    # --------------------------------------------------
    # Active Workspace
    # --------------------------------------------------

    def get_active_workspace(self) -> Optional[Workspace]:

        if self._active_workspace_id is None:
            return None

        return self.store.get(
            self._active_workspace_id
        )

    def set_active_workspace(
        self,
        workspace_id: str
    ) -> bool:

        if not self.store.exists(workspace_id):
            return False

        self._active_workspace_id = workspace_id

        return True

    # --------------------------------------------------
    # Conversation Management
    # --------------------------------------------------

    def add_conversation(
        self,
        workspace_id: str,
        conversation_id: str
    ) -> bool:

        workspace = self.store.get(workspace_id)

        if workspace is None:
            return False

        if conversation_id not in workspace.conversation_ids:

            workspace.conversation_ids.append(
                conversation_id
            )

            workspace.updated_at = datetime.now().isoformat()

            self.store.save(workspace)

        return True

    def remove_conversation(
        self,
        workspace_id: str,
        conversation_id: str
    ) -> bool:

        workspace = self.store.get(workspace_id)

        if workspace is None:
            return False

        if conversation_id in workspace.conversation_ids:

            workspace.conversation_ids.remove(
                conversation_id
            )

            workspace.updated_at = datetime.now().isoformat()

            self.store.save(workspace)

        return True


workspace_service = WorkspaceService()