from pathlib import Path
from datetime import datetime


class ExportService:
    """
    ExportService

    Responsible only for exporting conversation content.

    This service does NOT:
    - access UI
    - open dialogs
    - modify conversations

    It simply writes files.
    """

    def export_markdown(
        self,
        conversation,
        output_path: str,
    ):
        """
        Export a conversation to Markdown.
        """

        path = Path(output_path)

        lines = []

        lines.append(f"# {conversation.title}")
        lines.append("")

        lines.append(
            f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        lines.append("")
        lines.append("---")
        lines.append("")

        for message in conversation.messages:

            role = message.get("role", "").lower()
            content = message.get("content", "")

            if role == "user":
                heading = "## You"
            else:
                heading = "## Athena"

            lines.append(heading)
            lines.append("")
            lines.append(content)
            lines.append("")
            lines.append("---")
            lines.append("")

        path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return path

    def export_text(
        self,
        conversation,
        output_path: str,
    ):
        """
        Export a conversation as plain text.
        """

        path = Path(output_path)

        lines = []

        lines.append(conversation.title)
        lines.append("=" * len(conversation.title))
        lines.append("")

        lines.append(
            f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        lines.append("")

        for message in conversation.messages:

            role = message.get("role", "").lower()
            content = message.get("content", "")

            if role == "user":
                prefix = "You"
            else:
                prefix = "Athena"

            lines.append(f"{prefix}:")
            lines.append(content)
            lines.append("")

        path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return path


export_service = ExportService()