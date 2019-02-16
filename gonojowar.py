import os
import subprocess
import cv2
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def predict():
    os.chdir('/home/abrar11648/tensorflow-for-poets-2')
    b = subprocess.Popen("python -m scripts.label_image \
      --graph=tf_files/retrained_graph.pb  \
      --image=tf_files/frame.jpg", shell=True, stdout=subprocess.PIPE).stdout

    terminalOutput = str(b.read())

    return terminalOutput


def genResult(terminalOutput):
    terminalOutput = str(terminalOutput)
    terminalOutput = terminalOutput[41:-3]

    split_list = terminalOutput.split('n')
    result = dict()

    for i in split_list:
        i_list = i.split(' ')
        key = i_list[0]
        i_list = i_list[1].split('=')
        value = i_list[1][:-2]
        value = float(value)

        result.update({key: value})

    return result


def sub_one():
    i = 0
    file = open("dataText", "w")

    while (True):

        '''file.seek(0)
        file.truncate()
        file.flush()'''

        terminalOutput = predict()
        result = genResult(terminalOutput)
        max_key = max(result, key=result.get)
        max_value = result.get(max_key)

        if max_value > 0.94:
            i = i + 1
            resultString = '#'+ str(i) + '<<' + max_key + '>>' + '[confidenceLevel:' + str(max_value) + ']    ' + '\n'

            file.write(resultString)
            # print(max_key)
            file.flush()

        # time.sleep(1)


def sub_two():
    file = open('dataText', 'r')
    file_save = open('saveText', 'w')

    while (True):
        text = file.read()
        file_save.write(text)
        file_save.flush()

        # line = subprocess.check_output(['tail', '-1', 'dataText'])
        # print(text)

        print("sub_two running")
        time.sleep(3.5)


def sub_three(mirror=False):
    scale = 10

    cam = cv2.VideoCapture(0)
    timeout = 10

    while (True):

        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        # get the webcam size
        height, width, channels = img.shape

        # prepare the crop
        centerX, centerY = int(height / 2), int(width / 2)
        radiusX, radiusY = int(scale * height / 100), int(scale * width / 100)

        minX, maxX = centerX - radiusX, centerX + radiusX
        minY, maxY = centerY - radiusY, centerY + radiusY

        cropped = img[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (width, height))

        cv2.imshow('Tracker Cam', resized_cropped)

        cv2.imwrite("/home/abrar11648/tensorflow-for-poets-2/tf_files/frame.jpg", resized_cropped)

        # time.sleep(1)

        timeout = timeout - 1

        if cv2.waitKey(1) == 27:
            break  # esc to quit

        # add + or - 5 % to zoom

        if cv2.waitKey(1) == 0:
            scale += 5  # +5

        if cv2.waitKey(1) == 1:
            scale = 5  # +5

        '''if timeout == 0 or timeout < 0:
          break
    
        else:
    
          print(timeout)'''

    cv2.destroyAllWindows()


def clearFiles():
    fileData = open('dataText', 'w').close()
    fileSave = open('saveText', 'w').close()


def classifier():

    clearFiles()

    executor = ThreadPoolExecutor(max_workers=2)

    b = executor.submit(sub_one)
    a = executor.submit(sub_three(mirror=True))


def run():
    clearFiles()

    thread_classifier = threading.Thread(target=classifier)
    thread_classifier.start()
    sub_two()





