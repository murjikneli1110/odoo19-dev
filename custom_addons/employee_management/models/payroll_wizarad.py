from odoo import models, fields, api
from calendar import Calendar, monthrange

class PayrollWizard(models.TransientModel):
    _name = "custom.payroll.wizard"
    _description = "Generate Payroll"
    _rec_name = "employee_id"

    employee_id = fields.Many2one("custom.employee", required=True)
    year = fields.Integer(required=True)
    month = fields.Integer(required=True)

    def action_generate_payroll(self):
        self.ensure_one()

        salary = self.employee_id.salary

        expected_hours, worked_hours, overtime_hours, weekend_hours, undertime_hours, net_hours = self._calculate_hours(self.employee_id, self.year, self.month)

        hourly_rate = salary / expected_hours

        overtime_multiplier = self.env["custom.payroll"].overtime_multiplier
        weekend_multiplier = self.env["custom.payroll"].weekend_multiplier

        gross_pay = (
            worked_hours * hourly_rate 
            + ((overtime_hours - undertime_hours) * hourly_rate * overtime_multiplier)
            + (weekend_hours * hourly_rate * weekend_multiplier)
        )

        adjustment = gross_pay - salary

        values = {
            "employee_id": self.employee_id.id,
            "year": self.year,
            "month": self.month,
            "salary": salary,
            "expected_hours": expected_hours,
            "worked_hours": worked_hours,
            "overtime_hours": overtime_hours,
            "weekend_hours": weekend_hours,
            "undertime_hours": undertime_hours,
            "net_hours": net_hours,
            "hourly_rate": hourly_rate,
            "adjustment": adjustment,
            "gross_pay": gross_pay,
            "calculated_at": fields.Datetime.now(),
        }

        payroll = self.env["custom.payroll"].search([
            ("employee_id", "=", self.employee_id.id),
            ("year", "=", self.year),
            ("month", "=", self.month),
        ], limit=1)

        if payroll:
            payroll.write(values)
        else:
            payroll = self.env["custom.payroll"].create(values)

        return payroll

    def _calculate_hours(self, employee, year, month):
            calendar = Calendar()
    
            expected_days = 0
            for day in calendar.itermonthdates(year, month):
                if day.month == month and day.weekday() < 5:
                    expected_days += 1
    
            expected_hours = expected_days * 8
    
            attendances = self.env["custom.attendance"].search([
                ("employee_id", "=", employee.id),
                ("date", ">=", f"{year}-{month:02d}-01"),
                ("date", "<=", f"{year}-{month:02d}-{monthrange(year, month)[1]}")
            ])
    
            worked_hours = 0
            overtime_hours = 0
            weekend_hours = 0
            undertime_hours = 0
    
            for attendance in attendances:
                date = attendance.date
    
                if date.weekday() < 5:
                    if attendance.hours_worked > 8:
                        worked_hours += 8
                        overtime_hours += attendance.hours_worked - 8
                    elif attendance.hours_worked < 8:
                        worked_hours += attendance.hours_worked
                        undertime_hours += 8 - attendance.hours_worked
                    else:
                        worked_hours += 8
                else:
                    weekend_hours += attendance.hours_worked
    
            net_hours = worked_hours + overtime_hours + weekend_hours - undertime_hours
    
            return expected_hours, worked_hours, overtime_hours, weekend_hours, undertime_hours, net_hours

    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)

        if self.env.context.get("active_model") == "custom.employee":
            vals["employee_id"] = self.env.context.get("active_id")

        return vals