from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from database import Base, engine, SessionLocal
from models import URL, Click_count
from fastapi.responses import RedirectResponse
from datetime import datetime
from redistest import r
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



Base.metadata.create_all(engine)

# count = 10006


class URLRequest(BaseModel):
    original: str

def convert(count):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    short_code = ""

    while count != 0:
        short_code = short_code + chars[count % 62]
        count = count // 62

    return short_code    

db = SessionLocal()

last_url = db.query(URL).order_by(URL.id.desc()).first()

count = 10000 + last_url.id

db.close()

@app.get("/")
def home():
    return {"message": "URL Shortener API is running"}


@app.post("/shorten")
def shorten_url(data: URLRequest):

    global count

    db = SessionLocal()

    already_url = db.query(URL).filter(URL.original == data.original).first()

    if already_url != None:
             short_code = already_url.short_url
             db.close()

             return {
             "short_code": short_code,
             "short_url": f"http://127.0.0.1:8000/{short_code}"
            }

    count += 1

    short_code = convert(count)

    new_url = URL(
        original=data.original,
        short_url=short_code,
        create_time = datetime.now()
    )

    db.add(new_url)
    db.commit()

    db.close()

    r.set(short_code, data.original, ex=120)

    return {
        "short_code": short_code,
        "short_url": f"http://127.0.0.1:8000/{short_code}"
    }


@app.get("/{short_code}")
def redirect_url(short_code: str,request: Request):
    
    fast_url = r.get(short_code)

    if fast_url :
        original = fast_url.decode()

        db = SessionLocal()
        url = db.query(URL).filter(URL.short_url == short_code).first()
        click = Click_count(
            url_id=url.id,
            ip_add=request.client.host,
            user_agent=request.headers.get("user-agent"),
            clicktime=datetime.now()
        )

        db.add(click)
        db.commit()
        db.close()
        return RedirectResponse(url=original)
    
    db = SessionLocal()

    url = db.query(URL).filter(URL.short_url == short_code).first()

    if url is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Link not found"
        )
    
    click = Click_count(
        url_id=url.id,
        ip_add=request.client.host,
        user_agent=request.headers.get("user-agent"),
        clicktime=datetime.now()
    )

    db.add(click)
    db.commit()
    
    r.set(short_code, url.original, ex=120)


    original = url.original

    db.close()

    

    # return {"original_url": original}
    return RedirectResponse(url=original)


@app.get("/stats/{short_code}")
def get_click_count(short_code: str):

    db = SessionLocal()

    url = db.query(URL).filter(URL.short_url == short_code).first()

    if url is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Link not found"
        )

    click_count = db.query(Click_count).filter(Click_count.url_id == url.id).count()

    db.close()

    return {
        "click_count": click_count
    }