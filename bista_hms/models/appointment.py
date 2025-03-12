from odoo import api, fields, models

class HmsAppointment(models.Model):
    _name = "hms.appointment"
    _description = "Appointment"
    _rec_name = "patient_id"

    name = fields.Char(string="Appointment ID", copy=False, readonly=True, index=True, default="New")
    patient_id = fields.Many2one("res.patient", string="Patient", required=True)
    appointment_date = fields.Datetime(string="Date", required=True)
    appointment_reason = fields.Text(string="Reason")
    state = fields.Selection([('draft', 'Draft'),
                                           ('confirm', 'Confirm'),
                                           ('waiting', 'Waiting'),
                                           ('in_consultation', 'In Consultation'),
                                           ('done', 'Done'),
                                           ('cancel', 'Cancel')],
                                          string="Status", default='draft')


