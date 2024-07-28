from fastapi.testclient import TestClient

import pytest
from httpx import AsyncClient

import sys

sys.path.append("../application")
from main import app
import nest_asyncio
nest_asyncio.apply()
client = TestClient(app)