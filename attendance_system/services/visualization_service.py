"""Visualization stub using Matplotlib."""
from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt


def attendance_bar_chart(data: Iterable[tuple[str, float]]) -> plt.Figure:
    labels, values = zip(*data) if data else ([], [])
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel("Attendance %")
    ax.set_ylim(0, 100)
    return fig
