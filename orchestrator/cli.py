import sys
from dotenv import load_dotenv
from orchestrator.orchestrator_core.orchestrator import run_orchestrator
from utils.session_manager import SessionManager
from utils.session_models import SessionState

# Explicitly load the local .env file into the runtime environment
load_dotenv()


def print_usage():
    print(
        "Usage:\n"
        "  python -m orchestrator.cli run <pattern_name> "
        "[--framework <framework_name>] "
        "[--provider <provider_name>] "
        "[--prompt \"your question\"] "
        "[--session-id <session_id>] "
        "[--resume]\n"
    )

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    # Check for the resume flag
    resume = "--resume" in sys.argv

    # Extract optional --prompt
    user_prompt = None
    if "--prompt" in sys.argv:
        idx = sys.argv.index("--prompt")
        if idx + 1 < len(sys.argv):
            user_prompt = sys.argv[idx + 1]

    # Extract optional --session-id
    session_id = "default_session"
    if "--session-id" in sys.argv:
        idx = sys.argv.index("--session-id")
        if idx + 1 < len(sys.argv):
            session_id = sys.argv[idx + 1]

    # Initialize Session Manager & load/create session state
    session_manager = SessionManager()
    session = session_manager.load_session(session_id)
    if not session:
        session = SessionState(session_id=session_id)

    # RUN COMMAND
    if command == "run":
        if len(sys.argv) < 3:
            print("Error: Missing pattern name.\n")
            print_usage()
            return

        pattern_name = sys.argv[2]
        framework = "pure_python"
        provider = None

        if "--framework" in sys.argv:
            idx = sys.argv.index("--framework")
            if idx + 1 < len(sys.argv):
                framework = sys.argv[idx + 1]

        if "--provider" in sys.argv:
            idx = sys.argv.index("--provider")
            if idx + 1 < len(sys.argv):
                provider = sys.argv[idx + 1]

        # Execute the orchestrator, passing the active session down
        # (Ensure your run_orchestrator signature accepts a `session` argument)
        try:
            run_orchestrator(
                pattern_name=pattern_name,
                framework=framework,
                provider=provider,
                prompt=user_prompt,
                session=session,
                resume=resume
            )
        finally:
            # Always commit session state changes back to disk on exit
            session_manager.save_session(session)
            print(f"[Session Manager] Session '{session.session_id}' successfully persisted.")

        return

    print(f"Unknown command: {command}\n")
    print_usage()

if __name__ == "__main__":
    main()