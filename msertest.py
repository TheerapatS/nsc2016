import numpy as np
import scipy.ndimage.morphology as m
import cv2


def skeletonize(img):
    h1 = np.array([[0, 0, 0], [0, 1, 0], [1, 1, 1]])
    m1 = np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]])
    h2 = np.array([[0, 0, 0], [1, 1, 0], [0, 1, 0]])
    m2 = np.array([[0, 1, 1], [0, 0, 1], [0, 0, 0]])
    hit_list = []
    miss_list = []
    for k in range(4):
        hit_list.append(np.rot90(h1, k))
        hit_list.append(np.rot90(h2, k))
        miss_list.append(np.rot90(m1, k))
        miss_list.append(np.rot90(m2, k))
    img = img.copy()
    while True:
        last = img
        for hit, miss in zip(hit_list, miss_list):
            hm = m.binary_hit_or_miss(img, hit, miss)
            img = np.logical_and(img, np.logical_not(hm))
        if np.all(img == last):
            break
    return img


def find_skel(img, im, c):
    x = im.shape
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    img = cv2.dilate(img, element, iterations=3)
    skel = skeletonize(img)
    cv2.imshow(str(c), skel.astype(np.uint8) * 255)
    cv2.imwrite("skel_" + str(c) + ".jpg", skel.astype(np.uint8) * 255)
    c += 1
    tempimg = np.zeros((int(x[0] + 2), int(x[1] + 2)), np.uint8)
    for i in range(1, x[0]):
        for j in range(1, x[1]):
            if skel[i - 1][j - 1]:
                tempimg[i][j] = 1
            else:
                tempimg[i][j] = 0
    br_map = np.zeros((int(x[0]), int(x[1])), np.uint8)
    br_list = []
    end_map = np.zeros((int(x[0]), int(x[1])), np.uint8)
    end_list = []
    for i in range(1, x[0]):
        for j in range(1, x[1]):
            if tempimg[i][j] == 1:
                br = tempimg[i - 1][j - 1] + tempimg[i - 1][j] + tempimg[i - 1][j + 1] + tempimg[i][j - 1] + tempimg[i][
                    j + 1] + tempimg[i + 1][j - 1] + tempimg[i + 1][j] + tempimg[i + 1][j + 1]
                if br > 2:
                    br_map[i - 1][j - 1] = 255
                    br_list.append([i - 1, j - 1])
                if br == 1:
                    end_map[i - 1][j - 1] = 255
                    end_list.append([i - 1, j - 1])
    return c, br_map, br_list, end_map, end_list, skel


def im_fill(gray):
    des = gray.copy()
    des_invert = cv2.bitwise_not(gray)
    contour, hier = cv2.findContours(des_invert, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        if cv2.contourArea(cnt) < gray.size * (0.01):
            cv2.drawContours(des, [cnt], 0, 255, -1)
    return des


def get_txt(path):
    img = cv2.imread(path)
    mser = cv2.MSER(9, int(0.000 * img.size / 3), int(0.05 * img.size / 3), 0.1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converting to GrayScale
    regions = mser.detect(gray, None)
    x = img.shape
    im = np.zeros((int(x[0]), int(x[1])), np.uint8)
    for region in regions:
        for i in range(0, len(region)):
            im[region[i][1]][region[i][0]] = 255
    return im


def get_skel(path):
    countwindows = 0;
    img = cv2.imread(path)
    shape = img.shape
    fixed_length = 800.00
    if shape[0] > shape[1]:
        ratio_resize = fixed_length / shape[0]
    else:
        ratio_resize = fixed_length / shape[1]
    height, width = img.shape[:2]
    img = cv2.resize(img, (int(ratio_resize * width), int(ratio_resize * height)))
    mser = cv2.MSER(9, int(0.05 * img.size / 3), int(0.5 * img.size / 3), 0.1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converting to GrayScale
    regions = mser.detect(gray, None)
    area2 = []
    x = img.shape
    im_filled = []
    count_im_isok = []
    for region in regions:
        im = np.zeros((int(x[0]), int(x[1])), np.uint8)
        for i in range(0, len(region)):
            im[region[i][1]][region[i][0]] = 255
        temp = im_fill(im);
        im_filled.append(temp.copy())
        area2.append(cv2.countNonZero(temp))
        contour2, hier2 = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hull2 = cv2.convexHull(contour2[0])
        hull_area2 = cv2.contourArea(hull2)
        if hull_area2 != 0:
            solidity_filled = area2[countwindows] / hull_area2
            white_frame = 0.0
            for j in range(0, x[1] - 1):
                if im_filled[countwindows][0][j] == 255:
                    white_frame += 1
                if im_filled[countwindows][x[0] - 1][j] == 255:
                    white_frame += 1
            for j in range(1, x[0] - 2):
                if im_filled[countwindows][j][0] == 255:
                    white_frame += 1
                if im_filled[countwindows][j][x[1] - 1] == 255:
                    white_frame += 1
            frame = (2 * (x[0] + x[1])) - 4
            percent = (float(white_frame) / frame) * 100.0
            # cv2.imshow(str(countwindows + 100), im_filled[countwindows])
            if solidity_filled < 0.5:
                if percent < 50.0:
                    count_im_isok.append(countwindows)
            countwindows += 1
    temp = []
    ind = -1
    if len(count_im_isok) == 1:
        # cv2.imshow(str(countwindows + 300), im_filled[count_im_isok[0]])
        ind = count_im_isok[0]
    else:
        for i in count_im_isok:
            temp.append(area2[i])
        temp.sort()
        for i in count_im_isok:
            if area2[i] == temp[len(count_im_isok) - 1]:
                ind = i
    if ind != -1:
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 7))
        im_filled[ind] = cv2.dilate(im_filled[ind], element, iterations=1)
        im_filled[ind] = cv2.erode(im_filled[ind], element, iterations=1)

        element = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1))
        im_filled[ind] = cv2.dilate(im_filled[ind], element, iterations=1)
        im_filled[ind] = cv2.erode(im_filled[ind], element, iterations=1)

        element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
        im_filled[ind] = cv2.erode(im_filled[ind], element, iterations=1)
        im_filled[ind] = cv2.dilate(im_filled[ind], element, iterations=1)

        element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
        im_filled[ind] = cv2.erode(im_filled[ind], element, iterations=1)
        im_filled[ind] = cv2.dilate(im_filled[ind], element, iterations=1)

        cv2.imshow(str(countwindows + 300), im_filled[ind])
        cv2.imwrite(str(countwindows + 200)+".jpg", im_filled[ind])
        __1, __2, __3, end_map, end_list, skel = find_skel(im_filled[ind], img, countwindows)
        # cv2.imwrite(str(countwindows + 400)+".jpg", skel)
        return img, skel, ratio_resize
    return 0, 0


if __name__ == '__main__':
    img, skel, ratio = get_skel("F:/NSC/Sample/12.jpg")

    cv2.waitKey()
