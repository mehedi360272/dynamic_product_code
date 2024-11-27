from odoo import models, fields, api
from odoo.exceptions import UserError

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
            if not record.categ_id:
                raise UserError("Please assign a category to the product before generating the product code.")
            if not record.categ_id.prefix:
                raise UserError(
                    f"The category '{record.categ_id.name}' does not have a prefix. Please set a prefix for this category.")

            sequence = self.env['ir.sequence'].next_by_code('product.code.sequence') or '0001'
            record.default_code = f"{record.categ_id.prefix}-{sequence}"
