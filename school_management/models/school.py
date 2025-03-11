# -*- encoding: utf-8 -*-
from docutils.nodes import table

from odoo import models, fields

class SchoolDetails(models.Model):
    _name = "school.details"
    _description = "School Details"

    name = fields.Char(string="Name")
    number = fields.Integer(string="Number")
    partner_id = fields.Many2one('res.partner', string="Partner")
    student_ids = fields.One2many('student.details', 'school_id', string='Students')
    book_ids = fields.One2many('books.book', 'school_id', string='Books')
    product_ids = fields.Many2many('product.product', 'rel_school_product', column1='school_id', column2='product_id', string='Products')
    service_product_ids = fields.Many2many('product.product', 'rel_service_school_product', column1="school_id", column2="product_id", domain=[('type', '=', 'service')])
    opening_date = fields.Date(string="Opening Date")

    def action_open_school_wizard(self):
        view_id = self.env.ref('school_management.school_opening_wizard_wizard').id
        print("view_id",view_id)
        return {
            'name': 'Opening Date',
            'view_mode': 'form',
            'res_model': 'school.opening.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }