from tempfile import TemporaryFile
import base64
import openpyxl

from odoo import models, fields, _
from odoo.exceptions import UserError


class ImportEstimationWizard(models.TransientModel):
    _name = "import.estimation.wizard"
    _description = "Import Estimation Wizard"

    upload_file = fields.Binary(string="Upload Excel File", required=True)
    filename = fields.Char(string="File Name")

    def action_import_file(self):
        if not self.upload_file:
            raise UserError(_("Please upload an Excel file."))

        file_data = base64.b64decode(self.upload_file)
        fileobj = TemporaryFile('wb+')
        fileobj.write(file_data)
        fileobj.seek(0)

        workbook = openpyxl.load_workbook(fileobj, data_only=True)
        sheet = workbook.active

        current_estimation = False

        for row_no, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            (estimation_name, currency_name, shipping_mode_name, description, qty, unit_name, cost) = row

            if estimation_name:
                currency = self.env['res.currency'].search([('name', '=', currency_name)], limit=1)
                if not currency:
                    raise UserError(_(f"Row {row_no}: Currency not found ({currency_name})"))

                shipping_mode = self.env['shipping.mode'].search([('name', '=', shipping_mode_name)], limit=1)
                if not shipping_mode:
                    raise UserError(_(f"Row {row_no}: Shipping Mode not found ({shipping_mode_name})"))

                current_estimation = self.env['crm.estimation'].create({
                    'name': estimation_name,
                    'currency_id': currency.id,
                    'shipping_mode_id': shipping_mode.id,
                })

            if not current_estimation:
                raise UserError(_(f"Row {row_no}: Estimation not defined"))

            if description:
                unit = self.env['uom.uom'].search([('name', '=', unit_name)], limit=1)
                if not unit:
                    raise UserError(_(f"Row {row_no}: UOM not found ({unit_name})"))

                self.env['bill.of.quantities'].create({
                    'estimation_id': current_estimation.id,
                    'description': description,
                    'qty': qty or 0.0,
                    'unit_id': unit.id,
                    'cost': cost or 0.0,
                })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
