# uShoe
An AI model trained on images of the user's favorite shoes. Notifies the user of new shoe releases they may like.

# Setup
Clone this repository:
```
git clone https://github.com/fwang356/uShoe.git
```
Create a virtual environment:
```
python -m virtualenv venv
```
Activate the environment:
```
venv/Scripts/activate
```
Install the dependencies:
```
pip install -r requirements.txt
```
Replace default training images with images of your favorite shoes and edit main.py according to the comments and desired specifications.

# How to Use
Run the program to create and train the model:
```
python main.py
```
Comment out the following lines:
```
inputs(metadata)
model(metadata)
train(metadata)
```
Uncomment the following line:
```
# main(metadata)
```
In order to run the program asynchronously, follow the appropriate guide to schedule a time for the script to run:

Windows: http://theautomatic.net/2017/10/03/running-python-task-scheduler/

Mac OS: http://theautomatic.net/2020/11/18/how-to-schedule-a-python-script-on-a-mac/
