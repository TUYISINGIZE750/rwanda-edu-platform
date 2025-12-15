from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.school import School
from pydantic import BaseModel


router = APIRouter(prefix="/locations", tags=["locations"])

class ProvinceResponse(BaseModel):
    name: str

class DistrictResponse(BaseModel):
    name: str

class SectorResponse(BaseModel):
    name: str

class SchoolResponse(BaseModel):
    id: int
    school_code: str = None
    name: str
    type: str
    category: str
    province: str
    district: str
    trades_full: List[str] = []
    trades_short: List[str] = []
    gender: str = None
    
    @classmethod
    def from_orm(cls, obj):
        import json
        trades_full = []
        trades_short = []
        
        if hasattr(obj, 'trades_full') and obj.trades_full:
            try:
                if isinstance(obj.trades_full, str):
                    trades_full = json.loads(obj.trades_full)
                elif isinstance(obj.trades_full, list):
                    trades_full = obj.trades_full
            except (json.JSONDecodeError, TypeError):
                trades_full = []
        
        if hasattr(obj, 'trades_short') and obj.trades_short:
            try:
                if isinstance(obj.trades_short, str):
                    trades_short = json.loads(obj.trades_short)
                elif isinstance(obj.trades_short, list):
                    trades_short = obj.trades_short
            except (json.JSONDecodeError, TypeError):
                trades_short = []
        
        return cls(
            id=obj.id,
            school_code=getattr(obj, 'school_code', None),
            name=obj.name,
            type=obj.type,
            category=obj.category,
            province=obj.province,
            district=obj.district,
            trades_full=trades_full,
            trades_short=trades_short,
            gender=getattr(obj, 'gender', None)
        )
    
    class Config:
        from_attributes = True

