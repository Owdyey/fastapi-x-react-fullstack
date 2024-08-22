#FastAPI

Environment setup:
!!!You should have python installed in you device. (I'm using python version 3.12)!!!

Create virtual environment:
       --- Open terminal and Navigate to your project directory
       --- Create the Virtual Environment by running the following command:
           on Windows:
               python -m venv env 
           on MacOs:
               python3 -m venv env
       --- to Activate the virtual environment
           on Windows:
              env/Scripts/activate
           on MacOs:
              source env/Scripts/activate
       --- to Deactivate your virtual environment
           on Windows:
              deactivate
           on MacOs:
              deactivate

Install all the Dependencies needed
       --- Open the terminal and Navigate to your project directory
       --- Activate the virtual environment if it is not activated. 
       --- Install all the dependencies by running the following command:
           pip install -r requirements.txt

Run the Development Server:
       --- Open the terminal and Navigate to your project directory
       --- Activate the virtual environment if it is not activated. 
       --- Navigate to the directory where the folder app is located.
       --- Run the following commands
           "uvicorn app.main:app --reload"
