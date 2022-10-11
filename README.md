# Lunch-Money
Simple tool to check account balances on [MySchoolBucks](https://www.myschoolbucks.com/)

## Requirements

- Python
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

```bash
./lunch-money.py
```

## Overview
1. Script will open a new Chrome browser and log into MySchoolBucks using the account credentials found in `login_creds.yml`.
2. After account credentials are sent, the script will select the "Text Message" option for 2-Step Verification and ask for the single-use code to be entered in the terminal.
3. Once successfully logged in, the script will navigate to the transactions history page for all the linked student accounts.

---

## License

Lunch-Money is released under the MIT license. See [LICENSE](LICENSE) for details.