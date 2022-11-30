# TaskBoard

## Table of Contents
1. Frontend
2. Backend
3. Deployment

## Frontend

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 9.1.7.

### Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

### Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

### Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

### Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

### Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

### Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).

## Backend
The backend runtime is built using Python and Flask and data is persisted in SQLite. View all the endpoints in [this file](./backend/endpoints.http).

Flush the database by simply deleting the database file from the disk. A new file will be created when you start the server again.

## Deployment
The application can be deployed on an VM. Steps to deploy:

```bash
# First build the frontend locally. This will create all frontend static files in `backend/taskBoard` directory.
npm run build --prod

# Copy all the files to remote machine, this will copy all the files to backend directory
scp -r -i path-to-key-file.pem backend/ ubuntu@ec2-3-252-125-48.eu-west-1.compute.amazonaws.com:~/backend/

# ssh to the remote machine
ssh -i path-to-key-file.pem ubuntu@ec2-3-252-125-48.eu-west-1.compute.amazonaws.com

# Once you are in, you need to install the requirements and run the server
cd backend
pip3 install -r requirements.txt

# Run the server using
nohup python3 backend.py &
```

### Troubleshooting

#### Restarting the application
```bash
# Find the application por
$ netstat -plnt | grep 8080
ubuntu@ip-172-31-39-248:~$ netstat -plnt | grep 8080
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      3277/python3

# Kill the process if it's present
$ kill -9 3277

# Start the server again
nohup python3 backend.py &
```


#### Database is corrupt or flush the database
```bash
# Remove the sqlite file
rm -rf task-board-db.sqlite

# Start the application again
nohup python3 backend.py &
```
Note, this will delete all the existing tasks
