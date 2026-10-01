from odoo import models, fields, api

class Payroll(models.Model):
    _name = "custom.payroll"
    _description = "Payroll"
    _order = "year desc, month desc"
    _rec_name = "employee_id"

    employee_id = fields.Many2one("custom.employee", string="Employee", required=True)

    year = fields.Integer(required=True)
    month = fields.Integer(required=True)
    salary = fields.Float()
    expected_hours = fields.Float()
    worked_hours = fields.Float()
    overtime_hours = fields.Float()
    weekend_hours = fields.Float()
    undertime_hours = fields.Float()
    net_hours = fields.Float()
    hourly_rate = fields.Float()
    overtime_multiplier = 1.2
    weekend_multiplier = 1.5
    adjustment = fields.Float()
    gross_pay = fields.Float()
    calculated_at = fields.Datetime(default=fields.Datetime.now, readonly=True)

    _sql_constraints = [
        (
            "employee_year_month_unique",
            "UNIQUE(employee_id, year, month)",
            "Unique Payroll Records Should Exist For Each Month Per Employee!"
        )
    ]