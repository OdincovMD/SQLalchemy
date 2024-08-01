from queries.orm import SyncOrm
from queries.core import SyncCore
import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

sys.path.insert(1, os.path.join(sys.path[0], '..'))
async def main():
    # SyncCore.create_tables()
    # SyncCore.insert_data()
    # SyncCore.select_workers()
    # SyncCore.update_worker()
    # SyncCore.insert_resumes()

    SyncOrm.create_tables()
    SyncOrm.insert_data()
    # SyncOrm.select_data()
    SyncOrm.update_worker()
    SyncOrm.insert_resumes()
    # SyncOrm.select_resumes_avg()
    # SyncOrm.select_data()
    # SyncOrm.join_cte_subquery_window_func()
    # SyncOrm.select_workers_with_joined_relationship()
    # SyncOrm.select_workers_with_condition_relationship()
    SyncOrm.select_workers_with_contains_eager_relationship()
    SyncOrm.convert_workers_to_dto()



def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )
        
    @app.get("/workers", tags=["Кандидат"])
    def get_workers():
        workers = SyncOrm.convert_workers_to_dto()
        return workers
    
    return app
    

app = create_fastapi_app()


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(
        app="src.main:app",
        reload=True,
    )
