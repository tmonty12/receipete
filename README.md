# receipete 

## How to use Receipete application locally

### Installation

A pre-requisite for running the Receipete application is that you have Python installed. If you do not have Python installed, please download version 3.10.10 for your specific OS [here](https://www.python.org/downloads/). We ran the application using Python version 3.10 installed. If you have another version installed, we cannot guarantee that the dependency libraries are compatible with your version of python. If incompatible, please install python version 3.10.10 and ensure that you use this version for the creation of the virtual environments and running the application.

1. Clone this repository to your computer.

```
git clone https://github.com/tmonty12/receipete.git
```

2. Change into the repository directory.
```
cd receipete
```

3. Create a virtual environment.
```
python -m venv venv
```
We encourage you to use a virtual environment to handle library dependencies.

4. Activate your virtual environment.
```
venv/Scripts/activate
```

5. Install the library dependencies in the `requirements.txt` file.
```
python -m pip install -r requirements.txt
```

6. Initialize your local database instance.
```
flask db init
```
We are using sqlite for local deployment.

7. Migrate your database.
```
flask db migrate
```
We are using the flask-migrate package to handle changes made during database development.

8. Upgrade your database.
```
flask db upgrade
```

### Running the application locally
1. Start the application.
```
flask run
```

2. Navigate to the webpage.
Enter `localhost:5000` into your browser.
