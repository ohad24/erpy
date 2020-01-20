## ERPY - The First True Open Source ERP In Python

Welcome to the project, currently under development.

##### run stack using docker compose:

* download the repo
    
    ```git clone https://github.com/ohad24/erpy.git```

* run compose file
    ```bash
    POSTGRES_DB=test \
    POSTGRES_PASSWORD=1234 \
    SECRET_KEY=1234 \
    docker-compose up
    ```

##### sql schema:
![sql_schema](schema.png)


#### todo's:
* update ticket headers
    * categories
    * status
    * log writing
* email table