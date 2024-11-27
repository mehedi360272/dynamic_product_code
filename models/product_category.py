from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    prefix = fields.Char(string="Category Prefix", help="Prefix used for product codes in this category")
