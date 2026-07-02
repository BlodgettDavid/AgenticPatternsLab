@echo off
echo Creating AgenticPatternsLab directory structure...

REM === Patterns ===
mkdir patterns
mkdir patterns\react
mkdir patterns\react\pure_python
mkdir patterns\react\framework_a
mkdir patterns\react\framework_b

mkdir patterns\planner_executor
mkdir patterns\planner_executor\pure_python
mkdir patterns\planner_executor\framework_a
mkdir patterns\planner_executor\framework_b

mkdir patterns\multi_agent
mkdir patterns\multi_agent\pure_python
mkdir patterns\multi_agent\framework_a
mkdir patterns\multi_agent\framework_b

mkdir patterns\memory_agent
mkdir patterns\memory_agent\pure_python
mkdir patterns\memory_agent\framework_a
mkdir patterns\memory_agent\framework_b

REM === Orchestrator ===
mkdir orchestrator
type nul > orchestrator\cli.py
type nul > orchestrator\runner.py

REM === Utils ===
mkdir utils
type nul > utils\llm.py
type nul > utils\logging.py

REM === Tests ===
mkdir tests

REM === Root files ===
type nul > README.md
type nul > .gitignore
type nul > requirements.txt

echo Done!
