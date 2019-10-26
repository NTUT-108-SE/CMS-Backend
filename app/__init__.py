from sanic import Sanic
from sanic_session import Session, InMemorySessionInterface
import logging

app = Sanic(__name__)
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)

logger = logging.getLogger(__name__)

# formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
# logging.basicConfig(level=logging.INFO, format=formatter)


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await session.open(request)


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    await session.save(request, response)