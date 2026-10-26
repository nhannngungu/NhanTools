def main() -> int:
    from apps.suite.window import SuiteWindow
    from shared_ui.application import run_application
    return run_application(SuiteWindow)


if __name__ == "__main__":
    raise SystemExit(main())
