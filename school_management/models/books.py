from odoo import models, fields

class BooksBook(models.Model):
    _name = 'books.book'

    school_id = fields.Many2one('school.details', string='School', required=True, ondelete='cascade')
    name = fields.Char(string='Book Name', required=True)
    qty = fields.Integer(string='Quantity', required=True)