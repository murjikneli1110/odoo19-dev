from odoo import models, fields, api

class Attendance(models.Model):
    _name = "custom.attendance"
    _description = "Attendance"
    _order = "date desc"
    _rec_name = "employee_id"

    employee_id = fields.Many2one("custom.employee", string="Employee")

    date = fields.Date(required=True)
    status = fields.Selection(
        [
            ("worked", "Worked"),
            ("leave", "Leave"),
            ("sick_leave", "Sick Leave"),
            ("absent", "Absent")
        ],
        required=True,
        default="worked"
    )
    hours_worked = fields.Integer(required=True)
    overtime_hours = fields.Integer(compute="_compute_hours", store=True)
    undertime_hours = fields.Integer(compute="_compute_hours", store=True)

    _sql_constraints = [
        (
            "employee_date_unique",
            "UNIQUE(employee_id, date)",
            "Each Date Should Only Have One Attendacne Record Per Employee!"
        ),
    ]

    @api.depends("hours_worked")
    def _compute_hours(self):
        for record in self:
            if record.hours_worked == 8:
                record.overtime_hours = record.undertime_hours = 0
            elif record.hours_worked > 8:
                record.overtime_hours = record.hours_worked - 8
                record.undertime_hours = 0
            else:
                record.undertime_hours = 8 - record.hours_worked
                record.overtime_hours = 0