from odoo import models, fields, api
from odoo.exceptions import UserError

BLOOD_GROUP = [('A+', 'A+ve'),
                ('B+', 'B+ve'),
                ('O+', 'O+ve'),
                ('AB+', 'AB+ve'),
                ('A-', 'A-ve'),
                ('B-', 'B-ve'),
                ('O-', 'O-ve'),
                ('AB-', 'AB-ve')]


class ResPatient(models.Model):
    _name = "res.patient"
    _description = "Patient"

    patient_code = fields.Char(string="Patient ID")
    name = fields.Char(string="Name", required=True)
    blood_group = fields.Selection(BLOOD_GROUP,
                                   string="Blood Group",  required=True)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Char(string="Age")
    previous_diseases = fields.Text(string="Previous Diseases")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile")

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResPatient, self).create(vals_list)
        for record in res:
            record.patient_code = self.env['ir.sequence'].next_by_code('res.patient')
        return res

    def write(self, vals):
        res = super(ResPatient, self).write(vals)
        # if 'phone' in vals:
        #    if len(vals.get('phone')) < 10:
        #        raise UserError("Phone number should be minimum 10 digits")
        return res

    @api.constrains('phone')
    def check_phone(self):
        for record in self:
            if record.phone and len(record.phone) < 10:
                raise UserError("Phone number should be minimum 10 digits")

            # check no duplicate phone number
            patient_ids = self.env['res.patient'].search_count([('phone', '=', record.phone),('id', '!=', record.id)])
            if patient_ids:
                raise UserError("Phone number already exists")

    def action_open_appointments(self):
        view_id = self.env.ref('bista_hms.hms_appointment_form_view').id

        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.appointment',
            'view_id': view_id,
            'target': 'current',
            'context': {'default_patient_id': self.id, 'child': True}
        }





