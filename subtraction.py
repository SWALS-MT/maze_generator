import numpy as np
import cv2

jam = cv2.imread('./jam_cut2.png')

cv2.imshow('original', jam)
cv2.imwrite('./original.png', jam)

jam_modi = jam[:, :, 1] - jam[:, :, 2]
cv2.imshow('jam_modi', jam_modi)
cv2.imwrite('./green-red.png', jam_modi)

jam_modi = cv2.morphologyEx(jam_modi, cv2.MORPH_OPEN, (5, 5))

jam_dil = cv2.dilate(jam_modi, (5, 5), iterations=60)
jam_dil = cv2.erode(jam_dil, (5, 5), iterations=30)

jam_dil_int = jam_dil.copy()
sub = 17
for y in range(jam_dil.shape[0]):
    for x in range(jam_dil.shape[1]):
        if x - sub > 0 and jam_dil[y, x] == 0:
            jam_dil_int[y, x] = jam_dil[y, x-sub]


cv2.imshow('dilate', jam_dil_int)
cv2.imwrite('./dilate.png', jam_dil_int)
cv2.waitKey(0)


def wc_to_ic_rate(IC1, IC2, WC1, WC2):
    """ IC: Image Coordinate (画像座標)
        WC: World Coordinate (世界座標)
        2点間における緯度・経度の差と画像座標の差は比例関係にある(厳密には地球は球体なので違うが，範囲を絞れば微小である):
        1 [度] = (IC2 - IC1) / (WC2 - WC1) [pixel]
    """
    rateX = (IC2[0] - IC1[0]) / (WC2[0] - WC1[0])
    rateY = (IC2[1] - IC1[1]) / (WC2[1] - WC1[1])
    return np.array([rateX, rateY])

# example
IC1 = np.array([320, 332])  # [x, y] -> 渋谷スクランブル交差点
IC2 = np.array([82, 50])  # 代々木公園交番前
WC1 = np.array([139.70050927024405, 35.659477697903455]) # [経度, 緯度] -> 渋谷スクランブル交差点
WC2 = np.array([139.6917974559475, 35.6678544268231])  # 代々木公園交番前

rate = wc_to_ic_rate(IC1, IC2, WC1, WC2)
print('rate:', rate)
WCX = np.array([139.7008149154306, 35.662209127073574])  # タワレコ渋谷店前

# WC2を利用してICXを求めるパターン
subICX = rate * (WC2 - WCX)
ICX = IC2 - subICX  # ICX: 求めたい画像座標(WCXに対応する画像座標)
print(ICX)
# WC1を利用してICXを求めるパターン
subICX = rate * (WC1 - WCX)
ICX = IC1 - subICX
print(ICX)