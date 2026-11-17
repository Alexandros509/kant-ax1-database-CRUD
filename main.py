import json
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

supabase: Client


# 회원 users
def create_user(email, name):
    return supabase.table("users").insert({"email": email, "name": name}).execute().data

def get_user(user_id):
    return supabase.table("users").select("*").eq("id", user_id).execute().data

def update_user(user_id, name):
    return supabase.table("users").update({"name": name}).eq("id", user_id).execute().data

def delete_user(user_id):
    return supabase.table("users").delete().eq("id", user_id).execute().data


# 상품 products
def create_product(name, price):
    return supabase.table("products").insert({"name": name, "price": price}).execute().data

def get_product(product_id):
    return supabase.table("products").select("*").eq("id", product_id).execute().data

def update_product(product_id, price):
    return supabase.table("products").update({"price": price}).eq("id", product_id).execute().data

def delete_product(product_id):
    return supabase.table("products").delete().eq("id", product_id).execute().data


# 주문 orders
def create_order(user_id, product_id, quantity):
    return supabase.table("orders").insert({
        "user_id": user_id, "product_id": product_id, "quantity": quantity,
    }).execute().data

def get_order(order_id):
    return supabase.table("orders").select("*").eq("id", order_id).execute().data

def update_order(order_id, quantity):
    return supabase.table("orders").update({"quantity": quantity}).eq("id", order_id).execute().data

def delete_order(order_id):
    return supabase.table("orders").delete().eq("id", order_id).execute().data


def show(label, rows):
    print(f"\n{label}: {len(rows)}건")
    print(json.dumps(rows, ensure_ascii=False))
    return rows


def run_demo():
    print("===== 1. 회원 생성·조회·수정 =====")
    user = show("회원 C", create_user("demo@example.com", "연습 회원"))[0]
    show("회원 R", get_user(user["id"]))
    show("회원 U", update_user(user["id"], "수정한 회원"))

    print("\n===== 2. 상품 생성·조회·수정 =====")
    product = show("상품 C", create_product("키보드", 10000))[0]
    show("상품 R", get_product(product["id"]))
    show("상품 U", update_product(product["id"], 12000))

    print("\n===== 3. 주문 생성·조회·수정 =====")
    order = show("주문 C", create_order(user["id"], product["id"], 1))[0]
    show("주문 R", get_order(order["id"]))
    show("주문 U", update_order(order["id"], 2))

    # FK 때문에 주문 → 상품 → 회원 순서로 삭제
    print("\n===== 4. 주문·상품·회원 삭제 =====")
    show("주문 D", delete_order(order["id"]))
    show("상품 D", delete_product(product["id"]))
    show("회원 D", delete_user(user["id"]))
    show("삭제 후 회원 조회", get_user(user["id"]))  # 0건

    print("\n완료: 회원·상품·주문 CRUD를 확인했습니다.")


def main():
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    global supabase
    supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_PUBLISHABLE_KEY"])
    run_demo()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"실행 실패: {error}")
        raise SystemExit(1)