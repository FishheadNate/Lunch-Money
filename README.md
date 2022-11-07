# Lunch-Money
Simple tool to check account balances on [MySchoolBucks](https://www.myschoolbucks.com/)

## Requirements

- Python packages
  ```bash
  pip install -r requirements.txt
  ```

- [MySchoolBucks account with 2-Step Verification via Text Message](https://login.myschoolbucks.com/users/register/getsignup.action?login_hint=&clientID=schoolbucks)

- `login_creds.yml` with MySchoolBucks credentials
  ```YAML
  MySchoolBucks:
    url: https://www.myschoolbucks.com/
    email: name@example.com
    password: password
  ```

## Usage

1. Collect account history from MSB
  ```bash
  ./lunch-money.py
  ```

2. Launch interactive dashboard
  ```bash
  streamlit run ./dashboard.py
  ```

## Dashboard

<img src='https://github.com/FishheadNate/Lunch-Money/blob/main/demo/LunchMoneyDashboard.png' width='600'>

## Overview
1. `lunch-money.py` opens a new Chrome browser and log into MySchoolBucks using the account credentials found in `login_creds.yml`.
2. After account credentials are sent, the script will select the "Text Message" option for 2-Step Verification and ask for the single-use code to be entered in the terminal.
3. Once successfully logged in, the script will pull transactions history data for all the linked student accounts and exports the data as a CSV.
4. `dashboard.py` launches an interactive dashboard for viewing the CSV created by `lunch-money.py`.

---

## License

Lunch-Money is released under the MIT license. See [LICENSE](LICENSE) for details.
