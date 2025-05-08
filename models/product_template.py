from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import qrcode
from io import BytesIO

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char(string="Product Code", readonly=True)
    qr_code_image = fields.Image("QR Code Image", readonly=True)

    @api.model
    def create(self, vals):
        if 'categ_id' in vals:
            category = self.env['product.category'].browse(vals['categ_id'])
            if category.prefix:
                sequence = self.env['ir.sequence'].next_by_code('product.code.sequence') or '0000'
                vals['default_code'] = f"{category.prefix}-{sequence}"
        return super(ProductTemplate, self).create(vals)

    def action_generate_product_code(self):
        for record in self:
            if record.default_code:
                raise UserError("The product code has already been generated and cannot be changed.")
            if not record.categ_id:
                raise UserError("Please assign a category to the product before generating the product code.")
            if not record.categ_id.prefix:
                raise UserError(
                    f"The category '{record.categ_id.name}' does not have a prefix. Please set a prefix for this category.")
            sequence = self.env['ir.sequence'].next_by_code('product.code.sequence') or '0001'
            record.default_code = f"{record.categ_id.prefix}-{sequence}"

    def action_generate_and_store_qr_code(self):
        for record in self:
            # if not record.default_code or not record.uom_id:
            #     raise UserError("Product must have a code and unit of measure to generate a QR code.")

            qr_data = f"Product Name: {record.name}\nProduct Code: {record.default_code}\nUnit of Measure: {record.uom_id.name}"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)

            qr_image = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")
            record.qr_code_image = base64.b64encode(buffer.getvalue())
