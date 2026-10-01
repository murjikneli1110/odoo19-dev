from odoo import models, fields, api

class Trait(models.Model):
    _name = "custom.trait"
    _description = "Trait"
    _rec_name = "name"

    employee_ids = fields.Many2many("custom.employee", "employee_trait_rel", "trait_id", "employee_id", string="Employees")
    
    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "name_unique",
            "UNIQUE(name)",
            "Trait Names Should Be Unique!"
        )
    ]