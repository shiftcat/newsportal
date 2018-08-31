
import os
from app.app_router import flask_app


flask_app.run(host="0.0.0.0", port=int(os.getenv('SERVER_PORT', 80)), debug=True)