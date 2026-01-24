"""Report generation using ReportLab."""
from __future__ import annotations
import logging
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ..config import DefaultConfig

logger = logging.getLogger(__name__)

def ensure_report_dir():
    cfg = DefaultConfig()
    path = Path(cfg.REPORTS_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path

def generate_daily_report(date_str: str, output: Path | None = None) -> Path:
    """Generate a PDF report for daily attendance."""
    path = ensure_report_dir()
    out = output or path / f"daily_report_{date_str}.pdf"
    
    try:
        c = canvas.Canvas(str(out), pagesize=letter)
        c.drawString(100, 750, f"Daily Attendance Report: {date_str}")
        
        # TODO: Fetch actual data for the day
        # For now, placeholder
        c.drawString(100, 730, "Subject: Mathematics")
        c.drawString(100, 715, "Faculty: Dr. Smith")
        c.drawString(100, 700, "Student | Status")
        c.line(100, 695, 300, 695)
        
        y = 680
        # Mock data iteration
        for i in range(1, 6):
            c.drawString(100, y, f"Student {i} | P")
            y -= 15
            
        c.save()
        logger.info(f"Report generated: {out}")
    except ImportError:
        logger.error("ReportLab not installed.")
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        
    return out

def generate_defaulter_report(subject_id: int, defaulters: list[dict], output: Path | None = None) -> Path:
    """Generate a PDF list of defaulters."""
    path = ensure_report_dir()
    out = output or path / f"defaulters_subject_{subject_id}.pdf"
    
    try:
        c = canvas.Canvas(str(out), pagesize=letter)
        c.drawString(100, 750, f"Defaulter List - Subject ID: {subject_id}")
        
        y = 720
        c.drawString(100, y, "ID | Enrollment | Percentage")
        y -= 20
        
        for d in defaulters:
            c.drawString(100, y, f"{d['student_id']} | {d['enrollment_no']} | {d['percentage']:.2f}%")
            y -= 15
            
        c.save()
        logger.info(f"Defaulter report generated: {out}")
    except Exception as e:
        logger.error(f"Failed to generate defaulter report: {e}")
        
    return out
