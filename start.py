import os

from tea_site import create_app
from tea_site.config import ProdConfig

app = create_app(ProdConfig)

if __name__ == "__main__":
    port = int(os.environ.get("PORT"))
    app.run(host="0.0.0.0", port=port, debug=False)

