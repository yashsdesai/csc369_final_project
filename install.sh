#!/bin/bash

apt update
apt install python3-pip

pip install selenium
pip install rsa

chmod +x $(pwd)/chromedriver
echo 'export PATH="$pwd/ChromeDriver:$PATH"' >> ~/.profile
source ~/.profile

echo "Enter your LinkedIn Credentials"
echo -n "Email: "
read email
echo -n "Password: "
read -s password

echo $email > credentials.txt
echo $password >> credentials.txt

openssl genrsa -out key.txt 2048
#enc_password=$(echo $password | openssl rsautl -inkey key.txt -encrypt)

#json='{"username":"'"$email"'","password":"'"$enc_password"'"}'
#echo $json > credentials.txt



#echo $enc_email > credentials.txt
#echo "" >> credentials.txt
#echo $enc_password >> credentials.txt

#openssl rsautl -inkey key.txt -decrypt $enc_email

#echo $password | openssl rsautl -inkey key.txt -encrypt >> output.bin

#openssl rsautl -inkey key.txt -decrypt < output.bin



