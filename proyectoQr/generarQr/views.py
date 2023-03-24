import qrcode
import barcode
from django.utils.encoding import smart_str
from django.shortcuts import render
from barcode.writer import ImageWriter

from django.http import HttpResponse
from .import views
def generate_file(barcode_file):
    # output = HttpResponse(content_type="image/jpeg")
    output = HttpResponse(content_type="application/force-download")
    barcode_file.save(output, "JPEG")
    output['Content-Disposition'] = 'attachment; filename=%s' % smart_str('barcode.png')
    output['X-Sendfile'] = smart_str('barcode.png')
    return output



    
#generacion del Qr con opcion de poder elegir el tipo

def generate(request):
    context = {
        'barcode_types': [b for b in barcode.PROVIDED_BARCODES if str(b).startswith('code')] + ['qrcode']
    }

    if request.method == 'POST':
        b_type = request.POST['typeOfBarcode']
        b_data = request.POST['barcodeData']

        if b_type == 'qrcode':
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )
            qr.add_data(b_data)
            qr.make(fit=True)
            qr_file = qr.make_image(fill_color="black", back_color="white") # renderizar imagen qr
            return generate_file(qr_file) # generamos el archivo

        else:        
            bar = barcode.get_barcode(name=b_type, code=b_data, writer=ImageWriter())
            barcode_file = bar.render() # crea un objeto de imagen de clase PIL
            return generate_file(barcode_file) # genera el archivo
    else:
        return render(request, 'generarQr/generar.html', context=context)
