from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import qrcode
from io import BytesIO

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char(string="Product Code", readonly=True)

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

    def action_generate_and_download_qr_code(self):
        if not self.default_code or not self.uom_id:
            raise UserError("Product must have a code and unit of measure to generate a QR code.")

        # Generate QR Code Data
        qr_data = f"Product Name: {self.name}\nProduct Code: {self.default_code}\nUnit of Measure: {self.uom_id.name}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create QR Code Image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        buffer.seek(0)
        qr_code_data = buffer.read()

        # Encode and Return File Data
        filename = f"{self.default_code or 'product'}_qr_code.png"
        return {
            'type': 'ir.actions.act_url',
            'url': f"/generate_qr_code/download/{self.id}",
            'target': 'self',
        }
