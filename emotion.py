import cv2
import requests
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "xyz.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()




auth_headers = {
    'app_id': 'b9b48835',
    'app_key': '9d83ecd2df2d2ac31206265f5f5e3584'
}

url = 'https://api.kairos.com/v2/media'
files = {
    'source': open('xyz.png')
}
data = {
    'timeout': 60
}


response = requests.post(url, files=files, data=data, headers=auth_headers)

f = (response.json())
print(f)
'''

h = f['frames'][0]['people']
if (h == []):
	print("face can't recognize")
	exit(0)
else :
	g= f['frames'][0]['people'][0]['emotions']
	k = [(value,key) for key,value in g.items()]
	l = max(k)[1]
	
	print(f)
	print(g)
	print(l)
'''
