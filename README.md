# TKB Tự động
## Tự động cập nhật thời khóa biểu của UNISOFT và hiển thị lên desktop theo thời gian thực

Để chạy chương trình dùng lệnh:

```sh
python TKBTuDong.py
```

### Lưu ý:
- Thay đổi biến _ABSOLUTE_BASE_PATH_ tới vị trí ảnh gốc
- Thay đổi biến _Cord[x,y]_ sẽ thay đổi vị trí của TKB trên ảnh


### Một số ví dụ:
[Ảnh gốc: ](https://www.pixiv.net/en/artworks/87054415)
![Ảnh gốc](https://github.com/DuongTung2003/TKBTuDong/blob/master/sample.jpg?raw=true)

Hình nền sau khi chạy chương trình:
![Ảnh TKB](https://github.com/DuongTung2003/TKBTuDong/blob/master/ExampleIMG/Screenshot.png?raw=true)


Nếu tiết tiếp theo nằm trong ngày thì sẽ hiện màu xanh:
![Trong ngày](https://github.com/DuongTung2003/TKBTuDong/blob/master/ExampleIMG/CoTietHomnay.png?raw=true)

Nếu hôm nay không có tiết nào hoặc đã học hết tiết cuối cùng trong ngày thì sẽ hiện màu trắng,
còn ngày tiếp theo có tiết sẽ hiện màu vàng:
![Hết tiết](https://github.com/DuongTung2003/TKBTuDong/blob/master/ExampleIMG/tietHomTiepTheo.png?raw=true)

Tính từ thời điểm chạy chương trình nếu đang trong tiết thì sẽ hiện màu đỏ:
![Trong tiết](https://github.com/DuongTung2003/TKBTuDong/blob/master/ExampleIMG/Dangtrongtiet.png?raw=true)


### Để chạy chương trình tại startup:

Mở hộp thoại _Run_ nhập 
```sh
shell:startup
```
Tạo shortcut của _TKB.cmd_ vào thư mục hiện lên
 

Tác giả: [Facebook]

[Facebook]: <https://www.facebook.com/duongdoan.tung.56>
