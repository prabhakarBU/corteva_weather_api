To clone above project:
git clone https://github.com/prabhakarBU/corteva_weather_api.git

Go to the project foler.

Run pip install -r requirements.txt

Configure your Database:
Update your database details under dbconfig.ini file :
[mysqlDB]
host = localhost
db = cortevaweather
user = root
pass = root

Run ``` python app.py ``` to run the app on port 8080.

Swagger Api url:
http://localhost:8080/swagger/


Run unit test cases by running following command on the terminal:
pytest

Deployment:
Approach 1: ( Naive Approach )
This approach is when the architecture is a basic setup of EC2 server/s and the code just needs to be
deployed to the EC2s. 
-Creating a Github action workflow which triggers whenever we push a new build
-The Github action workflow has a file called "workflow.yml" that has bunch of jobs and build steps which
could be configured based on the environment.
Steps:
-Create Environments under Settings in Github section to provide our app secrets, aws secrets etc.
-Then, create a file .github/workflows/workflow.yml that would look somewhat like below:

        name: "Development Build"
        on:
        push:
            branches: [ development ]
        pull_request:
            branches: [ development ]

        jobs:

        Build:

            runs-on: ubuntu-latest
            environment:
            name: Development
            strategy:
            matrix:
                python-version: [3.7, 3.8, 3.9]

            steps:
            - name: Check out code
            uses: actions/checkout@v2

            - name: Set up Python ${{ matrix.python-version }}
            uses: actions/setup-python@v2
            with:
                python-version: ${{ matrix.python-version }}

            - name: Install dependencies
            run: |
                python -m pip install --upgrade pip
                if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
                if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
            - name: Test with pytest
            run: |
                if [ -d tests ] || [ -d test ]; then FLASK_ENV=${{secrets.FLASK_ENV}} python -m pytest; fi

        DeployDev:
            name: Deploy to Dev
            needs: [Build]
            runs-on: ubuntu-latest
            environment:
            name: Development
            steps:
            - name: Deploy
                run: echo I am deploying the api to AWS
            - name: Deploy in EC2
                env:
                PRIVATE_KEY: ${{ secrets.AWS_PRIVATE_KEY  }}
                HOST_NAME : ${{ secrets.HOST_NAME  }}
                USER_NAME : ${{ secrets.USER_NAME  }}
                USER_PASSWORD: ${{ secrets.USER_PASSWORD }}
                APP_DIR: ${{secrets.APP_DIR}}
                SERVICE_NAME: ${{secrets.SERVICE_NAME}}
                run: |
                echo "$PRIVATE_KEY" > private_key && chmod 600 private_key
                ssh -o StrictHostKeyChecking=no -i private_key ${USER_NAME}@${HOST_NAME} "
                    cd ${APP_DIR} &&
                    git pull &&
                    echo ${USER_PASSWORD} | sudo -S systemctl restart ${SERVICE_NAME} "


Approach 2: ( AWS CodePipeline CI/CD )
This approach could use more resources and depends if the team is using ECS cluster.
-Using a CodePipeline to upload the code which could be integrating with Github like third parties tools.
-CodePipeline behaves as Continuous Integration for our code workflow at this point.
-To make this work, we would create a buildspec.yml file in our project that should read and build the code
from CodePipeline and push it to the AWS CodeBuild.
-Now at this point, we should have ECR endpoints, we will use this endpoints to deploy our dockerized Flask app in 
a bit.
-Now, we could go ahead and create a ECS cluster that'd read the build from the ECR endpoints we just got from the above step.
-This last could be done either manaully or could be automated creating another AWS CodeBuild Stage with another
yaml script that'd push the build to the ECS.