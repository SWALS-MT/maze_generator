import numpy as np
import cv2

jam = cv2.imread('./jam_cut2.png')

cv2.imshow('original', jam)

jam_modi = jam[:, :, 1] - jam[:, :, 2]
cv2.imshow('jam_modi', jam_modi)

jam_modi = cv2.morphologyEx(jam_modi, cv2.MORPH_OPEN, (5, 5))

jam_dil = cv2.dilate(jam_modi, (5, 5), iterations=60)
jam_dil = cv2.erode(jam_dil, (5, 5), iterations=30)
cv2.imshow('dilate', jam_dil)

jam_dil_int = jam_dil.copy()
sub = 17
for y in range(jam_dil.shape[0]):
    for x in range(jam_dil.shape[1]):
        if x - sub > 0 and jam_dil[y, x] == 0:
            jam_dil_int[y, x] = jam_dil[y, x-sub]


cv2.imshow('dilate', jam_dil_int)
cv2.waitKey(0)


def wc_to_ic_rate(IC1, IC2, WC1, WC2):
    """ IC: Image Coordinate (画像座標)
        WC: World Coordinate (世界座標)
        1 [度] = (IC2 - IC1) / (WC2 - WC1) [pixel]
    """
    rateX = (IC2[0] - IC1[0]) / (WC2[0] - WC1[0])
    rateY = (IC2[1] - IC1[1]) / (WC2[1] - WC1[1])
    return np.array([rateX, rateY])

# example
IC1 = np.array([1, 2])  # [x, y]
IC2 = np.array([224, 220])
WC1 = np.array([131.61, 54.3]) # [経度, 緯度]
WC2 = np.array([143.53, 41.2])

rate = wc_to_ic_rate(IC1, IC2, WC1, WC2)
print('rate:', rate)
WCX = np.array([136.23, 49.7])
subICX = rate * (WC2 - WCX)
print(IC2 - subICX)
subICX = rate * (WC1 - WCX)
print(IC1 - subICX)