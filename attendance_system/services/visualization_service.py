"""
Visualization Service - Generate graphs and charts using matplotlib
===============================================================

Provides methods to generate various attendance and performance reports
with graphical visualizations using matplotlib. Converts graphs to
base64 encoded images for embedding in HTML templates.

Bootstrap Color Palette (No Purple):
- Primary Blue: #0d6efd
- Success Green: #198754
- Danger Red: #dc3545
- Warning Yellow: #ffc107
- Secondary Gray: #6c757d
- Info Cyan: #0dcaf0

Methods:
--------
- attendance_pie_chart(present, absent, leave) - Pie chart for attendance
- monthly_attendance_bar(months_data) - Bar chart for monthly attendance
- faculty_performance_chart(faculty_data) - Faculty performance comparison
- subject_attendance_bar(subject_data) - Subject-wise attendance
- class_attendance_line(dates, percentages) - Attendance trend line chart
- department_attendance_heatmap(departments, months, data) - Department heatmap
- student_rank_bar(students_data) - Top student performance
- class_comparison_bar(classes_data) - Class-wise comparison
- absence_reasons_pie(reasons_data) - Absence reasons breakdown
- export_chart_to_base64(fig) - Convert matplotlib fig to base64 image

Usage Example:
--------------
from services.visualization_service import VisualizationService

viz = VisualizationService()
present, absent, leave = 85, 10, 5
base64_img = viz.attendance_pie_chart(present, absent, leave)
# Use base64_img in HTML: <img src="data:image/png;base64,{base64_img}" />
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


class VisualizationService:
    """
    Service for generating graphical reports and visualizations.
    
    Uses matplotlib to create various charts and converts them to
    base64 encoded images for web display. All colors use Bootstrap
    palette - no purple colors.
    """
    
    def __init__(self):
        """Initialize visualization service with default settings and Bootstrap colors."""
        plt.style.use('default')
        # Bootstrap Color Palette - Pure colors, NO PURPLE
        self.colors_bootstrap = {
            'primary': '#0d6efd',      # Bootstrap Blue
            'success': '#198754',      # Bootstrap Green
            'danger': '#dc3545',       # Bootstrap Red
            'warning': '#ffc107',      # Bootstrap Yellow
            'secondary': '#6c757d',    # Bootstrap Gray
            'info': '#0dcaf0',         # Bootstrap Cyan
            'light': '#f8f9fa',        # Bootstrap Light
            'dark': '#212529'          # Bootstrap Dark
        }
    
    @staticmethod
    def export_chart_to_base64(fig) -> str:
        """
        Convert matplotlib figure to base64 encoded image.
        
        Args:
            fig (matplotlib.figure.Figure): Matplotlib figure object
            
        Returns:
            str: Base64 encoded PNG image string for embedding in HTML
            
        Example:
            >>> fig, ax = plt.subplots()
            >>> ax.plot([1, 2, 3], [1, 2, 3])
            >>> base64_img = VisualizationService.export_chart_to_base64(fig)
        """
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        buffer.close()
        return image_base64
    
    def attendance_pie_chart(self, present: int, absent: int, leave: int) -> str:
        """
        Generate attendance pie chart showing present, absent, and leave.
        
        Uses Bootstrap Green, Red, and Yellow for maximum clarity.
        
        Args:
            present (int): Number of students present
            absent (int): Number of students absent
            leave (int): Number of students on leave
            
        Returns:
            str: Base64 encoded pie chart image
            
        Example:
            >>> viz = VisualizationService()
            >>> base64_img = viz.attendance_pie_chart(85, 10, 5)
            >>> # Render in HTML: <img src="data:image/png;base64,{base64_img}" />
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        sizes = [present, absent, leave]
        labels = ['Present', 'Absent', 'Leave']
        colors = [
            self.colors_bootstrap['success'],  # Green for present
            self.colors_bootstrap['danger'],   # Red for absent
            self.colors_bootstrap['warning']   # Yellow for leave
        ]
        explode = (0.05, 0.05, 0)
        
        ax.pie(
            sizes, 
            labels=labels, 
            colors=colors, 
            autopct='%1.1f%%',
            startangle=90,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 11, 'weight': 'bold'}
        )
        
        ax.set_title('Attendance Distribution', fontsize=14, weight='bold', pad=20)
        fig.patch.set_facecolor('white')
        
        return self.export_chart_to_base64(fig)
    
    def monthly_attendance_bar(self, months_data: Dict[str, float]) -> str:
        """
        Generate monthly attendance bar chart with color coding.
        
        Green bars for ≥90%, Yellow for 75-89%, Red for <75%.
        
        Args:
            months_data (Dict[str, float]): Dictionary with month names as keys
                                          and attendance percentage as values
                                          
        Returns:
            str: Base64 encoded bar chart image
            
        Example:
            >>> data = {
            ...     'January': 92.5,
            ...     'February': 88.0,
            ...     'March': 95.3,
            ...     'April': 89.7
            ... }
            >>> base64_img = viz.monthly_attendance_bar(data)
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        months = list(months_data.keys())
        percentages = list(months_data.values())
        
        # Color bars based on percentage
        bar_colors = [
            self.colors_bootstrap['success'] if p >= 90 else 
            self.colors_bootstrap['warning'] if p >= 75 else 
            self.colors_bootstrap['danger']
            for p in percentages
        ]
        
        bars = ax.bar(months, percentages, color=bar_colors, edgecolor='black', linewidth=1.5)
        
        # Add percentage labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height,
                f'{height:.1f}%',
                ha='center', 
                va='bottom',
                fontweight='bold'
            )
        
        ax.set_ylabel('Attendance %', fontsize=12, weight='bold')
        ax.set_xlabel('Month', fontsize=12, weight='bold')
        ax.set_title('Monthly Attendance Report', fontsize=14, weight='bold', pad=20)
        ax.set_ylim([0, 110])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        fig.patch.set_facecolor('white')
        fig.tight_layout()
        
        return self.export_chart_to_base64(fig)
    
    def faculty_performance_chart(self, faculty_data: Dict[str, int]) -> str:
        """
        Generate faculty performance bar chart showing student count per faculty.
        
        Shows which faculty has maximum students enrolled.
        
        Args:
            faculty_data (Dict[str, int]): Faculty names as keys,
                                         number of students as values
                                         
        Returns:
            str: Base64 encoded horizontal bar chart image
            
        Example:
            >>> data = {
            ...     'Dr. Smith': 150,
            ...     'Prof. Johnson': 200,
            ...     'Dr. Williams': 175,
            ...     'Prof. Brown': 165
            ... }
            >>> base64_img = viz.faculty_performance_chart(data)
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        faculty_names = list(faculty_data.keys())
        student_counts = list(faculty_data.values())
        
        bars = ax.barh(
            faculty_names, 
            student_counts, 
            color=self.colors_bootstrap['primary'],  # Bootstrap Blue
            edgecolor='black',
            linewidth=1.5
        )
        
        # Add count labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(
                width, 
                bar.get_y() + bar.get_height()/2.,
                f'{int(width)}',
                ha='left',
                va='center',
                fontweight='bold',
                fontsize=10
            )
        
        ax.set_xlabel('Number of Students', fontsize=12, weight='bold')
        ax.set_title('Faculty Performance (Student Count)', fontsize=14, weight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        fig.patch.set_facecolor('white')
        fig.tight_layout()
        
        return self.export_chart_to_base64(fig)
    
    def subject_attendance_bar(self, subject_data: Dict[str, float]) -> str:
        """
        Generate subject-wise attendance bar chart.
        
        Shows which subjects have highest/lowest attendance.
        
        Args:
            subject_data (Dict[str, float]): Subject names as keys,
                                           average attendance % as values
                                           
        Returns:
            str: Base64 encoded bar chart image
            
        Example:
            >>> data = {
            ...     'Mathematics': 92.3,
            ...     'Physics': 88.5,
            ...     'Chemistry': 95.1,
            ...     'Biology': 90.2,
            ...     'English': 93.7
            ... }
            >>> base64_img = viz.subject_attendance_bar(data)
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        subjects = list(subject_data.keys())
        percentages = list(subject_data.values())
        
        # Color based on attendance level
        bar_colors = [
            self.colors_bootstrap['success'] if p >= 90 else 
            self.colors_bootstrap['warning'] if p >= 75 else 
            self.colors_bootstrap['danger']
            for p in percentages
        ]
        
        bars = ax.bar(subjects, percentages, color=bar_colors, edgecolor='black', linewidth=1.5)
        
        # Add percentage labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.1f}%',
                ha='center',
                va='bottom',
                fontweight='bold'
            )
        
        ax.set_ylabel('Average Attendance %', fontsize=12, weight='bold')
        ax.set_title('Subject-wise Attendance Report', fontsize=14, weight='bold', pad=20)
        ax.set_ylim([0, 110])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        fig.patch.set_facecolor('white')
        fig.tight_layout()
        
        return self.export_chart_to_base64(fig)
    
    def class_attendance_line(self, dates: List[str], percentages: List[float]) -> str:
        """
        Generate class attendance trend line chart showing attendance over time.
        
        Includes reference lines for target (90%) and minimum (75%) attendance.
        
        Args:
            dates (List[str]): List of dates as strings (e.g., '2024-01-15')
            percentages (List[float]): Corresponding attendance percentages
            
        Returns:
            str: Base64 encoded line chart image
            
        Example:
            >>> dates = ['2024-01-15', '2024-01-16', '2024-01-17']
            >>> percentages = [92.5, 88.0, 95.3]
            >>> base64_img = viz.class_attendance_line(dates, percentages)
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x_pos = np.arange(len(dates))
        
        # Plot line with markers
        ax.plot(
            x_pos, 
            percentages, 
            color=self.colors_bootstrap['primary'],  # Blue line
            linewidth=3,
            marker='o',
            markersize=8,
            markerfacecolor=self.colors_bootstrap['success'],  # Green dots
            markeredgecolor='black',
            markeredgewidth=1.5
        )
        
        # Add value labels on points
        for i, (x, y) in enumerate(zip(x_pos, percentages)):
            ax.text(
                x, 
                y + 1.5,
                f'{y:.1f}%',
                ha='center',
                fontweight='bold',
                fontsize=9
            )
        
        # Add reference lines
        ax.axhline(y=90, color=self.colors_bootstrap['warning'], linestyle='--', alpha=0.5, label='Target: 90%')
        ax.axhline(y=75, color=self.colors_bootstrap['danger'], linestyle='--', alpha=0.5, label='Minimum: 75%')
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(dates, rotation=45, ha='right')
        ax.set_ylabel('Attendance %', fontsize=12, weight='bold')
        ax.set_xlabel('Date', fontsize=12, weight='bold')
        ax.set_title('Attendance Trend Analysis', fontsize=14, weight='bold', pad=20)
        ax.set_ylim([0, 110])
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='lower right')
        
        fig.patch.set_facecolor('white')
        fig.tight_layout()
        
        return self.export_chart_to_base64(fig)
    
    def department_attendance_heatmap(self, departments: List[str], 
                                     months: List[str], 
                                     data: np.ndarray) -> str:
        """
        Generate department attendance heatmap showing patterns across time.
        
        Red-Yellow-Green color mapping: Red (low attendance) to Green (high).
        
        Args:
            departments (List[str]): List of department names
            months (List[str]): List of month names
            data (np.ndarray): 2D array of attendance percentages
                              (rows=departments, cols=months)
                              
        Returns:
            str: Base64 encoded heatmap image
            
        Example:
            >>> deps = ['CSE', 'ECE', 'ME', 'CE']
            >>> months = ['Jan', 'Feb', 'Mar', 'Apr']
            >>> data = np.array([
            ...     [92, 88, 95, 90],
            ...     [85, 90, 88, 92],
            ...     [90, 92, 89, 94],
            ...     [88, 85, 91, 89]
            ... ])
            >>> base64_img = viz.department_attendance_heatmap(deps, months, data)
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=70, vmax=100)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(months)))
        ax.set_yticks(np.arange(len(departments)))
        ax.set_xticklabels(months)
        ax.set_yticklabels(departments)
        
        # Rotate the tick labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add text annotations
        for i in range(len(departments)):
            for j in range(len(months)):
                text = ax.text(
                    j, i, 
                    f'{data[i, j]:.1f}%',
                    ha="center", va="center", 
                    color="black",
                    fontweight='bold'
                )
        
        ax.set_title('Department-wise Attendance Heatmap', fontsize=14, weight='bold', pad=20)
        ax.set_xlabel('Month', fontsize=12, weight='bold')
        ax.set_ylabel('Department', fontsize=12, weight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Attendance %', rotation=270, labelpad=20, weight='bold')
        
        fig.patch.set_facecolor('white')
        fig.tight_layout()
        
        return self.export_chart_to_base64(fig)
    
    def student_rank_bar(self, students_data: Dict[str, float], top_n: int = 10) -> str:
        """
        Generate top student performance bar chart ranked by attendance.
        
        Displays top N students with highest attendance percentages.
        
        Args:
            students_data (Dict[str, float]): Student names as keys,
                                            attendance percentage as values
            top_n (int): Number of top students to display (default: 10)
            
        Returns:
            str: Base64 encoded bar chart image
            
        Example:
            >>> data = {
            ...     'Student A': 98.5,
            ...     'Student B': 97.3,
            ...     'Student C': 96.1,
            ...     'Student D': 95.2,
            ...     'Student E': 94.8
            ... }
            >>> base64_img = viz.student_rank_bar(data, top_n=5)
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Sort and get top N students
        sorted_students = sorted(students_data.items(), key=lambda x: x[1], reverse=True)
        top_students = dict(sorted_students[:top_n])
        
        names = list(top_students.keys())
        percentages = list(top_students.values())
        
        # Create colors with gradient - Green for excellent, Blue for good, Yellow for fair
        colors = [
            self.colors_bootstrap['success'] if p >= 95 else 
            self.colors_bootstrap['info'] if p >= 90 else 
            self.colors_bootstrap['warning']
            for p in percentages
        ]
        
        bars = ax.barh(names, percentages, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add percentage labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(
                width - 2,
                bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='right',
                va='center',
                fontweight='bold',
                color='white',
                fontsize=10
            )
        
        ax.set_xlabel('Attendance %', fontsize=12, weight='bold')
        ax.set_title(f'Top {top_n} Students by Attendance', fontsize=14, weight='bold', pad=20)
        ax.set_xlim([0, 105])
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        fig.patch.set_facecolor('white')
        fig.tight_layout()
        
        return self.export_chart_to_base64(fig)
    
    def class_comparison_bar(self, classes_data: Dict[str, float]) -> str:
        """
        Generate class-wise attendance comparison bar chart.
        
        Shows which classes have highest/lowest attendance.
        
        Args:
            classes_data (Dict[str, float]): Class names as keys,
                                            average attendance % as values
                                            
        Returns:
            str: Base64 encoded bar chart image
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        classes = list(classes_data.keys())
        percentages = list(classes_data.values())
        
        # Sort by percentage for better visualization
        sorted_data = sorted(zip(classes, percentages), key=lambda x: x[1], reverse=True)
        classes, percentages = zip(*sorted_data)
        
        bar_colors = [
            self.colors_bootstrap['success'] if p >= 90 else 
            self.colors_bootstrap['warning'] if p >= 75 else 
            self.colors_bootstrap['danger']
            for p in percentages
        ]
        
        bars = ax.bar(classes, percentages, color=bar_colors, edgecolor='black', linewidth=1.5)
        
        # Add labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.1f}%',
                ha='center',
                va='bottom',
                fontweight='bold'
            )
        
        ax.set_ylabel('Average Attendance %', fontsize=12, weight='bold')
        ax.set_xlabel('Class', fontsize=12, weight='bold')
        ax.set_title('Class-wise Attendance Comparison', fontsize=14, weight='bold', pad=20)
        ax.set_ylim([0, 110])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        fig.patch.set_facecolor('white')
        fig.tight_layout()
        
        return self.export_chart_to_base64(fig)
    
    def absence_reasons_pie(self, reasons_data: Dict[str, int]) -> str:
        """
        Generate pie chart showing breakdown of absence reasons.
        
        Uses Bootstrap color palette for visual distinction.
        
        Args:
            reasons_data (Dict[str, int]): Absence reasons as keys,
                                          count as values
                                          
        Returns:
            str: Base64 encoded pie chart image
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = list(reasons_data.keys())
        sizes = list(reasons_data.values())
        
        # Use Bootstrap colors - no purple
        color_list = [
            self.colors_bootstrap['danger'],
            self.colors_bootstrap['warning'],
            self.colors_bootstrap['info'],
            self.colors_bootstrap['secondary'],
            self.colors_bootstrap['dark']
        ]
        colors = (color_list * len(labels))[:len(labels)]
        
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            textprops={'fontsize': 10, 'weight': 'bold'}
        )
        
        # Make percentage text white for better visibility on colored backgrounds
        for autotext in autotexts:
            autotext.set_color('white')
        
        ax.set_title('Absence Reasons Distribution', fontsize=14, weight='bold', pad=20)
        fig.patch.set_facecolor('white')
        
        return self.export_chart_to_base64(fig)
