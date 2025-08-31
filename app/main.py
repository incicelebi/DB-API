from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.model import Clan
from app.db import get_db

app = FastAPI()

# POST /clans - Yeni clan oluştur
@app.post("/clans")
def create_clan(name: str, region: Optional[str] = None, db: Session = Depends(get_db)):
    new_clan = Clan(
        id=uuid.uuid4(),
        name=name,
        region=region
    )
    db.add(new_clan)
    db.commit()
    db.refresh(new_clan)

    return {
        "message": "Clan created successfully.",
        "id": str(new_clan.id)
    }

# GET /clans - Tüm clanları listele, opsiyonel filtre ve sıralama
@app.get("/clans")
def list_clans(
    region: Optional[str] = Query(None, description="Filter by region"),
    sort: Optional[str] = Query(None, description="Sort by created_at, use 'asc' or 'desc'"),
    db: Session = Depends(get_db)
):
    query = db.query(Clan)
    if region:
        query = query.filter(Clan.region == region)
    if sort == "asc":
        query = query.order_by(Clan.created_at.asc())
    elif sort == "desc":
        query = query.order_by(Clan.created_at.desc())
    clans = query.all()

    # JSON’a çevirirken id ve created_at değerlerini string yapalım
    result = []
    for clan in clans:
        result.append({
            "id": str(clan.id),
            "name": clan.name,
            "region": clan.region,
            "created_at": clan.created_at.isoformat() if clan.created_at else None
        })
    return result

# GET /clans/{clan_id} - ID ile clan getir
@app.get("/clans/{clan_id}")
def get_clan(clan_id: str, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    return {
        "id": str(clan.id),
        "name": clan.name,
        "region": clan.region,
        "created_at": clan.created_at.isoformat() if clan.created_at else None
    }

# DELETE /clans/{clan_id} - ID ile clan sil
@app.delete("/clans/{clan_id}")
def delete_clan(clan_id: str, db: Session = Depends(get_db)):
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    db.delete(clan)
    db.commit()
    return {"message": "Clan deleted successfully."}

# Basit root endpoint
@app.get("/")
def root():
    return {"message": "Clan API is running"}