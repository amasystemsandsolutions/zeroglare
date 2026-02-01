from odoo import models, fields


class AMACRMShippingMode(models.Model):
    _name = "shipping.mode"
    _inherit = ['mail.thread.main.attachment', 'mail.activity.mixin']
    _description = "Shipping Mode"

    name = fields.Char(string="Name")