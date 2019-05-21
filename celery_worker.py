import os
from tea_site import celery, create_app
from tea_site.config import ProdConfig

app = create_app(ProdConfig)
app.app_context().push()
