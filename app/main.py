"""An HTTP service for the Celtra DevOps homework.

Exposes one GET route, <accountId>/data, which returns the account ID from
the URL, the current UTC timestamp and a random string.
"""

import os
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)
app.json.sort_keys = False


@app.get("/<account_id>/data")
def get_account_data(account_id: str):
    """Return data for the given account.

    - accountId: echoed back from the URL path
    - timestamp: current time in UTC, in ISO 8601 format
    - data: a random UUID
    """
    now_utc = datetime.now(timezone.utc)
    
    return jsonify(
        {
            "accountId": account_id,
            "timestamp": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "data": str(uuid.uuid4()),
        }
    )


if __name__ == "__main__":
    # Local development only. In the container, gunicorn serves the app
    # (see Dockerfile). Heroku tells the app which port to use via $PORT.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
