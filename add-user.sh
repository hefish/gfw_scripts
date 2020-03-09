#!/bin/sh

UID1=8427
UID2=8428
SHELL_=/bin/bash
HOME_DIR=/home/hefish
HOME_DIR2=/home/rongsu



. /etc/os-release

case $ID in 
    debian|ubuntu)
        useradd -g users -u $UID1 -G sudo -s $SHELL_ -d $HOME_DIR hefish
        useradd -g users -u $UID2 -G sudo -s $SHELL_ -d $HOME_DIR2 rongsu
        #passwd hefish
        mkdir $HOME_DIR
        ;;
    centos|fedora|rhel)
        useradd -g users -u $UID1 -G wheel -s $SHELL_ -d $HOME_DIR hefish
        useradd -g users -u $UID2 -G wheel -s $SHELL_ -d $HOME_DIR2 rongsu
        #passwd hefish
        ;;
esac

mkdir $HOME_DIR/.ssh
cat > $HOME_DIR/.ssh/authorized_keys << EOF
#
# hefish public keys

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCgrzK/4TIagqOZj+o6wc0nOXDooZSE0hTwe3U6Y4Y5o7ACmtSHbNubeJSYzv6SrW/R3uDOx05H8ojfUD3ajSfzyet3zZxQAOtxkX21r+kU/M8TjNaDAJVPeFqdPYDDyWcdnlQPiBTdjicLBa/Y7oGAtlLCIqaH5OSDEXPF2VLlxZhcyIOQkP4+xKNXxGL3q41T+cHtSiuInnwHBakxf65rjNkSo8fbfQr0rFDLrRlz1TgjEcNLHbAXzd0rDPNj/OFgiksp6+22195nmak+X0Zh5fGh1dzmEN807+HJVf0I2Kz/rhQeDjt9Kg+gXhI8s9wlF5f15UJ9DN9Z/XCQMrx1 hefish


EOF

chown -R hefish:users $HOME_DIR
chmod 700 $HOME_DIR/.ssh
chmod 600 $HOME_DIR/.ssh/authorized_keys


mkdir $HOME_DIR2/.ssh
cat > $HOME_DIR2/.ssh/authorized_keys << EOF
# RongSu

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDGkrLHEGOVC7XH0trbDumsZmlFjLuU0xHOv62Jaqm/8ZsY/Wxjwnrch6Q0TFz5Di6Og1NWgBWLb3MiI8aCwaWB6yDXleb4DPKP2GltWaICw9GNg7UE2AhFD9blSe+YMsi03UIV4q73EoBmbT9xjxtgA7jQGKBdL+Gf5hVyhkaSby5AML6Z8vhTDIMTP+/AMMHm+ng8C3maPKR4/MvccPbw0D5TDCK2iFnJJmkTW+7RRyP2gJ8z+ujSnlU9C9Gpv2OAWBAKlYVIYiAcim3PTeD8rxrk3zU7itwvRgMpO3jTof6g5vEStiBlYpOETgDQq5nI486dpmbSLVlibAb9WX61uqKw1TREmyDuSY19PC8qe8PLGfV+ucBMuEFxb0m+zwJMHHfvFyghBXFYfL2c0uI+k6/uWPUlP78LhSEmWjMXI9tNXRkbO56Uavr/UeDdvgHPFDmZNnnBShA59yYMTJlZNKM9lBziyK1V1GodHZDEcjgXpPOPPBoeF2OoF9ZNbATZRjfTNhQkPgzqxho/Ebei4GLn84SIR/jOijcXGVNYEZXnaZYAPGy9+Dq4ZPwgP8FTPaxfTL7hq2L7AZM7p64yklbt9RmaFurIkVU3ZF5qOslOVTJf7oDEn3QCJ21mKzMQMvjxsd1k4wPMUNATYe9Oq1WrrrL/M5GK/2/bisH8Lw== rennichow@gmail.com


EOF

chown -R rongsu:users $HOME_DIR2
chmod 700 $HOME_DIR2/.ssh
chmod 600 $HOME_DIR2/.ssh/authorized_keys
