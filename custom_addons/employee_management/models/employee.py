from odoo import models, fields, api

class Employee(models.Model):
    _name = "custom.employee"
    _description = "Employee"
    _order = "last_name, first_name"
    _rec_name = "name"

    user_id = fields.Many2one("res.users", required=True)
    department_id = fields.Many2one("custom.department", string="Department", required=True)
    citizenship_id = fields.Many2one("res.country", string="Citizenship")
    trait_ids = fields.Many2many("custom.trait", "employee_trait_rel", "employee_id", "trait_id", string="Traits")
    education_ids = fields.One2many("custom.education", "employee_id", string="Educations")
    position_ids = fields.One2many("custom.position", "employee_id", string="Positions")
    attendance_ids = fields.One2many("custom.attendance", "employee_id", string="Attendances")
    payroll_ids = fields.One2many("custom.payroll", "employee_id", string="Payrolls")

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    name = fields.Char(compute="_compute_name", store=False)
    personal_id = fields.Char(required=True, string="Personal ID")
    birth_date = fields.Date(required=True)
    is_department_admin = fields.Boolean(default=False)
    phone_number = fields.Char()
    salary = fields.Float()
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
            ("not", "Prefer Not To Say")
        ],
        required=True
    )
    photo = fields.Image(string="Photo")

    _sql_constraints = [
        (
            "personal_id_unique",
            "UNIQUE(personal_id)",
            "Personal ID must be unique."
        ),
        (
            "user_unique",
            "UNIQUE(user_id)",
            "User must be uique."
        )
    ]

    @api.depends("first_name", "last_name")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("user_id"):
                name = f"{vals.get('first_name', '')} {vals.get('last_name', '')}".strip()

                user = self.env["res.users"].create({
                    "name": name,
                    "login": vals["personal_id"],
                    "password": "demo123",
                    "group_ids": [
                        (4, self.env.ref(
                            "employee_management.group_employee_own"
                        ).id)
                    ],
                })

                vals["user_id"] = user.id

        return super().create(vals_list)