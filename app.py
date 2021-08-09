from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import sys
import math
import pytesseract

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def preprocess(img):
    img_gray=img
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 50, 50)
    kernel = np.ones((3, 3))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
    img_erode = cv2.erode(img_dilate, kernel, iterations=1)
    return img_erode

def find_tip(points, convex_hull):
    length = len(points)
    indices = np.setdiff1d(range(length), convex_hull)

    for i in range(2):
        j = indices[i] + 2
        if j > length - 1:
            j = length - j
        if np.all(points[j] == points[indices[i - 1] - 2]):
            return tuple(points[j])

def find_beg(points,arrow_tip):
    length = len(points)
    biggest = 0
    for i in range(length):
        if distance(tuple(points[i]),tuple(arrow_tip)) > biggest :
            biggest = distance(points[i],arrow_tip)
            biggestt = points[i]
    return tuple(biggestt)

def find_tips(points):
    length = len(points)
    biggest = 0
    for i in range(length):
        for j in range(length):
            if distance(tuple(points[i]),tuple(points[j])) > biggest :
                biggest = distance(points[i],points[j])
                point1 = points[i]
                point2 = points[j]
                index1=i
                index2=j
    biggest2=0
    for i in range(length):
        for j in range(length):
            if i!=index1 and i!=index2 and j!=index1 and j!=index2 and i!=distance(tuple(points[i]),tuple(points[j])) > biggest2 :
                biggest2 = distance(points[i],points[j])
                point3 = points[i]
                point4 = points[j]
                index3 = i
                index4 = j
    smallest1=99999
    for i in range(length):
        if i!=index1 and i!=index2 and i!=index3 and i!=index4 and distance(points[i],point1) < smallest1 :
            smallest1 = distance(points[i],point1)
    smallest2=99999
    for i in range(length):
        if i!=index1 and i!=index2 and i!=index3 and i!=index4 and distance(points[i],point2) < smallest2 :
            smallest2 = distance(points[i],point2)
    if smallest1 < smallest2:
        point5=point1
        point1=point2
        point2=point5
    smallest1=99999
    for i in range(length):
        if i!=index1 and i!=index2 and i!=index3 and i!=index4 and distance(points[i],point3) < smallest1 :
            smallest1 = distance(points[i],point3)
    smallest2=99999
    for i in range(length):
        if i!=index1 and i!=index2 and i!=index3 and i!=index4 and distance(points[i],point4) < smallest2 :
            smallest2 = distance(points[i],point4)
    if smallest1 < smallest2:
        point5=point3
        point3=point4
        point4=point5
    tup=[0,0,0,0]
    tup[0]=tuple(point1)
    tup[1]=tuple(point2)
    tup[2]=tuple(point3)        
    tup[3]=tuple(point4)
    return tup

def analyzetxt(txt):
    print(len(txt))
    for i in range(len(txt)):
        print('index '+str(i)+' is '+txt[i]+' with ASCII value ' + str(ord(txt[i])))

def processtxt(txt):
    txt2=''
    for i in range(len(txt)):
        if ord(txt[i]) > 47 and ord(txt[i]) < 123:
            txt2=txt2+txt[i]
    if len(txt2)==2 and txt2[0].isupper() and txt2[1]==txt[0].lower() :
            txt2=txt2[0:1]
    return txt2

class edge:
    def __init__(self,countour,beg_point,edge_tip):
        self.cnt = countour
        self.beg = beg_point
        self.arr = edge_tip
    def highlight(self,img):
        cv2.drawContours(img, self.cnt, -1, (255, 0, 0), 2)
        cv2.circle(img, self.arr, 5, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, self.beg, 5, (0, 0, 255), cv2.FILLED)
    def getBeg(self):
        tup=[0,0]
        tup[0] = int(self.beg[0])
        tup[1] = int(self.beg[1])
        return tup
    def getArr(self):
        tup=[0,0]
        tup[0] = int(self.arr[0])
        tup[1] = int(self.arr[1])
        return tup

