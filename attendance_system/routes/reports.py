"""Reports API routes."""

from __future__ import annotations

from flask import render_template, request, jsonify, send_file
from datetime import datetime

from . import api
from ..services.report_service import ReportService
from ..decorators.rbac import login_required

report_svc = ReportService()


@api.route("/reports", methods=["GET"])
@login_required
def reports():
    """
    Reports page route.
    
    Returns:
        reports.html template
    """
    return render_template("reports.html")


@api.route("/reports/generate", methods=["POST"])
@login_required
def generate_report():
    """
    Generate attendance report.
    
    POST body:
        - report_type: "student", "class", "faculty", "department"
        - format: "pdf", "csv", "json"
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        - filters: Additional filters (dict)
    
    Returns:
        JSON response with report data or file download
    """
    data = request.get_json()
    
    report_type = data.get("report_type")
    format_type = data.get("format", "json")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    filters = data.get("filters", {})
    
    try:
        if report_type == "student":
            report_data = report_svc.generate_student_report(
                student_id=filters.get("student_id"),
                start_date=start_date,
                end_date=end_date
            )
        elif report_type == "class":
            report_data = report_svc.generate_class_report(
                class_id=filters.get("class_id"),
                start_date=start_date,
                end_date=end_date
            )
        elif report_type == "faculty":
            report_data = report_svc.generate_faculty_report(
                faculty_id=filters.get("faculty_id"),
                start_date=start_date,
                end_date=end_date
            )
        else:
            return jsonify({"success": False, "message": "Invalid report type"}), 400
        
        if format_type == "json":
            return jsonify({"success": True, "data": report_data})
        elif format_type == "csv":
            # Generate CSV file
            csv_file = report_svc.export_to_csv(report_data, report_type)
            return send_file(csv_file, as_attachment=True, download_name=f"{report_type}_report.csv")
        elif format_type == "pdf":
            # Generate PDF file
            pdf_file = report_svc.export_to_pdf(report_data, report_type)
            return send_file(pdf_file, as_attachment=True, download_name=f"{report_type}_report.pdf")
        else:
            return jsonify({"success": False, "message": "Invalid format"}), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api.route("/reports/analytics", methods=["GET"])
@login_required
def analytics_data():
    """
    Get analytics data for dashboards.
    
    Query params:
        - type: "overview", "trends", "comparison"
        - period: "week", "month", "semester", "year"
    
    Returns:
        JSON response with analytics data
    """
    analytics_type = request.args.get("type", "overview")
    period = request.args.get("period", "month")
    
    try:
        data = report_svc.get_analytics(analytics_type, period)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ========== Frontend Report Endpoints (UI-Compatible) ==========

@api.route("/reports/daily", methods=["GET"])
@login_required
def daily_report():
    """Daily report data for UI widgets."""
    try:
        date_str = request.args.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
        data = report_svc.generate_daily_report(date)
        return jsonify({
            "report_type": "daily",
            "summary": data,
            "students": [],
            "trend": []
        })
    except Exception:
        return jsonify({"report_type": "daily", "students": [], "trend": []})


@api.route("/reports/weekly", methods=["GET"])
@login_required
def weekly_report():
    """Weekly report data for UI widgets."""
    try:
        date_str = request.args.get("date")
        start_date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
        data = report_svc.generate_weekly_report(start_date)
        return jsonify({
            "report_type": "weekly",
            "summary": data,
            "students": [],
            "trend": []
        })
    except Exception:
        return jsonify({"report_type": "weekly", "students": [], "trend": []})


@api.route("/reports/monthly", methods=["GET"])
@login_required
def monthly_report():
    """Monthly report data for UI widgets."""
    try:
        year = int(request.args.get("year", datetime.now().year))
        month = int(request.args.get("month", datetime.now().month))
        data = report_svc.generate_monthly_report(year, month)
        return jsonify({
            "report_type": "monthly",
            "summary": data,
            "students": [],
            "trend": []
        })
    except Exception:
        return jsonify({"report_type": "monthly", "students": [], "trend": []})


@api.route("/reports/defaulters", methods=["GET"])
@login_required
def defaulters_report():
    """Defaulters report data for UI widgets."""
    try:
        defaulters = report_svc.generate_defaulter_list()
        return jsonify({"defaulters": defaulters})
    except Exception:
        return jsonify({"defaulters": []})


@api.route("/reports/subject-wise", methods=["GET"])
@login_required
def subject_wise_report():
    """Subject-wise report data for UI widgets."""
    try:
        subject_id = request.args.get("subject")
        if subject_id:
            data = report_svc.generate_subject_wise_report(int(subject_id))
            return jsonify({"subjects": [data]})
    except Exception:
        pass
    return jsonify({"subjects": []})


@api.route("/reports/division-wise", methods=["GET"])
@login_required
def division_wise_report():
    """Division-wise report data for UI widgets."""
    return jsonify({"divisions": []})