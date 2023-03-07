# Honours Project Application
This web application was built using Flask for my 4th year honours project at Glasgow Caledonian University. The application aims to use a facial expression recognition model which has been trained on the FER-2013 dataset. The aim of the application is to provide a tool for diagnosing mental health disorders.

## Key Development Technologies 
Flask, TensorFlow, Keras, Jinja, NumPy, Pandas, SQLAlchemy, SQLite


## Running the Application
In order to run the application make sure you have Python3 installed on your machine. The following steps can then be used to run the application itself.

Step 1: initalise empty git repository in empty folder.
```
git init
```

Step 2: Clone the repository into the folder
```
git clone https://github.com/GaryS0410/HonoursProjectApplication.git
```

Step 3: Move into project directory
```
cd HonoursProjectApplication
```

Step 4: Create a Python virtual environment
```
py -3 venv venv
```

Step 5: Activate the virtual environment 
```
venv\Scripts\activate
```

Step 6: Install the projects dependencies. This can be done by installing the contents of the requirements.txt file. To do so run the following:
```
pip install -r requirements.txt
```
Note that it is highly recommended to only do this if you are currently inside your activated virtual environment. 

Step 7: Run the application
```
Add later. Currently think my environment run variable is set to something else, therefore won't work on other machines.
```

## Application Description
As previously stated this application was built in order to assist in diagnosing mental illnesses. To achieve this, the application was created which allows a patient to participate in a therapy session wherein an image is taken of them through their webcam every so often (depending on length of session chosen). This data is then collected and stored for further review by a therapist, along with an emotional score metric to give an idea of how the patient was feeling overall during the session.