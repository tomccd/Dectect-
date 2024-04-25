#--Nhận diện hình dạng của khối hình (nhận đơn lẻ hoi)
import cv2 as cv
import numpy as np
#--Đọc ảnh và chuyển ảnh sang gray
arr = cv.imread('./trapez.jpg')
gray_arr = cv.cvtColor(arr,cv.COLOR_BGR2GRAY)
#--Sử dụng nhiễu Gaussian để làm mịn
gauss = cv.GaussianBlur(gray_arr,(5,5),0)

#--Tìm cạnh Canny
canny = cv.Canny(gauss,120,200)

#--Tìm các đường viền với cài đặt chỉ tìm các đường viền ngoài
contours,_ = cv.findContours(canny,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)

# print(contours[0].shape)
#--Tính toán xấp xỉ chu vi đường
perimeter = cv.arcLength(contours[0],True)
# print(perimeter)
#--Tìm đường viền xấp xỉ khép kín với đường viền của vật thể gốc
approximate_shape = cv.approxPolyDP(contours[0],0.1*perimeter,True)
#--Tìm số các điểm tạo đường viền xấp xỉ
len_approx = len(approximate_shape)
# print(len_approx)

#--Nếu có 4 điểm tạo nên đường viền xấp xỉ khép kín-> kết quả cho ra có thể là hình bình hành, hình chữ nhật, hình vuông
if len_approx==4:
    point_A = approximate_shape[0][0]
    point_D = approximate_shape[1][0]
    point_C = approximate_shape[2][0]
    point_B = approximate_shape[3][0]
    #--Kiểm chứng điểm
    cv.line(arr,point_A,point_B,(0,255,0),2)
    cv.line(arr,point_C,point_D,(0,255,0),2)
    cv.line(arr,point_A,point_D,(0,255,0),2)
    cv.line(arr,point_B,point_C,(0,255,0),2)
    # -Tìm độ dài cạnh AB,CD,AD,BC và đường chéo AC bằng tọa độ của A,B,C,D sử dụng khoảng cách giữa 2 điểm trong tọa độ
    AB_distance = np.sqrt(np.power(point_A[0]-point_B[0],2)+np.power(point_A[1]-point_B[1],2))
    AD_distance = np.sqrt(np.power(point_A[0]-point_D[0],2)+np.power(point_A[1]-point_D[1],2))
    CD_distance = np.sqrt(np.power(point_C[0]-point_D[0],2)+np.power(point_C[1]-point_D[1],2))
    BC_distance = np.sqrt(np.power(point_B[0]-point_C[0],2)+np.power(point_B[1]-point_C[1],2))
    AC_distance = np.sqrt(np.power(point_A[0]-point_C[0],2)+np.power(point_A[1]-point_C[1],2))
    #-Sử dụng Pytago tìm đường chéo để phân biệt giữa hình bình hành và 2 hình vuông và hình chữ nhật
    diagonal = np.sqrt(np.power(AB_distance,2)+np.power(AD_distance,2))
    # print(f'AB : {AB_distance}px, AD : {AD_distance}px, AC : {AC_distance}px, Diagonal : {diagonal}')
    #- Xây dựng điều kiện đường chéo
    condition_diagonal_1 = np.abs(AC_distance-diagonal) >= 0
    condition_diagonal_2 = np.abs(AC_distance-diagonal) <= 1
    #- Nếu mà điều kiện Pytagos đúng -> phân biệt được hình bình hành,hình thang với hình vuông và hình chữ nhật
    if np.logical_and(condition_diagonal_1,condition_diagonal_2) == True:
        #- Xây dựng điều kiện AB xấp xỉ bằng AD -> là hình vuông, nếu không là hình chữ nhật
        if (np.abs(AB_distance-AD_distance) <=1.5) == True:
            print("Square") #Hình vuông
        else:
            print("Rectangle") #Hình chữ nhật
    else:
        #- Xây dựng điều kiện của hình bình hành 
        condition_distance_parallelogram_1 = np.abs(AB_distance-CD_distance) <=1.5
        condition_distance_parallelogram_2 = np.abs(BC_distance-AD_distance) <=1.5
        # print(f'AB : {AB_distance}px, CD : {CD_distance}px')
        if np.logical_and(condition_distance_parallelogram_1,condition_distance_parallelogram_2) == True:
            print("Parallelogram") #Hình bình hành
        else:
            print("Trapeziem") #Hình thang
        
#--Nếu có 3 điểm tạo nên đường viên xấp xỉ khép kín -> kết quả cho ra là hình tam giác (chưa làm)
#--Còn lại khum bít
else:
    print("I dunno")

cv.imshow('bla',arr)

cv.waitKey(0)