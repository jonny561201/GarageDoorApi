# Project Purpose #
- Create flask APis for operating a garage door
- Maintain security through login and persistence of JWT tokens
- Provide simple APIs for opening/closing and retrieving the current status
- Learn more about application hosting on Raspberry Pi

# Development #
1. After cloning repo:
    * create virtual environment: `virtualenv venv`
    * activate virtual environment: `source ./venv/scripts/activate`
    * install production dependencies: `pip install -Ur requirements.txt`
    * install test dependencies: `pip install -Ur test_requirements.txt`
2. Install docker desktop for linux containers
3. Provide any corresponding test coverage in directories `/test/integration` and `/test/unit`
4. Prior to committing code execute `./run_all_tests.sh`
    * will start/stop a postgres docker container
5. Stand up application by executing `python app.py`
    * will need to execute flyway against a postgres database for production
