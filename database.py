from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from setting import settings
from fastapi import HTTPException

engine = create_engine(settings.DB_URL)
Base = declarative_base()
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    finally:
        db.close()
