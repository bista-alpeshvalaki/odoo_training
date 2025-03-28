from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HmsPrescription(models.Model):
    _name = "hms.prescription"

    patient_id = fields.Many2one("res.patient", string="Patient", required=True, ondelete="restrict")
    date = fields.Date(string="Date", required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft')
    prescription_lines = fields.One2many("prescription.line",
                                         "prescription_id", string="Prescription Lines")
    total_amount = fields.Float(compute='_compute_total_amount', string="Total Amount")
    invoice_ids = fields.Many2many("account.move", string="Invoices")

    @api.depends('prescription_lines.total')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.prescription_lines.mapped('total'))

    def action_create_invoice(self):
        if not self.prescription_lines:
            raise ValidationError("Please add prescription lines before creating an invoice.")
        # if not self.state == 'confirm':
        #     raise ValidationError("Prescription must be confirmed before creating an invoice.")

        vals = self.prepare_invoice_vals()
        # invoice_id = self.env['account.move'].create(vals)

        # vals['invoice_line_ids'] = line_vals

        invoice_id = self.env['account.move'].create(vals)

        line_vals_list = self.prepare_invoice_line_vals(invoice_id)

        line_ids  = self.env['account.move.line'].create(line_vals_list)

        self.invoice_ids = [(6, 0 , [invoice_id.id])]

        # self.invoice_ids = [(3, 25)]
        print("move_line_ids==========",invoice_id)


    def prepare_invoice_vals(self):
        values = {
            'move_type': 'out_invoice',
            'partner_id': 7, # self.patient_id.partner_id.id,
            'partner_shipping_id': 7, # # self.patient_id.partner_id.id,
            'company_id': self.env.user.company_id.id,
            'user_id': self.env.user.id,
            'invoice_date': self.date,
        }
        return values

    def prepare_invoice_line_vals(self, invoice_id):
        line_vals_list = []
        for line in self.prescription_lines:
            line_vals = {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'discount': 0.0,
                'move_id': invoice_id.id,
            }
            line_vals_list.append(line_vals)
            # line_vals_list.append((0, 0, line_vals))
        return line_vals_list

class PrescriptionLine(models.Model):
    _name = "prescription.line"

    prescription_id = fields.Many2one("hms.prescription", string="Prescription", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Medicine", required=True)
    quantity = fields.Integer(string="Quantity", required=True)
    price_unit = fields.Float(string="Price Unit", required=True)
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.price_unit = self.product_id.lst_price

    @api.depends('quantity', 'price_unit')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.price_unit