from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Department(models.Model):
    _name = "custom.department"
    _description = "Department"
    _order = "name"
    _rec_name = "name"

    parent_id = fields.Many2one("custom.department", string="Parent Department", ondelete="restrict")
    child_ids = fields.One2many("custom.department", "parent_id", string="Child Departments")
    employee_ids = fields.One2many("custom.employee", "department_id")
    manager_id = fields.Many2one("custom.employee", string="Manager")
    
    name = fields.Char(required=True)

    _sql_constraints = [
        (
            "manager_unique",
            "UNIQUE(manager_id)",
            "The same Employee cannot be the manager of more than one Department."
        )
    ]

    @api.constrains("parent_id")
    def _check_parent_id(self):
        for department in self:
            parent = department.parent_id

            while parent:
                if parent == department:
                    raise ValidationError(
                        "A department cannot be its own parent."
                    )
                parent = parent.parent_id

    # @api.constrains("child_ids")
    # def _check_child_ids(self):
    #     for department in self:
    #         if department in department.child_ids:
    #             raise ValidationError("Cannot Add Self As A Child Department!")
