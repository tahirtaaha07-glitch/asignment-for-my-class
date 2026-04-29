import os, json, jwt
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="gully_pro_2026_secret")
templates = Jinja2Templates(directory="templates")

DATA_FILE = "data.json"
ORDERS_FILE = "orders.json"

def get_db(file=DATA_FILE):
    if not os.path.exists(file):
        if file == DATA_FILE:
            default = {
                "users": {"admin": "1234"}, 
                "products": [], 
                "categories": ["Mobile", "Laptop", "Watch"],
                "ad": {"title": "PRO STORE", "price": "000", "image": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=1200"}
            }
        else: default = []
        with open(file, "w") as f: json.dump(default, f, indent=4)
        return default
    
    with open(file, "r") as f: 
        try:
            db = json.load(f)
            # Ensure categories exist in data.json
            if file == DATA_FILE and isinstance(db, dict):
                if "categories" not in db:
                    db["categories"] = ["Mobile", "Laptop", "Watch"]
                    save_db(db)
            return db
        except:
            return [] if file == ORDERS_FILE else {}

def save_db(data, file=DATA_FILE):
    with open(file, "w") as f: json.dump(data, f, indent=4)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    db = get_db()
    return templates.TemplateResponse("home.html", {
        "request": request, 
        "items": db.get("products", []), 
        "ad": db.get("ad", {}), 
        "categories": db.get("categories", ["Mobile", "Laptop", "Watch"]), 
        "user": request.session.get("user")
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    user = request.session.get("user")
    if not user or user.get("type") != "admin": 
        return RedirectResponse(url="/login")
    
    db = get_db()
    orders = get_db(ORDERS_FILE)
    
    # Safer revenue calculation to prevent 500 errors
    revenue = 0
    if isinstance(orders, list):
        for o in orders:
            if isinstance(o, dict):
                revenue += int(o.get('price', 0))

    return templates.TemplateResponse("admin.html", {
        "request": request, 
        "items": db.get("products", []), 
        "orders": orders, 
        "revenue": revenue, 
        "ad": db.get("ad", {}), 
        "categories": db.get("categories", ["Mobile", "Laptop", "Watch"])
    })

@app.post("/update_categories")
async def update_categories(cats: str = Form(...)):
    db = get_db()
    new_cats = [c.strip() for c in cats.split(",") if c.strip()]
    db["categories"] = new_cats
    save_db(db)
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/auth/google")
async def auth_google(request: Request, credential: str = Form(...)):
    try:
        data = jwt.decode(credential, options={"verify_signature": False})
        request.session["user"] = {"name": data.get("name"), "pic": data.get("picture"), "type": "customer"}
        return RedirectResponse(url="/", status_code=303)
    except: return RedirectResponse(url="/login")

@app.post("/edit_product/{item_id}")
async def edit_product(item_id: int, name: str = Form(...), price: int = Form(...), discount: int = Form(0), category: str = Form(...), image: str = Form(...), stock: str = Form(...)):
    db = get_db()
    for p in db.get("products", []):
        if p["id"] == item_id:
            p.update({"name": name, "price": price, "discount": discount, "category": category, "image": image, "stock": stock})
            break
    save_db(db)
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/add_product")
async def add_product(name: str = Form(...), price: int = Form(...), discount: int = Form(0), category: str = Form(...), image: str = Form(...), stock: str = Form("instock")):
    db = get_db()
    products = db.get("products", [])
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    db["products"].insert(0, {"id": new_id, "name": name, "price": price, "discount": discount, "category": category, "image": image, "stock": stock})
    save_db(db)
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/update_ad")
async def update_ad(title: str = Form(...), price: str = Form(...), image: str = Form(...)):
    db = get_db()
    db["ad"] = {"title": title, "price": price, "image": image}
    save_db(db)
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/delete_all_products")
async def delete_all_products():
    db = get_db()
    db["products"] = []
    save_db(db)
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request): 
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def handle_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        request.session["user"] = {"name": "Admin", "type": "admin"}
        return RedirectResponse(url="/admin", status_code=303)
    return RedirectResponse(url="/login")

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)