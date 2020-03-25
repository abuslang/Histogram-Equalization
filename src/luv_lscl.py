import cv2
import numpy as np
import sys

# read arguments
if(len(sys.argv) != 7) :
    print(sys.argv[0], ": takes 6 arguments. Not ", len(sys.argv)-1)
    print("Expecting arguments: w1 h1 w2 h2 ImageIn ImageOut.")
    print("Example:", sys.argv[0], " 0.2 0.1 0.8 0.5 fruits.jpg out.png")
    sys.exit()

w1 = float(sys.argv[1])
h1 = float(sys.argv[2])
w2 = float(sys.argv[3])
h2 = float(sys.argv[4])
name_input = sys.argv[5]
name_output = sys.argv[6]

# check the correctness of the input parameters
if(w1<0 or h1<0 or w2<=w1 or h2<=h1 or w2>1 or h2>1) :
    print(" arguments must satisfy 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1")
    sys.exit()

# read image
inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
# convert image from BGR (default colorspace) to LUV
luvImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2Luv)


if(inputImage is None) :
    print(sys.argv[0], ": Failed to read image from: ", name_input)
    sys.exit()

# cv2.imshow("input image: " + name_input, inputImage)

# check for color image and change w1, w2, h1, h2 to pixel locations
rows, cols, bands = inputImage.shape
if(bands != 3) :
    print("Input image is not a standard color image:", inputImage)
    sys.exit()

W1 = round(w1*(cols-1))
H1 = round(h1*(rows-1))
W2 = round(w2*(cols-1))
H2 = round(h2*(rows-1))

# The transformation should be applied only to
# the pixels in the W1,W2,H1,H2 range.
# The following code goes over these pixels

tmp1 = np.copy(inputImage)
for i in range(H1, H2+1) :
    for j in range(W1, W2+1) :
        tmp1[i,j] = luvImage[i,j]

# cv2.imshow("luvImage", tmp1)



tmp2 = np.copy(luvImage)

# find a and b
LList = set()
for i in range(0, rows):
    for j in range(0, cols):
        L, u, v = tmp2[i, j]
        LList.add(L)
LList = list(sorted(LList))
a = LList[0]
b = LList[-1]

# linear scaling
def linearScale(x, a, b, A, B):
    return (((x-a) * (B-A) / (b-a)) + A)


for i in range(0, rows):
    for j in range(0, cols):
       # tmp2[i, j] = linearScale(tmp2[i, j], a, b, 0, 255)
        L, u, v = tmp2[i, j]
        newL = linearScale(L, a, b, 0, 255)
        tmp2[i, j] = newL, u, v

# cv2.imshow("linear scale", tmp2)

# change scaled image back to bgr (not sure if youre supposed to do this)
tmp2 = cv2.cvtColor(tmp2, cv2.COLOR_Luv2BGR)

tmp3 = np.copy(inputImage)
for i in range(H1, H2+1) :
    for j in range(W1, W2+1) :
        tmp3[i,j] = tmp2[i,j]


# cv2.imshow("luv_lscl", tmp3)
# saving the output - save the gray window image
cv2.imwrite(name_output, tmp2)

# wait for key to exit
# cv2.waitKey(0)
# cv2.destroyAllWindows()