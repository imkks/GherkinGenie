GherkinGenie: Robust UI-to-Test Automation

Capstone Project: Software Engineering Productivity Track

📖 Project Overview

GherkinGenie is an autonomous Sequential Multi-Agent System designed to accelerate the QA process. It takes a raw screenshot of a web interface (e.g., a login screen, dashboard) and generates a high-quality, industry-standard Gherkin feature file.

The system moves beyond simple OCR by using a "Chain of Thought" architecture where different agents handle specific concerns: Vision, Strategy, Syntax, and Quality Assurance.

🏗️ Multi-Agent Architecture

This project utilizes 4 Sequential Agents:

👁️ Vision Agent (Multimodal): Uses Gemini 1.5 Flash Vision capabilities to extract semantic meaning from pixels (Inputs, Buttons, Headers).

📐 Architect Agent (Reasoning): Analyzes the extracted elements to formulate a robust Test Strategy (Happy Paths, Edge Cases, Security Checks).

🥒 Gherkin Agent (Syntax): Translates the natural language strategy into strict, syntactically correct Gherkin (Given/When/Then).

🛡️ Reviewer Agent (Gatekeeper & Tools): specific agent equipped with a Custom Tool. It reviews the code and autonomously saves the .feature file to the local disk.

🚀 Key Concepts Demonstrated

Sequential Multi-Agent System: A clear separation of concerns where the output of one agent becomes the context for the next.

Custom Tools: The Reviewer Agent is equipped with a specific python function save_feature_file that it invokes via the LLM's function calling capability.

Observability: A custom AgentLogger class traces the execution flow and visually renders the "hand-off" of data between agents in the terminal.

🛠️ Installation & Usage

Clone the repo

Install dependencies:

pip install -r requirements.txt


Set API Key:
Create a .env file:

GEMINI_API_KEY=your_key_here


Run the Pipeline:
Provide a path to a screenshot (e.g., login.png).

python main.py --image login.png


📝 Example Output

Input: A screenshot of a standard Login Page.

Generated Output (output/login_tests.feature):

Feature: User Authentication

  Background:
    Given the user is on the Login Page

  Scenario: Successful Login with Valid Credentials
    When the user enters "valid_user" into the Username field
    And the user enters "password123" into the Password field
    And clicks the "Sign In" button
    Then the user should be redirected to the Dashboard

  Scenario: SQL Injection Attempt
    When the user enters "' OR '1'='1" into the Username field
    And clicks the "Sign In" button
    Then the system should display a generic error message
    And access should be denied
