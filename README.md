# TKB Tự động
## Tự động cập nhật thời khóa biểu của Trường ĐH PHENIKAA và hiển thị lên desktop theo thời gian thực

Để chạy chương trình dùng lệnh:

```sh
python TKBTuDong.py
```
### Các chức năng chính
- Hiển thị thời khóa biểu lên hình nền máy tính
- Thay đổi hình nền ngẫu nhiên với các hình nền trong thư mục Backgrounds
- Tạo sự kiện các tiết học của 7 ngày tiếp theo lên Google Calendar
- Nhắc trước tiết học 2 lần: trước 30 phút và 5 phút
- Có thể chạy khi offline (chỉ thay đổi TKB trên hình nền) 
- Tự do thay đổi màu, phông chữ, vị trí của TKB trên hình nền
- Có thể cài đặt tự khởi chạy khi bật máy tính
### Lưu ý:
Google lịch giới hạn số người thử nghiệm ở 100 người nên liên hệ với tác giả qua Facebook hoặc Email để được sử dụng chức năng này!
> Trường hợp muốn sử dụng riêng hình nền: mở file TKBSetting.cfg thay đổi 
> FORCE_INTERNET_OFF = true

### Một số ví dụ:
Sự kiện được tạo trên Google calendar:
![Google calendar](https://github.com/DuongTung2003/TKBTuDong/blob/master/ExampleIMG/GoogleCalendarExample.png?raw=true)

![Windows Calendar](https://github.com/DuongTung2003/TKBTuDong/blob/master/ExampleIMG/CalendarExample.png?raw=true)

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
 

Liên hệ tác giả qua: [Facebook]

[Facebook]: <https://www.facebook.com/duongdoan.tung.56>
