from odoo import http
from odoo.http import request
import qrcode
from io import BytesIO

class ProductQRCodeController(http.Controller):

    @http.route('/generate_qr_code/download/<int:product_id>', type='http', auth="user", csrf=False)
    def download_qr_code(self, product_id):
        # Fetch the product
        product = request.env['product.template'].browse(product_id)
        if not product.exists():
            return request.not_found()

        # Generate QR Code Data
        qr_data = f"Product Name: {product.name}\nProduct Code: {product.default_code}\nUnit of Measure: {product.uom_id.name}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create QR Code Image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Set Filename
        filename = f"{product.default_code or 'product'}_qr_code.png"

        # Return the QR Code as a downloadable file
        return http.send_file(buffer, filename=filename, as_attachment=True)