# Rwanda locations data
RWANDA_DATA = {
    "provinces": [
        {
            "name": "Kigali City",
            "districts": [
                {
                    "name": "Gasabo",
                    "sectors": [
                        {"name": "Bumbogo"}, {"name": "Gatsata"}, {"name": "Gikomero"}, {"name": "Gisozi"}, {"name": "Jabana"}, 
                        {"name": "Jali"}, {"name": "Kacyiru"}, {"name": "Kimihurura"}, {"name": "Kimironko"}, {"name": "Kinyinya"}, 
                        {"name": "Ndera"}, {"name": "Nduba"}, {"name": "Remera"}, {"name": "Rusororo"}, {"name": "Rutunga"}
                    ]
                },
                {
                    "name": "Kicukiro",
                    "sectors": [
                        {"name": "Gahanga"}, {"name": "Gatenga"}, {"name": "Gikondo"}, {"name": "Kagarama"}, {"name": "Kanombe"}, 
                        {"name": "Kicukiro"}, {"name": "Kigarama"}, {"name": "Masaka"}, {"name": "Niboye"}, {"name": "Nyarugunga"}
                    ]
                },
                {
                    "name": "Nyarugenge",
                    "sectors": [
                        {"name": "Gitega"}, {"name": "Kanyinya"}, {"name": "Kigali"}, {"name": "Kimisagara"}, {"name": "Mageragere"}, 
                        {"name": "Muhima"}, {"name": "Nyakabanda"}, {"name": "Nyamirambo"}, {"name": "Nyarugenge"}, {"name": "Rwezamenyo"}
                    ]
                }
            ]
        },
        {
            "name": "Southern Province",
            "districts": [
                {"name": "Gisagara", "sectors": [{"name": "Gishubi"}, {"name": "Kansi"}, {"name": "Kibirizi"}, {"name": "Kigembe"}, {"name": "Mukindo"}, {"name": "Mamba"}, {"name": "Muganza"}, {"name": "Mugombwa"}, {"name": "Ndora"}, {"name": "Nyanza"}, {"name": "Save"}, {"name": "Shyogwe"}]},
                {"name": "Huye", "sectors": [{"name": "Gishamvu"}, {"name": "Karama"}, {"name": "Kigoma"}, {"name": "Kinazi"}, {"name": "Maraba"}, {"name": "Mbazi"}, {"name": "Mukura"}, {"name": "Ngoma"}, {"name": "Ruhashya"}, {"name": "Rusatira"}, {"name": "Rwaniro"}, {"name": "Simbi"}, {"name": "Tumba"}]},
                {"name": "Kamonyi", "sectors": [{"name": "Gacurabwenge"}, {"name": "Kamonyi"}, {"name": "Kayenzi"}, {"name": "Kayumbu"}, {"name": "Mugina"}, {"name": "Musambira"}, {"name": "Nyamiyaga"}, {"name": "Nyarubaka"}, {"name": "Rugalika"}, {"name": "Runda"}, {"name": "Ruzo"}]},
                {"name": "Muhanga", "sectors": [{"name": "Cyeza"}, {"name": "Kabacuzi"}, {"name": "Kibangu"}, {"name": "Kiyumba"}, {"name": "Muhanga"}, {"name": "Mukura"}, {"name": "Nyabinoni"}, {"name": "Nyamabuye"}, {"name": "Nyamiyaga"}, {"name": "Rongi"}, {"name": "Rugendabari"}, {"name": "Shyogwe"}]},
                {"name": "Nyamagabe", "sectors": [{"name": "Buruhukiro"}, {"name": "Cyanika"}, {"name": "Gasaka"}, {"name": "Gatare"}, {"name": "Kaduha"}, {"name": "Kamegeri"}, {"name": "Kibirizi"}, {"name": "Kibumbwe"}, {"name": "Kitabi"}, {"name": "Mbazi"}, {"name": "Musebeya"}, {"name": "Mushubi"}, {"name": "Nkomane"}, {"name": "Tare"}, {"name": "Uwinkingi"}]},
                {"name": "Nyanza", "sectors": [{"name": "Busasamana"}, {"name": "Busoro"}, {"name": "Cyabakamyi"}, {"name": "Kibirizi"}, {"name": "Kigoma"}, {"name": "Mukingo"}, {"name": "Muyira"}, {"name": "Ntyazo"}, {"name": "Nyagisozi"}, {"name": "Rwabicuma"}]},
                {"name": "Nyaruguru", "sectors": [{"name": "Cyahinda"}, {"name": "Gatare"}, {"name": "Kibeho"}, {"name": "Kibumbwe"}, {"name": "Munini"}, {"name": "Ngera"}, {"name": "Ngoma"}, {"name": "Nyabimata"}, {"name": "Nyagisozi"}, {"name": "Ruheru"}, {"name": "Rusenge"}, {"name": "Rwabicuma"}, {"name": "Simbi"}]},
                {"name": "Ruhango", "sectors": [{"name": "Bweramana"}, {"name": "Byimana"}, {"name": "Kabagali"}, {"name": "Kinazi"}, {"name": "Kinihira"}, {"name": "Mbuye"}, {"name": "Ntongwe"}, {"name": "Ruhango"}]}
            ]
        },
        {
            "name": "Western Province",
            "districts": [
                {"name": "Karongi", "sectors": [{"name": "Bwishyura"}, {"name": "Gishyita"}, {"name": "Karongi"}, {"name": "Mugesera"}, {"name": "Mutuntu"}, {"name": "Rwankuba"}]},
                {"name": "Nyabihu", "sectors": [{"name": "Bigogwe"}, {"name": "Jenda"}, {"name": "Jomba"}, {"name": "Kabatwa"}, {"name": "Karago"}, {"name": "Kintobo"}, {"name": "Mukamira"}, {"name": "Rambura"}, {"name": "Rugera"}, {"name": "Rurembo"}, {"name": "Shyira"}]},
                {"name": "Ngororero", "sectors": [{"name": "Bwira"}, {"name": "Gatumba"}, {"name": "Hindiro"}, {"name": "Kabaya"}, {"name": "Kageyo"}, {"name": "Kavumu"}, {"name": "Matyazo"}, {"name": "Muhanda"}, {"name": "Muhororo"}, {"name": "Ndaro"}, {"name": "Ngororero"}, {"name": "Nyange"}, {"name": "Sovu"}]},
                {"name": "Rubavu", "sectors": [{"name": "Bugeshi"}, {"name": "Busasamana"}, {"name": "Cyanzarwe"}, {"name": "Gisenyi"}, {"name": "Kanama"}, {"name": "Kanzenze"}, {"name": "Mudende"}, {"name": "Nyakiliba"}, {"name": "Nyamyumba"}, {"name": "Rubavu"}, {"name": "Rugerero"}]},
                {"name": "Rusizi", "sectors": [{"name": "Butare"}, {"name": "Bugarama"}, {"name": "Gashonga"}, {"name": "Giheke"}, {"name": "Gihundwe"}, {"name": "Gitambi"}, {"name": "Kamembe"}, {"name": "Muganza"}, {"name": "Mururu"}, {"name": "Nkanka"}, {"name": "Nkombo"}, {"name": "Nkungu"}, {"name": "Nyakabuye"}, {"name": "Nyakarenzo"}, {"name": "Rwimbogo"}]},
                {"name": "Nyamasheke", "sectors": [{"name": "Bangwe"}, {"name": "Bushekeri"}, {"name": "Bushenge"}, {"name": "Cyato"}, {"name": "Gihombo"}, {"name": "Kagano"}, {"name": "Karambi"}, {"name": "Karengera"}, {"name": "Kirimbi"}, {"name": "Macuba"}, {"name": "Mahembe"}, {"name": "Nyabitekeri"}, {"name": "Rangiro"}, {"name": "Ruharambuga"}, {"name": "Shangi"}]},
                {"name": "Rutsiro", "sectors": [{"name": "Boneza"}, {"name": "Gihango"}, {"name": "Kigeyo"}, {"name": "Kivumu"}, {"name": "Manihira"}, {"name": "Mukura"}, {"name": "Musasa"}, {"name": "Mushonyi"}, {"name": "Mushubati"}, {"name": "Nyabirasi"}, {"name": "Ruhango"}, {"name": "Rusebeya"}]}
            ]
        },
        {
            "name": "Northern Province",
            "districts": [
                {"name": "Burera", "sectors": [{"name": "Bungwe"}, {"name": "Butaro"}, {"name": "Cyanika"}, {"name": "Cyeru"}, {"name": "Gahunga"}, {"name": "Gatebe"}, {"name": "Gitovu"}, {"name": "Kagogo"}, {"name": "Kinoni"}, {"name": "Kinyababa"}, {"name": "Kivuye"}, {"name": "Nemba"}, {"name": "Rugarama"}, {"name": "Rugendabari"}, {"name": "Ruhunde"}, {"name": "Rusarabuye"}, {"name": "Rwerere"}]},
                {"name": "Gakenke", "sectors": [{"name": "Busengo"}, {"name": "Coko"}, {"name": "Cyabingo"}, {"name": "Gakenke"}, {"name": "Gashenyi"}, {"name": "Mugunga"}, {"name": "Janja"}, {"name": "Kamubuga"}, {"name": "Karambo"}, {"name": "Kivuruga"}, {"name": "Mataba"}, {"name": "Minazi"}, {"name": "Muhondo"}, {"name": "Muyongwe"}, {"name": "Muzo"}, {"name": "Nemba"}, {"name": "Ruli"}, {"name": "Rusasa"}, {"name": "Rushashi"}]},
                {"name": "Gicumbi", "sectors": [{"name": "Bukure"}, {"name": "Bwisige"}, {"name": "Byumba"}, {"name": "Cyumba"}, {"name": "Gicumbi"}, {"name": "Kageyo"}, {"name": "Kaniga"}, {"name": "Manyagiro"}, {"name": "Miyove"}, {"name": "Muko"}, {"name": "Mutete"}, {"name": "Nyamiyaga"}, {"name": "Nyankenke"}, {"name": "Rubaya"}, {"name": "Rukomo"}, {"name": "Rushaki"}, {"name": "Rutare"}, {"name": "Ruvune"}, {"name": "Rwamiko"}, {"name": "Shangasha"}]},
                {"name": "Musanze", "sectors": [{"name": "Busogo"}, {"name": "Cyuve"}, {"name": "Gacaca"}, {"name": "Gashaki"}, {"name": "Gataraga"}, {"name": "Kimonyi"}, {"name": "Kinigi"}, {"name": "Muhoza"}, {"name": "Muko"}, {"name": "Musanze"}, {"name": "Nkotsi"}, {"name": "Nyange"}, {"name": "Remera"}, {"name": "Rwaza"}, {"name": "Shingiro"}]},
                {"name": "Rulindo", "sectors": [{"name": "Base"}, {"name": "Burega"}, {"name": "Bushoki"}, {"name": "Cyinzuzi"}, {"name": "Cyungo"}, {"name": "Kinihira"}, {"name": "Kisaro"}, {"name": "Masoro"}, {"name": "Mbogo"}, {"name": "Murambi"}, {"name": "Ngoma"}, {"name": "Ntarabana"}, {"name": "Rukozo"}, {"name": "Rulindo"}, {"name": "Rusiga"}, {"name": "Shyorongi"}, {"name": "Tumba"}]}
            ]
        },
        {
            "name": "Eastern Province",
            "districts": [
                {"name": "Bugesera", "sectors": [{"name": "Gashora"}, {"name": "Juru"}, {"name": "Kamabuye"}, {"name": "Mareba"}, {"name": "Mayange"}, {"name": "Musenyi"}, {"name": "Mwogo"}, {"name": "Ngeruka"}, {"name": "Ntarama"}, {"name": "Nyamata"}, {"name": "Nyarugenge"}, {"name": "Rilima"}, {"name": "Ruhuha"}, {"name": "Rweru"}, {"name": "Shyara"}]},
                {"name": "Gatsibo", "sectors": [{"name": "Gasange"}, {"name": "Gatsibo"}, {"name": "Gitoki"}, {"name": "Kabarore"}, {"name": "Kageyo"}, {"name": "Kiramuruzi"}, {"name": "Kiziguro"}, {"name": "Muhura"}, {"name": "Murambi"}, {"name": "Ngarama"}, {"name": "Nyagihanga"}, {"name": "Remera"}, {"name": "Rugarama"}, {"name": "Rwimbogo"}]},
                {"name": "Kayonza", "sectors": [{"name": "Gahini"}, {"name": "Kabare"}, {"name": "Kabarondo"}, {"name": "Mukarange"}, {"name": "Murama"}, {"name": "Murundi"}, {"name": "Mwiri"}, {"name": "Ndego"}, {"name": "Nyamirama"}, {"name": "Rukara"}, {"name": "Ruramira"}, {"name": "Rwinkwavu"}]},
                {"name": "Kirehe", "sectors": [{"name": "Gatore"}, {"name": "Kigarama"}, {"name": "Kigina"}, {"name": "Kirehe"}, {"name": "Mahama"}, {"name": "Mpanga"}, {"name": "Musaza"}, {"name": "Mushikiri"}, {"name": "Nasho"}, {"name": "Nyamugali"}, {"name": "Nyarubuye"}]},
                {"name": "Ngoma", "sectors": [{"name": "Gashanda"}, {"name": "Jarama"}, {"name": "Karembo"}, {"name": "Kazo"}, {"name": "Mugesera"}, {"name": "Murama"}, {"name": "Mutenderi"}, {"name": "Remera"}, {"name": "Rukira"}, {"name": "Rukumberi"}, {"name": "Sake"}, {"name": "Zaza"}]},
                {"name": "Nyagatare", "sectors": [{"name": "Gatunda"}, {"name": "Karama"}, {"name": "Karangazi"}, {"name": "Katabagemu"}, {"name": "Kiyombe"}, {"name": "Matimba"}, {"name": "Mimuli"}, {"name": "Mukama"}, {"name": "Musheri"}, {"name": "Nyagatare"}, {"name": "Rukomo"}, {"name": "Rwempasha"}, {"name": "Rwimiyaga"}, {"name": "Tabagwe"}]},
                {"name": "Rwamagana", "sectors": [{"name": "Fumbwe"}, {"name": "Gahengeri"}, {"name": "Gishari"}, {"name": "Karenge"}, {"name": "Kigabiro"}, {"name": "Muhazi"}, {"name": "Munyaga"}, {"name": "Munyiginya"}, {"name": "Musha"}, {"name": "Muyumbu"}, {"name": "Mwulire"}, {"name": "Nyakaliro"}, {"name": "Nzige"}, {"name": "Rubona"}, {"name": "Rwamagana"}]}
            ]
        }
    ]
}

