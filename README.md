# GherkinGenie: Robust UI-to-Test Automation  
### *Capstone Project — Software Engineering Productivity Track*

---

## 📖 Project Overview

**GherkinGenie** is an autonomous **Sequential Multi-Agent System** designed to accelerate the QA process by converting raw UI screenshots (e.g., login screens, dashboards) into high-quality, industry-standard **Gherkin feature files**.

Unlike simple OCR tools, GherkinGenie uses a **Chain-of-Thought Multi-Agent Architecture** where each agent performs a specialized reasoning step: Vision → Strategy → Syntax → Quality Review.

---

## 🏗️ Multi-Agent Architecture

The system uses **4 sequential agents**:

### 👁️ Vision Agent (Multimodal)
- Uses **Gemini 1.5 Flash Vision** for pixel-level semantic extraction  
- Identifies UI elements such as Inputs, Buttons, Labels, Headers

### 📐 Architect Agent (Reasoning)
- Interprets UI components  
- Generates a comprehensive **Test Strategy**, including:  
  - Happy paths  
  - Edge cases  
  - Security and validation checks

### 🥒 Gherkin Agent (Syntax)
- Converts the natural-language test strategy into fully compliant **Gherkin syntax**  
- Ensures `Given / When / Then` structure is preserved

### 🛡️ Reviewer Agent (Gatekeeper + Tools)
- Performs validation and final quality checks  
- Equipped with a **custom tool**: `save_feature_file`  
- Automatically writes the `.feature` file to disk using LLM function calling

---

## 🚀 Key Concepts Demonstrated

- **Sequential Multi-Agent Orchestration**  
  Output of one agent becomes context for the next.

- **LLM Function Calling + Custom Tools**  
  The reviewer agent invokes Python functions autonomously to save files.

- **Observability & Logging**  
  A custom `AgentLogger` visualizes agent-to-agent handoff and the reasoning chain.

---

## 🛠️ Installation & Usage

### 1. Clone the Repository
```bash
git clone <repo_url>
cd GherkinGenie
```

### 2. Install dependencies:
```
pip install -r requirements.txt
```

### 3. Set API Key:
Create a .env file:
```
GEMINI_API_KEY=your_key_here
```

### 4. Run the Pipeline:
Provide a path to a screenshot (e.g., login.png).
```
python main.py --image login.png
```

## 📝 Example Output

### Input: A screenshot of a standard Login Page.

### Generated Output (output/login_tests.feature):
```
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
```
## 📦 Folder Structure
```
GherkinGenie/
│  
├── src/
│   └── agents.py
│   └── tools.py
│   └──utils.py
├── output/
├── main.py
├── requirements.txt
├── README.md
└── .env
```
## 📄 License

MIT License
