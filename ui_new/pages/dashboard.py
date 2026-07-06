from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
)

from ui_new.widgets.metric_card import MetricCard
from services.stats_service import StatsService


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        # -----------------------------
        # Main Layout
        # -----------------------------
        layout = QVBoxLayout(self)

        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # -----------------------------
        # Welcome Title
        # -----------------------------
        title = QLabel("🦉 Welcome to Athena AI")
        title.setObjectName("Title")

        subtitle = QLabel("Your Engineering AI Workspace")
        subtitle.setObjectName("Subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(15)

        # -----------------------------
        # Statistics Grid
        # -----------------------------
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)

        grid.addWidget(
            MetricCard(
                "Chats",
                StatsService.chat_count(),
                "Available",
            ),
            0,
            0,
        )

        grid.addWidget(
            MetricCard(
                "Reports",
                StatsService.report_count(),
                "Generated",
            ),
            0,
            1,
        )

        grid.addWidget(
            MetricCard(
                "Documents",
                StatsService.document_count(),
                "Indexed",
            ),
            1,
            0,
        )

        grid.addWidget(
            MetricCard(
                "Math",
                StatsService.math_count(),
                "Solved",
            ),
            1,
            1,
        )

        layout.addLayout(grid)

        layout.addSpacing(25)

        # -----------------------------
        # Recent Activity
        # -----------------------------
        activity_title = QLabel("Recent Activity")
        activity_title.setStyleSheet(
            "font-size:18px;"
            "font-weight:bold;"
        )

        layout.addWidget(activity_title)

        reports = sorted(
            StatsService.OUTPUTS.glob("*"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )[:5]

        if reports:

            for report in reports:
                item = QLabel(f"📄 {report.name}")
                item.setStyleSheet(
                    "font-size:13px;"
                    "padding:4px;"
                )
                layout.addWidget(item)

        else:

            empty = QLabel("No reports generated yet.")
            empty.setStyleSheet("color:gray;")
            layout.addWidget(empty)

        layout.addStretch()