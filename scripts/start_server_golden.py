"""Production entrypoint that installs the Golden Drive bridge before Uvicorn."""
from scripts.golden_runtime_bridge import install_golden_runtime_bridge
from scripts.start_server import main


if __name__ == "__main__":
    install_golden_runtime_bridge()
    main()
