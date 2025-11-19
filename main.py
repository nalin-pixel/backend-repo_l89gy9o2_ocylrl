import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import Batmobile, Gadget

app = FastAPI(title="Batman Gadgets & Batmobiles API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Batman API running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# -------------------- Batmobiles --------------------
@app.get("/api/batmobiles", response_model=List[Batmobile])
def list_batmobiles(limit: Optional[int] = None):
    try:
        docs = get_documents("batmobile", {}, limit)
        # Convert ObjectId to str-safe dict
        for d in docs:
            d.pop("_id", None)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/batmobiles")
def add_batmobile(b: Batmobile):
    try:
        doc_id = create_document("batmobile", b)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Seed many notable Batmobiles across films, animation, games
@app.post("/api/seed/batmobiles")
def seed_batmobiles():
    seed: List[Batmobile] = [
        Batmobile(name="Serial Roadster", year=1943, media="Film Serial", title="Batman (1943)", universe="Film", era="Golden Age", description="Black 1939 Cadillac Series 61 used in the original serial.", image_url="https://images.unsplash.com/photo-1483721310020-03333e577078?q=80&w=1600&auto=format&fit=crop", specs=["Straight-8 engine", "Concealed plates"]),
        Batmobile(name="Serial Sedan", year=1949, media="Film Serial", title="Batman and Robin (1949)", universe="Film", era="Golden Age", description="Stock 1949 Mercury Convertible standing in as the Batmobile.", image_url="https://images.unsplash.com/photo-1502877338535-766e1452684a?q=80&w=1600&auto=format&fit=crop", specs=["Mercury V8", "Convertible"]),
        Batmobile(name="1966 TV Batmobile", year=1966, media="TV", title="Batman (1966 TV)", universe="TV", era="Silver Age", designer="George Barris", description="Iconic Lincoln Futura-based Batmobile with red pinstripes and gadgets.", image_url="https://images.unsplash.com/photo-1523986371872-9d3ba2e2f642?q=80&w=1600&auto=format&fit=crop", specs=["Batphone", "Parachute deployment", "Flamethrower"]),
        Batmobile(name="Burton Batmobile", year=1989, media="Film", title="Batman (1989)", universe="Film", era="Burtonverse", description="Art-deco jet-turbine Batmobile with grappling hook and armor cocoon.", image_url="https://images.unsplash.com/photo-1619767886558-efdc259cde1a?q=80&w=1600&auto=format&fit=crop", specs=["Jet turbine", "Grapple turn", "Armor cocoon"]),
        Batmobile(name="Returns Batmobile", year=1992, media="Film", title="Batman Returns (1992)", universe="Film", era="Burtonverse", description="Updated 1989 design with shields and Batmissile escape mode.", image_url="https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?q=80&w=1600&auto=format&fit=crop", specs=["Shields", "Batmissile mode"]),
        Batmobile(name="Forever Batmobile", year=1995, media="Film", title="Batman Forever (1995)", universe="Film", era="Schumacher", description="Ribbed fins, exposed blue lighting, single rear fin.", image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=1600&auto=format&fit=crop", specs=["Blue underglow", "Grapple wheel"]),
        Batmobile(name="Batman & Robin Batmobile", year=1997, media="Film", title="Batman & Robin (1997)", universe="Film", era="Schumacher", description="Open-cockpit neon-lit Batmobile with elongated nose.", image_url="https://images.unsplash.com/photo-1511919884226-fd3cad34687c?q=80&w=1600&auto=format&fit=crop", specs=["Exposed engine", "Neon accents"]),
        Batmobile(name="Tumbler (Begins)", year=2005, media="Film", title="Batman Begins (2005)", universe="Film", era="Nolan", description="Military prototype bridging tank and supercar; jump capability.", image_url="https://images.unsplash.com/photo-1580273916550-e323be2ae537?q=80&w=1600&auto=format&fit=crop", specs=["Stealth mode", "Jump pack", "Afterburner"]),
        Batmobile(name="Tumbler (TDK)", year=2008, media="Film", title="The Dark Knight (2008)", universe="Film", era="Nolan", description="Up-armored Tumbler; spawns the Batpod on self-destruct.", image_url="https://images.unsplash.com/photo-1502877338535-766e1452684a?q=80&w=1600&auto=format&fit=crop", specs=["Reactive armor", "Batpod deployment"]),
        Batmobile(name="Tumbler (TDKR)", year=2012, media="Film", title="The Dark Knight Rises (2012)", universe="Film", era="Nolan", description="Multiple Tumblers in camo; commandeered by Bane's men.", image_url="https://images.unsplash.com/photo-1619767886558-efdc259cde1a?q=80&w=1600&auto=format&fit=crop", specs=["Camo variants", "Heavy weapons"]),
        Batmobile(name="Snyder Batmobile", year=2016, media="Film", title="Batman v Superman (2016)", universe="Film", era="DCEU", description="Hybrid of racer and armored assault vehicle.", image_url="https://images.unsplash.com/photo-1550355291-bbee04a92027?q=80&w=1600&auto=format&fit=crop", specs=["Miniguns", "Ramming prow"]),
        Batmobile(name="Justice League Batmobile", year=2017, media="Film", title="Justice League (2017)", universe="Film", era="DCEU", description="Upgraded with heavy weaponry and shields.", image_url="https://images.unsplash.com/photo-1549924231-f129b911e442?q=80&w=1600&auto=format&fit=crop", specs=["Rocket pods", "Shielding"]),
        Batmobile(name="The Batman Muscle Car", year=2022, media="Film", title="The Batman (2022)", universe="Film", era="Reeves", description="Brutalist, DIY muscle-car Batmobile with exposed V8 and roll cage.", image_url="https://images.unsplash.com/photo-1502877338535-766e1452684a?q=80&w=1600&auto=format&fit=crop", specs=["Supercharged V8", "Roll cage", "Rear thruster"]),
        Batmobile(name="BTAS Batmobile", year=1992, media="Animation", title="Batman: The Animated Series", universe="Animated", era="DCAU", description="Long-nosed art-deco Batmobile from the animated series.", image_url="https://images.unsplash.com/photo-1511300636408-a63a89df3482?q=80&w=1600&auto=format&fit=crop", specs=["Grapple", "Smoke screen"]),
        Batmobile(name="TNBA Batmobile", year=1997, media="Animation", title="The New Batman Adventures", universe="Animated", era="DCAU", description="Streamlined update to the BTAS design.", image_url="https://images.unsplash.com/photo-1549924231-f129b911e442?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="Batman Beyond", year=1999, media="Animation", title="Batman Beyond", universe="Animated", era="DCAU", description="Futuristic flying Batmobile used by Terry McGinnis.", image_url="https://images.unsplash.com/photo-1550355291-bbee04a92027?q=80&w=1600&auto=format&fit=crop", specs=["VTOL", "Stealth cloak"]),
        Batmobile(name="The Batman (2004) Batmobile", year=2004, media="Animation", title="The Batman (2004)", universe="Animated", era="Animated", description="Sleek blue-lit coupe evolving into a more aggressive design.", image_url="https://images.unsplash.com/photo-1511919884226-fd3cad34687c?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="Beware the Batman", year=2013, media="Animation", title="Beware the Batman", universe="Animated", era="Animated", description="CG stylized stealth car with angular design.", image_url="https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="Arkham Knight Batmobile", year=2015, media="Game", title="Batman: Arkham Knight", universe="Game", era="Arkham", description="Transforming pursuit/tank mode Batmobile central to gameplay.", image_url="https://images.unsplash.com/photo-1550355291-bbee04a92027?q=80&w=1600&auto=format&fit=crop", specs=["Battle mode", "EMP", "Non-lethal rounds"]),
        Batmobile(name="Arkham Asylum Batmobile", year=2009, media="Game", title="Batman: Arkham Asylum", universe="Game", era="Arkham", description="Aggressive supercar aesthetic seen in cutscenes.", image_url="https://images.unsplash.com/photo-1619767886558-efdc259cde1a?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="Arkham City Batmobile", year=2011, media="Game", title="Batman: Arkham City", universe="Game", era="Arkham", description="Refined version glimpsed in promotional materials.", image_url="https://images.unsplash.com/photo-1502877338535-766e1452684a?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="The Telltale Batmobile", year=2016, media="Game", title="Batman: The Telltale Series", universe="Game", era="Game", description="Morphing car with stealth tech, seen in cinematics.", image_url="https://images.unsplash.com/photo-1549924231-f129b911e442?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="LEGO Batman Batmobile", year=2008, media="Game", title="LEGO Batman series", universe="Game", era="LEGO", description="Blocky stylized Batmobile from LEGO games.", image_url="https://images.unsplash.com/photo-1511300636408-a63a89df3482?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="Gotham Knight Batcycle (not a Batmobile)", year=2022, media="Game", title="Gotham Knights", universe="Game", era="Game", description="Primary ride is a Batcycle; included for reference.", image_url="https://images.unsplash.com/photo-1523986371872-9d3ba2e2f642?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="Justice League Animated", year=2001, media="Animation", title="Justice League / Unlimited", universe="Animated", era="DCAU", description="Occasional appearances of team-era Batmobile.", image_url="https://images.unsplash.com/photo-1542596768-5d1d21f1cf98?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="Batman: Brave and the Bold", year=2008, media="Animation", title="Batman: The Brave and the Bold", universe="Animated", era="Animated", description="Retro-inspired convertible variants across episodes.", image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=1600&auto=format&fit=crop"),
        Batmobile(name="Gotham TV Proto", year=2014, media="TV", title="Gotham", universe="TV", era="Prequel", description="Pre-Batman era vehicles hinting at future design.", image_url="https://images.unsplash.com/photo-1549924231-f129b911e442?q=80&w=1600&auto=format&fit=crop"),
    ]
    inserted = 0
    for item in seed:
        try:
            create_document("batmobile", item)
            inserted += 1
        except Exception:
            pass
    return {"ok": True, "inserted": inserted}

# -------------------- Gadgets --------------------
@app.get("/api/gadgets", response_model=List[Gadget])
def list_gadgets(limit: Optional[int] = None):
    try:
        docs = get_documents("gadget", {}, limit)
        for d in docs:
            d.pop("_id", None)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/gadgets")
def add_gadget(g: Gadget):
    try:
        doc_id = create_document("gadget", g)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/seed/gadgets")
def seed_gadgets():
    seed: List[Gadget] = [
        Gadget(name="Batarang", category="Offensive", description="Razor-edged bat-shaped throwing weapon; multiple variants including remote and explosive.", image_url="https://images.unsplash.com/photo-1599240516991-b40a6e2317f6?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Grapnel Gun", category="Mobility", description="Compressed CO2 grappling launcher for rapid ascents and swings.", image_url="https://images.unsplash.com/photo-1612198185725-055f3e8bd477?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Smoke Pellets", category="Stealth", description="Magnesium-tetrachloride pellets to create instant smoke cover.", image_url="https://images.unsplash.com/photo-1520975922284-6eb2a18b9a71?q=80&w=1600&auto=format&fit=crop"),\
        Gadget(name="Explosive Gel", category="Demolition", description="Foaming explosive compound forming bat-symbol charge; popularized in Arkham games.", image_url="https://images.unsplash.com/photo-1506806732259-39c2d0268443?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Cryptographic Sequencer", category="Forensics", description="Handheld device for hacking and frequency scanning.", image_url="https://images.unsplash.com/photo-1542751110-97427bbecf20?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Batclaw", category="Utility", description="Retractable claw for pulling objects and enemies.", image_url="https://images.unsplash.com/photo-1612198185725-055f3e8bd477?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Line Launcher", category="Mobility", description="Fires a taut line between two points for horizontal traversal.", image_url="https://images.unsplash.com/photo-1600111760418-03230cf37d34?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="EMP Device", category="Utility", description="Electromagnetic pulse tool to disable electronics temporarily.", image_url="https://images.unsplash.com/photo-1529245857260-427e03f69c4b?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Glue Grenade", category="Utility", description="Deploys expanding polymer to immobilize targets (Arkham Origin).", image_url="https://images.unsplash.com/photo-1520975922284-6eb2a18b9a71?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Thermal Vision Cowl", category="Forensics", description="Enhanced detective vision overlay for crime scene analysis.", image_url="https://images.unsplash.com/photo-1545665277-5937489579f3?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Shock Gloves", category="Offensive", description="Capacitive gauntlets delivering stunning charges.", image_url="https://images.unsplash.com/photo-1511735111819-9a3f7709049c?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Rebreather", category="Survival", description="Compact oxygen supply for underwater operations.", image_url="https://images.unsplash.com/photo-1516298252535-cf2ac5147ffa?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Sticky Bomb Gun", category="Offensive", description="Launches adhesive explosive charges (The Dark Knight).", image_url="https://images.unsplash.com/photo-1511735111819-9a3f7709049c?q=80&w=1600&auto=format&fit=crop"),
        Gadget(name="Bat-sonar", category="Surveillance", description="Wide-area cell phone sonar mapping system (The Dark Knight).", image_url="https://images.unsplash.com/photo-1545665277-5937489579f3?q=80&w=1600&auto=format&fit=crop"),
    ]
    inserted = 0
    for item in seed:
        try:
            create_document("gadget", item)
            inserted += 1
        except Exception:
            pass
    return {"ok": True, "inserted": inserted}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
