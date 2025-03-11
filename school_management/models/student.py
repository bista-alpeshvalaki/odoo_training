# -*- encoding: utf-8 -*-

from odoo import models, fields

class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Student Details"

    name = fields.Char(string="Name")
    roll_number = fields.Integer(string="Roll Number")
    school_id = fields.Many2one('school.details', string="School")