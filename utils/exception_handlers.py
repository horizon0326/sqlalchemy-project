from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import InternalError, SQLAlchemyError
from utils.exception import http_exception_handler, integrity_error_handler, sqlachemy_error_handler, general_exception_handler

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(InternalError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlachemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)