@router.get("/provinces", response_model=List[ProvinceResponse])
def get_provinces():
    """Get all provinces in Rwanda"""
    provinces = RWANDA_DATA.get("provinces", [])
    return [{"name": province["name"]} for province in provinces]

@router.get("/districts/{province_name}", response_model=List[DistrictResponse])
def get_districts(province_name: str):
    """Get all districts in a province"""
    from urllib.parse import unquote
    province_name = unquote(province_name)
    provinces = RWANDA_DATA.get("provinces", [])
    for province in provinces:
        if province["name"] == province_name:
            districts = province.get("districts", [])
            return [{"name": district["name"]} for district in districts]
    raise HTTPException(status_code=404, detail=f"Province '{province_name}' not found")

@router.get("/sectors/{province_name}/{district_name}", response_model=List[SectorResponse])
def get_sectors(province_name: str, district_name: str):
    """Get all sectors in a district"""
    from urllib.parse import unquote
    print(f"DEBUG: Raw params - province: '{province_name}', district: '{district_name}'")
    province_name = unquote(province_name)
    district_name = unquote(district_name)
    print(f"DEBUG: Decoded params - province: '{province_name}', district: '{district_name}'")
    
    provinces = RWANDA_DATA.get("provinces", [])
    print(f"DEBUG: Available provinces: {[p['name'] for p in provinces]}")
    
    for province in provinces:
        if province["name"] == province_name:
            print(f"DEBUG: Found province '{province_name}'")
            districts = province.get("districts", [])
            print(f"DEBUG: Available districts: {[d['name'] for d in districts]}")
            for district in districts:
                if district["name"] == district_name:
                    print(f"DEBUG: Found district '{district_name}'")
                    sectors = district.get("sectors", [])
                    return [{"name": sector["name"]} for sector in sectors]
            print(f"DEBUG: District '{district_name}' not found")
            break
    else:
        print(f"DEBUG: Province '{province_name}' not found")
    
    raise HTTPException(status_code=404, detail=f"District '{district_name}' not found in province '{province_name}'")

