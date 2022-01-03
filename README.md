# csc369_final_project

Basic LinkedIn scraper that uses PySpark to find and process a searched person/people and reduce their profile
to the very basics in a simple, compressed format


**Load times may vary based on Internet connection**

Prerequisites
*************
    -PySpark
  
    -Chromium-based Web Browser
  
Install
********
1.) Clone the repository to your machine

    git clone https://github.com/yashsdesai/csc369_final_project

2.) Run install script

    bash install.sh

3.) When prompted, enter your LinkedIn credentials

4.) When install script completes, run the scraper 

    python3 scraper.py [Optional CSV Filename]

5.) If prompted with an error, update path of browser in the commented code. You can do this by running the following in your terminal:

    which google-chrome
 
