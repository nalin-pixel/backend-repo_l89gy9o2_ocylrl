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
        Batmobile(name="Serial Roadster", year=1943, media="Film Serial", title="Batman (1943)", universe="Film", era="Golden Age", description="Black 1939 Cadillac Series 61 used in the original serial."),
        Batmobile(name="Serial Sedan", year=1949, media="Film Serial", title="Batman and Robin (1949)", universe="Film", era="Golden Age", description="Stock 1949 Mercury Convertible standing in as the Batmobile."),
        Batmobile(name="1966 TV Batmobile", year=1966, media="TV", title="Batman (1966 TV)", universe="TV", era="Silver Age", designer="George Barris", description="Iconic Lincoln Futura-based Batmobile with red pinstripes and gadgets."),
        Batmobile(name="Burton Batmobile", year=1989, media="Film", title="Batman (1989)", universe="Film", era="Burtonverse", description="Art-deco jet-turbine Batmobile with grappling hook and armor cocoon."),
        Batmobile(name="Returns Batmobile", year=1992, media="Film", title="Batman Returns (1992)", universe="Film", era="Burtonverse", description="Updated 1989 design with shields and Batmissile escape mode."),
        Batmobile(name="Forever Batmobile", year=1995, media="Film", title="Batman Forever (1995)", universe="Film", era="Schumacher", description="Ribbed fins, exposed blue lighting, single rear fin."),
        Batmobile(name="Batman & Robin Batmobile", year=1997, media="Film", title="Batman & Robin (1997)", universe="Film", era="Schumacher", description="Open-cockpit neon-lit Batmobile with elongated nose."),
        Batmobile(name="Tumbler (Begins)", year=2005, media="Film", title="Batman Begins (2005)", universe="Film", era="Nolan", description="Military prototype bridging tank and supercar; jump capability."),
        Batmobile(name="Tumbler (TDK)", year=2008, media="Film", title="The Dark Knight (2008)", universe="Film", era="Nolan", description="Up-armored Tumbler; spawns the Batpod on self-destruct."),
        Batmobile(name="Tumbler (TDKR)", year=2012, media="Film", title="The Dark Knight Rises (2012)", universe="Film", era="Nolan", description="Multiple Tumblers in camo; commandeered by Bane's men."),
        Batmobile(name="Snyder Batmobile", year=2016, media="Film", title="Batman v Superman (2016)", universe="Film", era="DCEU", description="Hybrid of racer and armored assault vehicle."),
        Batmobile(name="Justice League Batmobile", year=2017, media="Film", title="Justice League (2017)", universe="Film", era="DCEU", description="Upgraded with heavy weaponry and shields."),
        Batmobile(name="The Batman Muscle Car", year=2022, media="Film", title="The Batman (2022)", universe="Film", era="Reeves", description="Brutalist, DIY muscle-car Batmobile with exposed V8 and roll cage."),
        Batmobile(name="BTAS Batmobile", year=1992, media="Animation", title="Batman: The Animated Series", universe="Animated", era="DCAU", description="Long-nosed art-deco Batmobile from the animated series."),
        Batmobile(name="TNBA Batmobile", year=1997, media="Animation", title="The New Batman Adventures", universe="Animated", era="DCAU", description="Streamlined update to the BTAS design."),
        Batmobile(name="Batman Beyond", year=1999, media="Animation", title="Batman Beyond", universe="Animated", era="DCAU", description="Futuristic flying Batmobile used by Terry McGinnis."),
        Batmobile(name="The Batman (2004) Batmobile", year=2004, media="Animation", title="The Batman (2004)", universe="Animated", era="Animated", description="Sleek blue-lit coupe evolving into a more aggressive design."),
        Batmobile(name="Beware the Batman", year=2013, media="Animation", title="Beware the Batman", universe="Animated", era="Animated", description="CG stylized stealth car with angular design."),
        Batmobile(name="Arkham Knight Batmobile", year=2015, media="Game", title="Batman: Arkham Knight", universe="Game", era="Arkham", description="Transforming pursuit/tank mode Batmobile central to gameplay."),
        Batmobile(name="Arkham Asylum Batmobile", year=2009, media="Game", title="Batman: Arkham Asylum", universe="Game", era="Arkham", description="Aggressive supercar aesthetic seen in cutscenes."),
        Batmobile(name="Arkham City Batmobile", year=2011, media="Game", title="Batman: Arkham City", universe="Game", era="Arkham", description="Refined version glimpsed in promotional materials."),
        Batmobile(name="The Telltale Batmobile", year=2016, media="Game", title="Batman: The Telltale Series", universe="Game", era="Game", description="Morphing car with stealth tech, seen in cinematics."),
        Batmobile(name="LEGO Batman Batmobile", year=2008, media="Game", title="LEGO Batman series", universe="Game", era="LEGO", description="Blocky stylized Batmobile from LEGO games."),
        Batmobile(name="Gotham Knight Batcycle (not a Batmobile)", year=2022, media="Game", title="Gotham Knights", universe="Game", era="Game", description="Primary ride is a Batcycle; included for reference."),
        Batmobile(name="Justice League Animated", year=2001, media="Animation", title="Justice League / Unlimited", universe="Animated", era="DCAU", description="Occasional appearances of team-era Batmobile."),
        Batmobile(name="Batman: Brave and the Bold", year=2008, media="Animation", title="Batman: The Brave and the Bold", universe="Animated", era="Animated", description="Retro-inspired convertible variants across episodes."),
        Batmobile(name="Gotham TV Proto", year=2014, media="TV", title="Gotham", universe="TV", era="Prequel", description="Pre-Batman era vehicles hinting at future design."),
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
        Gadget(name="Batarang", category="Offensive", description="Razor-edged bat-shaped throwing weapon; multiple variants including remote and explosive."),
        Gadget(name="Grapnel Gun", category="Mobility", description="Compressed CO2 grappling launcher for rapid ascents and swings."),
        Gadget(name="Smoke Pellets", category="Stealth", description="Magnesium-tetrachloride pellets to create instant smoke cover."),
        Gadget(name="Explosive Gel", category="Demolition", description="Foaming explosive compound forming bat-symbol charge; popularized in Arkham games."),
        Gadget(name="Cryptographic Sequencer", category="Forensics", description="Handheld device for hacking and frequency scanning."),
        Gadget(name="Batclaw", category="Utility", description="Retractable claw for pulling objects and enemies."),
        Gadget(name="Line Launcher", category="Mobility", description="Fires a taut line between two points for horizontal traversal."),
        Gadget(name="EMP Device", category="Utility", description="Electromagnetic pulse tool to disable electronics temporarily."),
        Gadget(name="Glue Grenade", category="Utility", description="Deploys expanding polymer to immobilize targets (Arkham Origin)."),
        Gadget(name="Thermal Vision Cowl", category="Forensics", description="Enhanced detective vision overlay for crime scene analysis."),
        Gadget(name="Shock Gloves", category="Offensive", description="Capacitive gauntlets delivering stunning charges."),
        Gadget(name="Rebreather", category="Survival", description="Compact oxygen supply for underwater operations."),
        Gadget(name="Sticky Bomb Gun", category="Offensive", description="Launches adhesive explosive charges (The Dark Knight)."),
        Gadget(name="Bat-sonar", category="Surveillance", description="Wide-area cell phone sonar mapping system (The Dark Knight)."),
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
