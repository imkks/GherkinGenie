import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.utils import AgentLogger
from src.tools import save_feature_file

load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class BaseAgent:
    def __init__(self, name, icon, model_name="gemini-2.5-pro"):
        self.name = name
        self.icon = icon
        self.model = genai.GenerativeModel(model_name)
        self.logger = AgentLogger()

class VisionAgent(BaseAgent):
    """
    Multimodal agent that analyzes screenshots to identify UI elements.
    """
    def analyze(self, image_path):
        self.logger.log_phase(self.name, self.icon, "Scanning visual interface...")
        
        # Load image data
        try:
            # Note: In a real scenario, we use PIL or the file API. 
            # Here we assume the file exists and upload it.
            sample_file = genai.upload_file(path=image_path, display_name="UI Screenshot")
        except Exception as e:
            return f"Error loading image: {str(e)}"

        prompt = """
        Analyze this UI screenshot. 
        List every interactive element you see (Buttons, Input Fields, Links, Headers). 
        Format the output as a structured list suitable for a tester to read.
        Identify the likely context (e.g., Login Page, Dashboard, Checkout).
        """
        
        response = self.model.generate_content([sample_file, prompt])
        result = response.text
        self.logger.log_thought(result)
        return result

class ArchitectAgent(BaseAgent):
    """
    Reasoning agent that designs the test strategy based on UI elements.
    """
    def design_strategy(self, ui_elements):
        self.logger.log_phase(self.name, self.icon, "Designing Test Strategy...")
        
        prompt = f"""
        You are a Senior QA Architect. Based on the following UI elements, design a comprehensive test strategy.
        
        UI Context:
        {ui_elements}
        
        Your strategy must include:
        1. Happy Path Scenarios (Standard user flow).
        2. Edge Case Scenarios (Empty fields, invalid formats).
        3. Security Scenarios (SQL Injection, XSS attempts, Auth bypass).
        
        Write this in plain English, not Gherkin yet.
        """
        
        response = self.model.generate_content(prompt)
        result = response.text
        self.logger.log_thought(result)
        return result

class GherkinAgent(BaseAgent):
    """
    Syntax agent that converts English strategy into Gherkin (.feature).
    """
    def generate_code(self, strategy):
        self.logger.log_phase(self.name, self.icon, "Generating Gherkin Syntax...")
        
        prompt = f"""
        You are a Gherkin Syntax Expert. Convert the following test strategy into a valid Cucumber .feature file.
        
        Strategy:
        {strategy}
        
        Rules:
        - Use Feature, Scenario, Given, When, Then syntax strictly.
        - Add 'Scenario Outline' and 'Examples' where appropriate for data-driven tests.
        - Ensure indentation is correct.
        - Return ONLY the Gherkin code, no markdown backticks.
        """
        
        response = self.model.generate_content(prompt)
        result = response.text.replace("```gherkin", "").replace("```", "").strip()
        self.logger.log_thought(result)
        return result

class ReviewerAgent(BaseAgent):
    """
    Gatekeeper agent that reviews code and uses Tools to save it.
    """
    def __init__(self):
        # Initialize with tools capability
        super().__init__("Reviewer Agent", "🛡️")
        self.model = genai.GenerativeModel(
            "gemini-flash-lite-latest",
            tools=[save_feature_file]
        )

    def review_and_save(self, gherkin_code, filename="generated_test.feature"):
        self.logger.log_phase(self.name, self.icon, "Reviewing and Saving Artifact...")
        
        prompt = f"""
        Review the following Gherkin code for syntax errors or missing logic.
        
        Gherkin Code:
        {gherkin_code}
        
        If the code looks good, use the 'save_feature_file' tool to save it to disk with the filename '{filename}'.
        If there are critical errors, fix them first, then save.
        """
        
        # Enable automatic function calling
        chat = self.model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message(prompt)
        
        # We assume the tool was called if the model decided to.
        # We iterate to find tool calls for logging purposes (optional, as auto-calling handles execution)
        for part in response.candidates[0].content.parts:
            if part.function_call:
                self.logger.log_tool_usage(
                    part.function_call.name, 
                    part.function_call.args, 
                    "Tool executed via Automatic Function Calling"
                )
        
        result = response.text
        self.logger.log_thought(result)
        return result