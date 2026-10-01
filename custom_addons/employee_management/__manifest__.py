{
    'name': 'Employee Management',
    'version': '1.0.0',
    'summary': 'Employee management system',
    'description': """
        Custom employee management system.

        Includes:
        - Employees
        - Departments
        - Education
        - Positions
        - Attendance
        - Payroll
        - Traits
    """,
    'author': 'Reigani',
    'category': 'Human Resources',
    'license': 'LGPL-3',

    'depends': [
        'base',
    ],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'views/payroll_views.xml',
        'views/employee_views.xml',
        'views/department_views.xml',
        'views/education_views.xml',
        'views/position_views.xml',
        'views/attendance_views.xml',
        'views/trait_views.xml',
        'views/menus.xml',
    ],

    'demo': [
        'demo/demo_data.xml',
    ],

    'installable': True,
    'application': True,
}