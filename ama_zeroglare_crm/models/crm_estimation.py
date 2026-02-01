from odoo import models, fields, api


class AMACRMEstimation(models.Model):
    _name = "crm.estimation"
    _inherit = ['mail.thread.main.attachment', 'mail.activity.mixin']
    _description = "Estimation"

    name = fields.Char(string="Name", copy=False)
    currency_id = fields.Many2one("res.currency", string="Quotation Currency")
    shipping_mode_id = fields.Many2one("shipping.mode", string="Mode of Shipping")
    boq_ids = fields.One2many("bill.of.quantities", 'estimation_id', string="Bill of Quantities")


class AMACRMBillOfQuantities(models.Model):
    _name = "bill.of.quantities"
    _inherit = ['mail.thread.main.attachment', 'mail.activity.mixin']
    _description = "Bill of Quantities"

    estimation_id = fields.Many2one("crm.estimation", string="Estimation")
    description = fields.Text(string="Description")
    qty = fields.Float(string="Quantity")
    unit_id = fields.Many2one("uom.uom", string="Unit")
    cost = fields.Float(string="Cost")
    total = fields.Float(string="Total", compute="compute_total")

    @api.depends('qty', 'cost')
    def compute_total(self):
        for rec in self:
            rec.total = 0.00
            if rec.qty and rec.cost:
                rec.total = rec.qty * rec.cost
