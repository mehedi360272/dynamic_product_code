from odoo import http
from odoo.http import request
import qrcode
from io import BytesIO


class ProductQRCodeController(http.Controller):

    @http.route('/generate_qr_code/download/<int:product_id>', type='http', auth="user", csrf=False)
    def download_qr_code(self, product_id):
        # Fetch the product based on product_id
        product = request.env['product.template'].browse(product_id)

        if not product.exists():
            return request.not_found()  # If the product doesn't exist, return a 404

        # Prepare the QR code data: Product Name, Product Code, and UOM
        qr_data = f"Product Name: {product.name}\nProduct Code: {product.default_code}\nUnit of Measure: {product.uom_id.name if product.uom_id else 'N/A'}"

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,  # Version 1 means a small QR code
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
            box_size=10,  # Size of each box in the QR code
            border=4  # Border size
        )

        qr.add_data(qr_data)  # Add product data to the QR code
        qr.make(fit=True)  # Adjust QR code size to fit the data

        # Create the QR code image
        qr_image = qr.make_image(fill='black', back_color='white')

        # Save the image to a buffer in PNG format
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)  # Reset the buffer's position to the beginning

        # Generate the filename using Product Name and Product Code
        product_name = product.name.replace(" ", "_")  # Replace spaces with underscores
        product_code = product.default_code or "unknown_code"
        filename = f"{product_name}_{product_code}_qr_code.png"

        # Return the QR code as a downloadable file
        return http.send_file(buffer, filename=filename, as_attachment=True)
