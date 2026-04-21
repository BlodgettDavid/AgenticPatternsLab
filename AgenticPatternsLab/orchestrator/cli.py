import sys
from AgenticPatternsLab.orchestrator.orchestrator_core.orchestrator import run_orchestrator


def print_usage():
    print(
        "Usage:\n"
        "  python -m orchestrator.cli run <pattern_name> "
        "[--framework <framework_name>] "
        "[--provider <provider_name>] "
        "[--prompt \"your question\"]\n"
    )


def main():
    # Must have at least: cli.py run <pattern>
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    # ------------------------------------------------------------------
    # Extract optional --prompt
    # ------------------------------------------------------------------
    user_prompt = None
    if "--prompt" in sys.argv:
        idx = sys.argv.index("--prompt")
        if idx + 1 < len(sys.argv):
            user_prompt = sys.argv[idx + 1]

    # ------------------------------------------------------------------
    # RUN COMMAND
    # ------------------------------------------------------------------
    if command == "run":
        if len(sys.argv) < 3:
            print("Error: Missing pattern name.\n")
            print_usage()
            return

        pattern_name = sys.argv[2]

        # Defaults
        framework = "pure_python"
        provider = None   # <-- allow orchestrator to choose default chain

        # Parse flags
        if "--framework" in sys.argv:
            idx = sys.argv.index("--framework")
            if idx + 1 < len(sys.argv):
                framework = sys.argv[idx + 1]

        if "--provider" in sys.argv:
            idx = sys.argv.index("--provider")
            if idx + 1 < len(sys.argv):
                provider = sys.argv[idx + 1]

        run_orchestrator(pattern_name, framework, provider, user_prompt)
        return

    # ------------------------------------------------------------------
    # UNKNOWN COMMAND
    # ------------------------------------------------------------------
    print(f"Unknown command: {command}\n")
    print_usage()


if __name__ == "__main__":
    main()