import os

def save_feature_file(filename: str, content: str):
    """
    Saves the generated Gherkin feature content to a local file.
    
    Args:
        filename (str): The name of the file (e.g., 'login.feature').
        content (str): The full Gherkin syntax content.
        
    Returns:
        dict: A status object indicating success or failure.
    """
    output_dir = "output"
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "message": f"File successfully saved to {filepath}", "path": filepath}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Dictionary for tool binding (if needed for manual function calling maps)
tools_map = {
    "save_feature_file": save_feature_file
}