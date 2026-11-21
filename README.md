# my_api (12주차 대체용)

12주차에 만든 my_api 폴더가 없는 학생이 14주차 실습에 쓰는 폴더입니다.
12주차 실습 결과와 같은 카페 메뉴 API입니다.

- main.py: 메뉴 API (GET /menu, GET /menu/{번호})
- menu.csv: 카페 메뉴 데이터 6행
- CLAUDE.md: 12주차 설계서

## 내 PC에서 실행

```
pip install fastapi uvicorn
python -m uvicorn main:app
```

브라우저에서 http://127.0.0.1:8000/docs 를 엽니다.

## .devcontainer 폴더는?

Docker Desktop을 설치할 수 없는 학생이 GitHub Codespaces에서 실습할 때 쓰는 설정입니다.
내 PC에서 실습할 때는 신경 쓰지 않아도 됩니다.
