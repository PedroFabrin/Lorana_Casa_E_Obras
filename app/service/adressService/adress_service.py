from datetime import datetime
from sqlalchemy.orm import Session
from app.model.addressModel.adress_model import AdressModel
from app.schema.adressSchema.adress_schema import AdressCreate, AdressUpdate, AdressFilter, AdressResponse, AdressListResponse


def _sanitize_cep(cep: str) -> str:
    return cep.replace("-", "").replace(".", "").strip()


def create_adress(db: Session, data: AdressCreate, user_id: int):
    try:
        adress = AdressModel(
            user_id=user_id,
            rua=data.rua,
            numero=data.numero,
            cep=_sanitize_cep(data.cep),
            cidade=data.cidade,
            uf=data.uf.upper(),
        )
        db.add(adress)
        db.commit()
        db.refresh(adress)

        result = AdressResponse.model_validate(adress)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def get_adress(db: Session, adress_id: int):
    try:
        adress = db.query(AdressModel).filter(AdressModel.id == adress_id, AdressModel.deleted_at == None).first()
        if not adress:
            return None, "Endereço não encontrado"

        result = AdressResponse.model_validate(adress)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def get_adresses(db: Session, filters: AdressFilter):
    try:
        query = db.query(AdressModel).filter(AdressModel.deleted_at == None)

        if filters.user_id:
            query = query.filter(AdressModel.user_id == filters.user_id)
        if filters.cidade:
            query = query.filter(AdressModel.cidade.ilike(f"%{filters.cidade}%"))
        if filters.uf:
            query = query.filter(AdressModel.uf == filters.uf)
        if filters.cep:
            query = query.filter(AdressModel.cep == filters.cep)

        total = query.count()
        offset = (filters.page - 1) * filters.page_size
        adresses = query.offset(offset).limit(filters.page_size).all()

        result = AdressListResponse(
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            data=[AdressResponse.model_validate(a) for a in adresses],
        )
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def update_adress(db: Session, data: AdressUpdate):
    try:
        adress = db.query(AdressModel).filter(AdressModel.id == data.adress_id, AdressModel.deleted_at == None).first()
        if not adress:
            return None, "Endereço não encontrado"

        fields = data.model_dump(exclude_none=True, exclude={"adress_id"})
        if "cep" in fields:
            fields["cep"] = _sanitize_cep(fields["cep"])
        if "uf" in fields:
            fields["uf"] = fields["uf"].upper()

        for field, value in fields.items():
            setattr(adress, field, value)

        db.commit()
        db.refresh(adress)

        result = AdressResponse.model_validate(adress)
        return {"status": "success", "data": result.model_dump()}, None
    except Exception as e:
        return None, str(e)


def delete_adress(db: Session, adress_id: int):
    try:
        adress = db.query(AdressModel).filter(AdressModel.id == adress_id, AdressModel.deleted_at == None).first()
        if not adress:
            return None, "Endereço não encontrado"

        adress.deleted_at = datetime.now()
        db.commit()
        return {"status": "success", "message": "Endereço deletado com sucesso"}, None
    except Exception as e:
        return None, str(e)
