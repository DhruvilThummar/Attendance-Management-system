"""Visualization logic using Matplotlib."""
from __future__ import annotations
import io
import base64
import logging
from typing import Iterable
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def attendance_bar_chart(data: Iterable[tuple[str, float]]) -> str:
    """Generate a bar chart and return as base64 string."""
    if not data:
        return ""
        
    labels, values = zip(*data)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values, color='skyblue')
    ax.set_ylabel("Attendance %")
    ax.set_ylim(0, 100)
    ax.set_title("Student Attendance Overview")
    
    # Save to buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Encode
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def subject_performance_chart(subject_names: list[str], avg_attendances: list[float]) -> str:
    """Generate a chart comparing subject averages."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(subject_names, avg_attendances, color='lightgreen')
    ax.set_xlabel("Average Attendance %")
    ax.set_xlim(0, 100)
    ax.set_title("Subject-wise Performance")
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return base64.b64encode(buf.read()).decode('utf-8')
