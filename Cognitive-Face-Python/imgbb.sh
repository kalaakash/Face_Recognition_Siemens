index=$1
#mv ../../../../Pictures/Logitech\ Webcam/Picture\ $1.jpg ../../../../Pictures/Logitech\ Webcam/$1.jpg
img_location=
key_val=bab8667bf1ca9dc1380df6471dedcf87
curl --location --request POST "https://api.imgbb.com/1/upload?key=$key_val" --form "image=$img_location"
