import os
from datetime import datetime
import cv2
import numpy as np
from pyzbar.pyzbar import decode


class CameraStreamingWidget:
    def __init__(self):
        self.camera = cv2.VideoCapture(int(os.environ.get('CAMERA',cv2.CAP_DSHOW)))
        self.media_path = os.path.join(os.getcwd(), "media", "images")
        # crear la carpeta "media/images" si no existe
        if not self.media_path:
            os.mkdir(self.media_path)
    
    def get_frames(self):
        while True:
            # Captura cuadro por cuadro
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                
                # Agrega texto encima del código de barras si hay un código de barras en la transmisión usando opencv
                # convertir el marco de la cámara en una matriz numpy
                color_image = np.asanyarray(frame)

                # decodificar matriz numpy para verificar si hay un código de barras en color_image
                # puede agregar una verificación personalizada aquí para verificar si el código qr tiene la información 
                # de identificación correcta
                if decode(color_image):
                    for barcode in decode(color_image):
                        barcode_data = (barcode.data).decode('utf-8')
                        # si existen datos de código de barras
                        if barcode_data:                            
                            # guarda el archivo como PNG si se detecta un código QR
                            today = str(datetime.now().strftime("%d-%m-%y"))
                            image = os.path.join(self.media_path, f"img_{today}.png")
                            cv2.imwrite(image, frame)
                            
                            # imprimir información para fines de depuración
                            print('-'*50)
                            print('Guardando imagen...')
                            print('-'*50)
                            print(f'Guardado como: {image}')
                            print('-'*50)
                            
                            pts = np.array([barcode.polygon], np.int32)
                            pts = pts.reshape((-1,1,2))
                            # dibujar polilíneas en el código de barras
                            cv2.polylines(
                                img=color_image,
                                pts=[pts],
                                isClosed=True,
                                color=(0,255,0),
                                thickness=3
                            )
                            pts2 = barcode.rect
                            # poner texto encima de polilíneas
                            barcode_frame = cv2.putText(
                                img=color_image,
                                text=barcode_data,
                                org=(pts2[0], pts2[1]),
                                fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                                fontScale=0.9,
                                color=(0,0,255),
                                thickness=2
                            )
                            # codifica el nuevo barcode_frame  que tiene polilíneas y texto de datos de código de barras
                            _, buffer_ = cv2.imencode('.jpg', barcode_frame)
                            # convierte barcode_frame a bytes
                            barcode_frame = buffer_.tobytes()
                            # flujo de salida de rendimiento con polilíneas y texto de datos de código de barras
                            yield (b'--frame\r\n'
                                   b'Content-Type: image/jpeg\r\n\r\n' + barcode_frame + b'\r\n\r\n')
                # de lo contrario, produzca el flujo de cámara normal
                else:
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
