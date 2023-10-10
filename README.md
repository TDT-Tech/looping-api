# looping-api
## Prerequisites

- Download latest version of Python (3.12) https://www.python.org/downloads/
  - After finish downloading, run the `update shell command` in the installed python fodler file to ensure your terminal is using the right python version
  - Run python3 (or python) --version and ensure it returns python 3.12.0
 
- Download latest version of node(v18.18.0) and npm(9.8.1)
  - https://nodejs.org/en/download, follow instruction guides from this website, make sure you select v18.18.0
  - After installing run `node --version` and `npm --version` to ensure you have the above versions
 
- Download homebrew
  - Download from https://brew.sh/
    - If you're on Mac M1: https://stackoverflow.com/questions/66666134/how-to-install-homebrew-on-m1-mac
    - If you're on windows, damn unlucky
   
- Set up postgresql
  - `brew install postgresql`
  - `brew services start postgresql`
    - to stop `brew services stop postgresql`
  - Configure a root user on postgres from your terminal
    - Open postgres through ->`psql postgres`
    - `CREATE ROLE admin WITH LOGIN PASSWORD <insert_your_password_here> (will need to remember this to connect to db from our app locally)`
    - `ALTER ROLE admin CREATEDB;
    - `\q` to exit from postgres terminal
  - Verify user has been created
    - `psql postgres -U admin`
    - In postgres terminal type `\du` and verify your new `admin` user has been created
  - (OPTIONAL) Download PgAdmin which is a separate app to more easily view your postgres database
    - https://www.pgadmin.org/download/
    - After downloading, provide the following credentials on the pgadmin app to connect to your local db server
      ```
        host – “localhost”
        user – “admin”
        password – “<insert_your_password_here>”
        maintenance database – “postgres”
      ```

## Set up project

- `git clone https://github.com/tommypnguyen/looping.git`
- Set up backend
  - `cd backend`
  - Create virtualenv
    - `python3 -m venv venv
  - Activate virtualenv (remember to do this everytime you use backend)
    - `source venv/bin/activate`
  - Install dependencies for app
    - `pip install -r requirements.txt`
