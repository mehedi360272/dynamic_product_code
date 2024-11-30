{
    'name': 'Dynamic Product Code and QR code',
    'version': '1.0',
    'summary': 'Automatically generates product codes based on category prefixes.',
    'description': """
        Simplifies the process of setting product codes based on category prefixes. 
        Automates prefix generation to ensure consistent and error-free product codes.
    """,
    'author': 'Khondokar Md. Mehedi Hasan',
    'website': 'https://www.github.com/mehedi360272',
    'depends': ['product'],
    'data': [
        'data/product_sequence_data.xml',
        'views/product_category_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
}
