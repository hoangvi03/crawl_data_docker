Download Docker
python version 3.12
vào thư mục project > chạy lệnh linux: docker-compose build

lệnh tạo db(không cần vì có tạo sẳn): docker-compose run web python manage.py migrate

chạy server: docker-compose up

*note: Không chạy được cứ thêm sudo