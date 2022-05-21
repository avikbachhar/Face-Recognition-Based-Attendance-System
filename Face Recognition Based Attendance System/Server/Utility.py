import cv2
import face_recognition
def findEncodings(images):
    i=0
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        print("Encoded "+str(i))
        print(encode.dtype)
        #db_connect_photoencoding(studentrolls[i],encode.tobytes())
        i+=1
    return encodeList

def findEncodings(img):
    encode = face_recognition.face_encodings(img)[0]
    encoded_image = encode.tobytes()
    return encoded_image