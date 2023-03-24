import cv2

def return_camera_indexes():
     #comprueba los primeros 10 índices
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

print('Índice de cámara disponibles:', return_camera_indexes())