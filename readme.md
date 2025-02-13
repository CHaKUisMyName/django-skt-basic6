# Description

django project playground use python 3.13.1 pyenv venv bootstrap5

- login system check session from client and DB
- create middleware injection for get current User
- create decorator @requiredLogin for check login befor request

# Inner System

- User
- Organization
- Level

# Install

- install python 3.13.1
- install pyenv
- use pyenv python version
- create venv

```
python -m venv env
```

- activate venv

Activate venv สำหรับ Windows

```
 $ env\Scripts\activate
```

Activate venv สำหรับ macOS/Linux

```
source env/bin/activate
```

- pull this project branch main
- install lib

```
pip install -r requirements.txt
```

- run project

```
python manage.py runserver
```
