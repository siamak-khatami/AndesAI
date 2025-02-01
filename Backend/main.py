from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routers.Users import UserEndpoints
# from Routers.LLMs import LLMEndpoints
# Initialing fast api object

app = FastAPI(docs_url="/docs")
origins = ["*"]
app.include_router(UserEndpoints.user_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# TODO: Report a buf here for each page of the front-end


# app.include_router(router, dependencies=[Depends(security)]) # For Graphql
@app.get('/')
async def root():
    return {'msg': 'Hello Service after changes, change!'}








initial_work = 10

def IF_THEN_ELSE(q,w,e):
    return 0
def work_flow (x, y):
    a = IF_THEN_ELSE(1,2,3)
    return a

work_flow(1, 2)


def Max(a, b):
    # 1
    if(a>b):
        return a
    else:
        if(b>a):
            return b
    # 2
    if(a>b):
        return a
    elif b>a:
        return b
    # 3
    if(a>b):
        return a
    else:
        return b










