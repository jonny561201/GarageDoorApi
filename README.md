# Project Purpose
- Create flask APis for operating a garage door
- Maintain security through login and persistence of JWT tokens
- Provide simple APIs for opening/closing and retrieving the current status
- Learn more about application hosting on Raspberry Pi

# Development
1. After cloning repo:
    ```
    pip install -Ur requirements.txt
    pip install -Ur test_requirements.txt
    ```
2. Install docker desktop for linux containers
3. Provide any corresponding test coverage in directories `/test/integration` and `/test/unit`
4. Prior to committing code execute `./run_all_tests.sh` to run unit and integration tests which will start a postgres docker container
5. Stand up application by executing `python app.py`
