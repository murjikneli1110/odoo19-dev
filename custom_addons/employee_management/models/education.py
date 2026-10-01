from odoo import models, fields, api

class Education(models.Model):
    _name = "custom.education"
    _description = "Education"
    _order = "end_date desc, start_date desc"
    _rec_name = "degree"

    employee_id = fields.Many2one("custom.employee", ondelete="cascade", string="Employee")
    
    institution = fields.Char(required=True)
    degree = fields.Char(required=True)
    field_of_study = fields.Char(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date()
    is_current = fields.Boolean(compute="_check_end_date", store=True)

    @api.depends("end_date", "is_current")
    def _check_end_date(self):
        for record in self:
            record.is_current = not record.end_date