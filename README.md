# Flask-Blog
A social media application developed using flask implementing access control policies. 
## Access Control Policies
* 3 policies are implemented in this application and are maintained on different branches of this repository
* RBAC is maintained in branch rbac
* MAC is maintained in branch mac
* DAC is maintained in branch dac
* Use the below instructions to traverse and try out each of these policies. 
* The attached pdf also 

## Steps to run this app:
The below steps detail the way to build the application. There is no direct executable file because
this application requires prerequisites downloaded Once they are downloaded only one command is required. 
### Prerequisites
* Install Python3 (https://wiki.python.org/moin/BeginnersGuide/Download)
* Install pip (https://pip.pypa.io/en/stable/installing/)
* Install Git (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Unzip app
 ### Running the app

```shell
virtualenv venv --distribute
source venv/bin/activate
pip3 install -r requirements.txt
pip3 freeze > requirements.txt
git branch
```
* Check which branch you are currently in. 
* There are 4 branches: rbac, dac, mac, master
* Checkout the branch based on which policy needs to be used. 
```shell
git checkout <branch-name>
python3 run.py
```
Open 127.0.0.1:5000 on a web browser.

## Developers
* Avakash Bhat (17CO110)
* Shrindhi Anil Varna (171CO145)


