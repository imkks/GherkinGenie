import os
import argparse
from src.agents import VisionAgent, ArchitectAgent, GherkinAgent, ReviewerAgent
from src.utils import AgentLogger
from colorama import Fore, Style

def main():
    # 0. Setup
    parser = argparse.ArgumentParser(description="GherkinGenie: UI to Test Automation")
    parser.add_argument("--image", type=str, required=True, help="Path to the UI screenshot")
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"{Fore.RED}Error: Image file '{args.image}' not found.")
        return

    logger = AgentLogger()
    print(f"{Style.BRIGHT}{Fore.GREEN}Starting GherkinGenie Pipeline...{Style.RESET_ALL}\n")

    # 1. Initialize Agents
    vision_agent = VisionAgent("Vision Agent", "👁️")
    architect_agent = ArchitectAgent("Architect Agent", "📐")
    gherkin_agent = GherkinAgent("Gherkin Agent", "🥒")
    reviewer_agent = ReviewerAgent()

    # ---------------------------------------------------------
    # STEP 1: Vision Agent (Image -> UI List)
    # ---------------------------------------------------------
    ui_elements = vision_agent.analyze(args.image)
    logger.log_handoff("Vision Agent", "Architect Agent", ui_elements[:50])

    # ---------------------------------------------------------
    # STEP 2: Architect Agent (UI List -> Test Strategy)
    # ---------------------------------------------------------
    strategy = architect_agent.design_strategy(ui_elements)
    logger.log_handoff("Architect Agent", "Gherkin Agent", strategy[:50])

    # ---------------------------------------------------------
    # STEP 3: Gherkin Agent (Test Strategy -> .feature file)
    # ---------------------------------------------------------
    gherkin_code = gherkin_agent.generate_code(strategy)
    logger.log_handoff("Gherkin Agent", "Reviewer Agent", gherkin_code[:50])

    # ---------------------------------------------------------
    # STEP 4: Reviewer Agent (Review -> Tool Use [Save])
    # ---------------------------------------------------------
    # We derive a filename from the image name
    base_name = os.path.splitext(os.path.basename(args.image))[0]
    output_filename = f"{base_name}_tests.feature"
    
    final_response = reviewer_agent.review_and_save(gherkin_code, output_filename)

    print(f"\n{Style.BRIGHT}{Fore.GREEN}✅ Pipeline Complete! Output generated in /output folder.")

if __name__ == "__main__":
    main()