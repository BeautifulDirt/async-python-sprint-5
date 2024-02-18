import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import base
from core.config import app_settings, logging


app = FastAPI(
    title=app_settings.project_name,
    description=app_settings.project_description,
    summary=app_settings.project_summary,
    version=app_settings.project_version,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)

app.include_router(base.router)


if __name__ == '__main__':
    logging.info(f'DOCS_URL: {app.docs_url}')
    uvicorn.run(app,
                host=app_settings.project_host,
                port=app_settings.project_port)
