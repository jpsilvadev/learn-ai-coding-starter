---
description: Start the SlopLang web playground on a given port (default 8080)
---

The port is `$ARGUMENTS`, or 8080 if empty.

Current listeners: !`lsof -nP -iTCP -sTCP:LISTEN`

1. Check the listeners above for the port.
2. If something is already listening on that port:
   - If it is a Sloperator server (a `python` process running `playground/server.py`), don't start another. Tell me it is already running at `http://localhost:<port>`.
   - Otherwise, report which process holds the port and stop without starting anything.
3. If the port is free, start the playground from the project root as a background process (it runs until stopped, so don't wait for it to exit):
   `uv run playground/server.py <port>`
4. Tell me the URL, `http://localhost:<port>`. If it fails to start, report the error.
