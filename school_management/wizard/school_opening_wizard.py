from odoo import models, fields


class SchoolOpeningWizard(models.TransientModel):
    _name = 'school.opening.wizard'
    _description = 'School Opening Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date")



