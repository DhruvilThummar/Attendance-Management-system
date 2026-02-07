"""
Chart and visualization helper using matplotlib
"""
import io
import base64
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
from flask import current_app

# Use non-interactive backend for server environments
matplotlib.use('Agg')


def generate_attendance_weekly_chart(attendance_data):
    """
    Generate weekly attendance chart
    
    Args:
        attendance_data: dict with days as keys and attendance counts as values
        Example: {'Mon': 30, 'Tue': 28, 'Wed': 30, 'Thu': 29, 'Fri': 27}
    
    Returns:
        Base64 encoded PNG image string
    """
    fig, ax = plt.subplots(figsize=(10, 5), dpi=80)
    
    days = list(attendance_data.keys())
    counts = list(attendance_data.values())
    
    # Create bar chart
    bars = ax.bar(days, counts, color='#007bff', alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel('Day of Week', fontweight='bold')
    ax.set_ylabel('Number of Students Present', fontweight='bold')
    ax.set_title('Weekly Attendance Report', fontweight='bold', fontsize=14)
    max_count = max(counts) if counts else 0
    ax.set_ylim(0, max(max_count * 1.1, 10))  # Ensure minimum range of 10
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Convert to base64
    image_base64 = _fig_to_base64(fig)
    plt.close(fig)
    
    return image_base64


def generate_attendance_monthly_chart(attendance_data):
    """
    Generate monthly attendance trend chart
    
    Args:
        attendance_data: dict with dates as keys and attendance percentages as values
    
    Returns:
        Base64 encoded PNG image string
    """
    fig, ax = plt.subplots(figsize=(12, 5), dpi=80)
    
    dates = list(attendance_data.keys())
    percentages = list(attendance_data.values())
    
    # Create line chart with markers
    ax.plot(dates, percentages, marker='o', linewidth=2, markersize=6, 
            color='#28a745', label='Attendance %')
    ax.fill_between(range(len(dates)), percentages, alpha=0.3, color='#28a745')
    
    # Add value labels on points
    for i, (date, pct) in enumerate(zip(dates, percentages)):
        ax.text(i, pct + 1, f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Attendance Percentage (%)', fontweight='bold')
    ax.set_title('Monthly Attendance Trend', fontweight='bold', fontsize=14)
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Convert to base64
    image_base64 = _fig_to_base64(fig)
    plt.close(fig)
    
    return image_base64


def generate_role_distribution_chart(role_data):
    """
    Generate role distribution pie chart
    
    Args:
        role_data: dict with role names as keys and counts as values
        Example: {'FACULTY': 15, 'STUDENT': 200, 'HOD': 5}
    
    Returns:
        Base64 encoded PNG image string
    """
    fig, ax = plt.subplots(figsize=(10, 7), dpi=80)
    
    roles = list(role_data.keys())
    counts = list(role_data.values())
    colors = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1']
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(counts, labels=roles, autopct='%1.1f%%',
                                        colors=colors[:len(roles)], startangle=90,
                                        textprops={'fontweight': 'bold'})
    
    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('User Role Distribution', fontweight='bold', fontsize=14)
    plt.tight_layout()
    
    # Convert to base64
    image_base64 = _fig_to_base64(fig)
    plt.close(fig)
    
    return image_base64


def generate_department_comparison_chart(dept_data):
    """
    Generate department comparison bar chart
    
    Args:
        dept_data: dict with department names as keys and metrics as values
    
    Returns:
        Base64 encoded PNG image string
    """
    fig, ax = plt.subplots(figsize=(12, 5), dpi=80)
    
    depts = list(dept_data.keys())
    values = list(dept_data.values())
    
    # Create bar chart
    bars = ax.bar(depts, values, color=['#007bff', '#28a745', '#dc3545', '#ffc107'][:len(depts)],
                  alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel('Department', fontweight='bold')
    ax.set_ylabel('Count', fontweight='bold')
    ax.set_title('Department-wise Comparison', fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Convert to base64
    image_base64 = _fig_to_base64(fig)
    plt.close(fig)
    
    return image_base64


def generate_subject_attendance_chart(subject_data):
    """
    Generate subject-wise attendance chart
    
    Args:
        subject_data: dict with subject names as keys and attendance % as values
    
    Returns:
        Base64 encoded PNG image string
    """
    fig, ax = plt.subplots(figsize=(12, 5), dpi=80)
    
    subjects = list(subject_data.keys())
    attendance = list(subject_data.values())
    
    # Create horizontal bar chart
    bars = ax.barh(subjects, attendance, color='#17a2b8', alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center', fontweight='bold', fontsize=10)
    
    ax.set_xlabel('Attendance Percentage (%)', fontweight='bold')
    ax.set_title('Subject-wise Attendance', fontweight='bold', fontsize=14)
    ax.set_xlim(0, 105)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Convert to base64
    image_base64 = _fig_to_base64(fig)
    plt.close(fig)
    
    return image_base64


def generate_class_strength_chart(class_data):
    """
    Generate class strength distribution chart
    
    Args:
        class_data: dict with class/division names as keys and student counts as values
    
    Returns:
        Base64 encoded PNG image string
    """
    fig, ax = plt.subplots(figsize=(10, 6), dpi=80)
    
    classes = list(class_data.keys())
    strengths = list(class_data.values())
    colors = plt.cm.Set3(range(len(classes)))
    
    # Create bar chart
    bars = ax.bar(classes, strengths, color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel('Class / Division', fontweight='bold')
    ax.set_ylabel('Number of Students', fontweight='bold')
    ax.set_title('Class Strength Distribution', fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Convert to base64
    image_base64 = _fig_to_base64(fig)
    plt.close(fig)
    
    return image_base64


def generate_lecture_frequency_chart(lecture_data):
    """
    Generate lecture frequency chart (number of lectures per faculty/subject)
    
    Args:
        lecture_data: dict with faculty/subject names as keys and lecture counts as values
    
    Returns:
        Base64 encoded PNG image string
    """
    fig, ax = plt.subplots(figsize=(12, 5), dpi=80)
    
    names = list(lecture_data.keys())
    counts = list(lecture_data.values())
    
    # Create bar chart
    bars = ax.bar(names, counts, color='#6f42c1', alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel('Faculty / Subject', fontweight='bold')
    ax.set_ylabel('Number of Lectures', fontweight='bold')
    ax.set_title('Lecture Frequency Report', fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Convert to base64
    image_base64 = _fig_to_base64(fig)
    plt.close(fig)
    
    return image_base64


def _fig_to_base64(fig):
    """
    Convert matplotlib figure to base64 encoded string
    
    Args:
        fig: matplotlib figure object
    
    Returns:
        Base64 encoded string suitable for HTML img src
    """
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    image_base64 = base64.b64encode(img.getvalue()).decode()
    img.close()
    
    return f"data:image/png;base64,{image_base64}"
