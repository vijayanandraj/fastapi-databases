from typing import List

import databases
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
import logging
import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')

logging.config.fileConfig(fname=log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

DATABASE_URL = "mysql://root:Vinisha329@localhost:3306/test"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.reflect(engine, only=['ait_info', 'scan_status'])

Base = automap_base(metadata=metadata)

Base.prepare()

AIT_Info, Scan_Status = Base.classes.ait_info, Base.classes.scan_status
logger.info(AIT_Info)
logger.info(Scan_Status)
session = Session(engine)

class ScanRequest(BaseModel):
    ait_ids: List[str]

class ScanResponse(BaseModel):
    scan_request_id: str
    scan_status: str
    message: str

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/ere-start-scan/", response_model=ScanResponse)

async def initiate_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    ait_ids = str(request.ait_ids)
    scan_response = ScanResponse(scan_request_id = str(uuid.uuid4()), scan_status = "In Progress", message = "ER Engine initiated for AITs ==> " + ait_ids)
    background_tasks.add_task(initiate_scan_func, request, scan_response)
    return scan_response


@app.get("/ere-scan-status/{scan_request_id}", response_model=ScanResponse)

async def get_scan_status(scan_request_id: str):
    logger.info(f"Get Scan Status for ==> {scan_request_id}")
    query = "SELECT * FROM scan_status where scan_request_id = :scan_request_id"
    values = {"scan_request_id" : scan_request_id}
    row = await database.fetch_one(query, values)
    logger.info(row._asdict())
    result_dict = row._asdict()
    scan_status = Scan_Status(id=result_dict['id'], scan_request_id = result_dict['scan_request_id'],
                              scan_status = result_dict['scan_status'], scan_step = result_dict['scan_step'],
                              is_completed = result_dict['is_completed'], is_error = result_dict['is_error'],
                              modified = result_dict['modified'])

    logger.info(scan_status.scan_request_id)

@app.post("ere-restart-scan", response_model=ScanResponse)
async def restart_scan(scan_request_id: str):
    pass


async def initiate_scan_func(request: ScanRequest, response: ScanResponse):
    logger.info("In Init Scan")
    ait_ids = request.ait_ids
    query = "INSERT INTO scan_status(scan_request_id, scan_status, scan_step) VALUES (:scan_request_id, :scan_status, :scan_step)"
    values = {"scan_request_id": response.scan_request_id, "scan_status" : response.scan_status, "scan_step" : "Start"}
    await database.execute(query=query, values=values)
    logger.info("Scan status inserted...")



async def create_scan_request():
    pass

