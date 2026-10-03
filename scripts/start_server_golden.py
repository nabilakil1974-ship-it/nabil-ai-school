"""Production entrypoint (unchanged name). The Golden bridge monkey-patch is retired;
Golden routes are registered normally in app/main.py."""
import scripts.start_server as _server

if __name__ == "__main__":
    _server.main()