class node:
    def __init__(self,countour,name):
        self.cnt = countour
        self.name = name
        
    def highlight(self,img):
        cv2.drawContours(img, self.cnt, -1, (75,166,14), 5)
        print('Highlighting node '+ self.name)

def main(path_to_image="static/sample_inputs/graph_def.png"):
    im_in = cv2.imread(path_to_image,cv2.IMREAD_GRAYSCALE) #plain image
    output = im_in
    th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV) #plain invert
    im_floodfill = im_th.copy() #get rid of arrows, fill nodes with black
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_out = im_th | im_floodfill_inv

    kernelSize = [9,9]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
    opening = cv2.morphologyEx(im_out, cv2.MORPH_OPEN, kernel)
    sub = cv2.subtract(im_out,opening)
    exar = cv2.bitwise_not(sub)
    exno = cv2.add(im_in,sub)

    listEdges=[]
    listNodes=[]

    contours, hierarchy = cv2.findContours(preprocess(exar), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.025 * peri, True)
        hull = cv2.convexHull(approx, returnPoints=False)
        sides = len(hull)
        if 6 > sides > 3 and sides + 2 == len(approx):
            arrow_tip = find_tip(approx[:,0,:], hull.squeeze())
            if arrow_tip:
                beg_point = find_beg(approx[:,0,:], arrow_tip)
                listEdges.append(edge(cnt,beg_point,arrow_tip))
        elif sides == 4 and len(approx) == 8:
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
            tips = find_tips(approx[:,0,:])
            listEdges.append(edge(cnt,tips[0],tips[1]))
            listEdges.append(edge(cnt,tips[2],tips[3]))

    contours, hierarchy = cv2.findContours(preprocess(exno), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x=x-10
        y=y-10
        w=w+20
        h=h+20
        cropped = exno[y:y + h, x:x + w]
        gray = cropped
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 0.9, 20, param1 = 50, param2 = 30, minRadius = 30, maxRadius = 155)
        if circles is not None:
            x=x+31
            y=y+33
            w=w-60
            h=h-63
            cropped = exno[y:y + h, x:x + w]
            txt = pytesseract.image_to_string(cropped,config='--psm 9')
            txt=processtxt(txt)
            listNodes.append(node(cnt,txt))
    output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
    print('Found '+str(len(listEdges))+' arrows')
    for obj in listEdges:
        obj.highlight(output)
        nearest_beg=99999
        nearest_tip=99999
        for node_ in listNodes:
            dist = cv2.pointPolygonTest(node_.cnt,obj.getBeg(),True) * -1
            if dist<nearest_beg:
                nearest_beg = dist
                beg_node=node_
        #print('Distance from beg to '+ node_.name + ' is ' + str(dist))
            dist2 = cv2.pointPolygonTest(node_.cnt,obj.getArr(),True) * -1
            if dist2 < nearest_tip:
                nearest_tip = dist2
                tip_node=node_
            #print('Distance from arr to '+ node_.name + ' is ' + str(dist2))
        if len(listNodes)>0 :
            print('Found edge connecting '+ beg_node.name + ' to ' + tip_node.name)
    
    for obj in listNodes:
        obj.highlight(output)
        #cv2.imshow("Image", output)
    directory = r'static/downloads'
    os.chdir(directory)
    cv2.imwrite("out.png",output)
    os.chdir('../..')


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADED_FILES_DEST'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
firstTime=True
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    global firstTime
    if 'file' not in request.files:
        flash('No file received')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        if 'hiddenImg' in request.form and request.form['hiddenImg']!="nothing":
            main('static/sample_inputs/' + request.form['hiddenImg'])
            return render_template('index.html', filename=request.form['hiddenImg'])
        else:
            flash('Unknown Error')
            return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print('Entering file handling routine for '+filename)
        if firstTime == True:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            firstTime = False
        else: 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and analyzed')
        main('static/uploads/' + filename)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/display2/<filename>')
def display_image2(filename="out.png"): #filename="out.png"
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='downloads/' + 'out.png'), code=301)
 
if __name__ == "__main__":
    app.run()