@router.get("/schools/district/{province_name}/{district_name}", response_model=List[SchoolResponse])
def get_schools_by_district(
    province_name: str,
    district_name: str,
    db: Session = Depends(get_db)
):
    """Get all TVET/TSS schools in a district"""
    from urllib.parse import unquote
    from sqlalchemy import func
    province_name = unquote(province_name)
    district_name = unquote(district_name)
    
    # Case-insensitive matching for both province and district
    schools = db.query(School).filter(
        func.lower(School.province) == province_name.lower(),
        func.lower(School.district) == district_name.lower()
    ).all()
    return [SchoolResponse.from_orm(school) for school in schools]

@router.get("/schools/sector/{province_name}/{district_name}/{sector_name}", response_model=List[SchoolResponse])
def get_schools_by_sector(
    province_name: str,
    district_name: str,
    sector_name: str,
    db: Session = Depends(get_db)
):
    """Get all TVET/TSS schools in a sector"""
    from urllib.parse import unquote
    from sqlalchemy import func
    province_name = unquote(province_name)
    district_name = unquote(district_name)
    sector_name = unquote(sector_name)
    # For now, return schools by district since we don't have sector field in School model
    schools = db.query(School).filter(
        func.lower(School.province) == province_name.lower(),
        func.lower(School.district) == district_name.lower()
    ).all()
    return [SchoolResponse.from_orm(school) for school in schools]

@router.get("/schools", response_model=List[SchoolResponse])
def get_all_schools(db: Session = Depends(get_db)):
    """Get all TVET/TSS schools"""
    schools = db.query(School).all()
    return [SchoolResponse.from_orm(school) for school in schools]

@router.get("/schools/{school_id}/trades")
def get_school_trades(school_id: int, db: Session = Depends(get_db)):
    """Get all trades offered by a specific school"""
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return {"school_id": school_id, "school_name": school.name, "trades": school.trades or []}

@router.get("/levels")
def get_tvet_levels():
    """Get all available TVET levels"""
    return {
        "levels": ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"]
    }
