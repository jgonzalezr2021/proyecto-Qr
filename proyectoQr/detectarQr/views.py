from django.shortcuts import render
import os
import time
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse, StreamingHttpResponse
from PIL import Image
from pyzbar.pyzbar import decode
from utils.camera_streaming_widget import CameraStreamingWidget
from django.shortcuts import HttpResponse


def is_ajax(request):#definicion de metodo de uso Ajax
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
# alimentacion de la camara
def camera_feed(request):
    stream = CameraStreamingWidget()
    frames = stream.get_frames()

    ## si se envía una solicitud ajax
    if is_ajax(request):
        print('Ajax request received')
        time_stamp = str(datetime.now().strftime("%d-%m-%y"))
        image = os.path.join(os.getcwd(), "media",
                             "images", f"img_{time_stamp}.png")
        if os.path.exists(image):
            # abrir imagen si existe
            im = Image.open(image)
            # decodificar código de barras
            if decode(im):
                for barcode in decode(im):
                    barcode_data = (barcode.data).decode('utf-8')
                    file_saved_at = time.ctime(os.path.getmtime(image))
                    # devuelve el código de barras decodificado como respuesta json
                    return JsonResponse(data={'barcode_data': barcode_data, 'file_saved_at': file_saved_at})
            else:
                return JsonResponse(data={'barcode_data': None})
        else:
            return JsonResponse(data={'barcode_data': None})
    # de lo contrario, transmita los fotogramas desde la alimentación de la cámara definida en camera_feed
    else:
        return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')

def detect(request):
    stream = CameraStreamingWidget()
    success, frame = stream.camera.read()
    if success:
        status = True
    else:
        status = False
    
    return render(request, 'detectarQr/detectar.html', context={'cam_status': status})
