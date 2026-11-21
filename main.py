"""12주차 my_api 대체용 (12주차 폴더가 없는 학생이 14주차 실습에 쓰는 버전)

우리 카페 메뉴 API: menu.csv를 읽어 GET /menu, GET /menu/{item_id}를 제공한다.
실행: menu.csv와 같은 폴더에서
    python -m uvicorn main:app --reload
"""
import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

# main.py와 같은 폴더의 menu.csv를 읽는다 (내 컴퓨터에만 있는 C:\... 고정 경로를 쓰지 않음)
CSV_PATH = Path(__file__).parent / "menu.csv"

app = FastAPI(
    title="우리 카페 메뉴 API",
    description="12주차 실습 예시: 내가 정리한 데이터를 제공하는 API",
)


def load_menu():
    """CSV를 읽어 행 목록으로 돌려준다.

    id나 가격이 비었거나 숫자가 아닌 행(재료 불량)은 건너뛴다.
    그래서 CSV에 이상한 행이 있어도 서버가 500으로 무너지지 않는다.
    """
    rows = []
    # utf-8-sig: 엑셀에서 'CSV UTF-8'로 저장한 파일의 한글과 첫 열 이름이 깨지지 않게
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            try:
                row["id"] = int(row["id"])
                row["price"] = int(row["price"])
            except (ValueError, TypeError, KeyError):
                continue
            rows.append(row)
    return rows


@app.get("/menu", summary="메뉴 목록 조회")
def get_menu(
    category: str | None = Query(None, description="종류 (예: coffee, tea, dessert). 생략하면 전체"),
    max_price: int = Query(100000, ge=0, le=100000, description="최대 가격 (0 ~ 100000)"),
):
    """카테고리와 최대 가격으로 메뉴를 거릅니다. 범위 밖 값은 422로 거절됩니다."""
    rows = load_menu()
    if category:
        rows = [r for r in rows if r["category"] == category]
    rows = [r for r in rows if r["price"] <= max_price]
    return {"count": len(rows), "items": rows}


@app.get("/menu/{item_id}", summary="메뉴 하나 조회")
def get_item(item_id: int):
    """번호로 메뉴 하나를 찾습니다. 없는 번호면 404로 안내합니다."""
    for r in load_menu():
        if r["id"] == item_id:
            return r
    raise HTTPException(status_code=404, detail="해당 메뉴가 없습니다")
