from odoo import models, fields, api

class Position(models.Model):
    _name = "custom.position"
    _description = "Position"
    _order = "end_date desc"
    _rec_name = "title"

    employee_id = fields.Many2one("custom.employee", ondelete="cascade", string="Employee")
    
    title = fields.Char(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date()
    is_current = fields.Boolean(compute="_check_end_date", store=True)

    @api.depends("end_date", "is_current")
    def _check_end_date(self):
        for record in self:
            record.is_current = not record.end_date