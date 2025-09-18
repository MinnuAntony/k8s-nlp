from flask import Flask, request, jsonify
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph
import subprocess
import re
 
app = Flask(__name__)
 
# Initialize Ollama model (small one for limited memory)
llm = ChatOllama(model="phi3", base_url="http://localhost:11434")
 
# --- Helper: extract kubectl command from any AI text ---
def extract_kubectl_command(text):
    """
    Extract the first kubectl command from any text returned by AI.
    """
    # Match 'kubectl' followed by anything until newline or backtick
    match = re.search(r"(kubectl\s+[^\n`]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None
 
# --- Node: interpret natural language into kubectl command & execute ---
def interpret_query(state):
    prompt = f"""
You are a Kubernetes assistant. Translate natural language queries
into kubectl commands that list, describe, or fetch logs of resources.
 
Query: {state['query']}
"""
    try:
        response = llm.invoke(prompt)
        raw_text = response.content
 
        # Extract kubectl command
        command = extract_kubectl_command(raw_text)
        if not command:
            return {"error": "Could not find kubectl command in AI response"}
 
        # Prevent obviously dangerous commands
        forbidden = ["rm", "sudo", "&", ";", "|", ">", "<"]
        command_lower = command.lower()
        if any(f in command_lower for f in forbidden):
            return {"error": "Command not allowed"}
 
        # Execute safely
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
 
        return {"command": command, "result": output}
 
    except Exception as e:
        return {"error": str(e)}
 
# --- Setup LangGraph ---
graph = StateGraph(dict)
graph.add_node("interpret", interpret_query)
graph.set_entry_point("interpret")
app_graph = graph.compile()  # <- defines app_graph
 
# --- Flask route ---
@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    result = app_graph.invoke({"query": user_query})
    return jsonify(result)
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
