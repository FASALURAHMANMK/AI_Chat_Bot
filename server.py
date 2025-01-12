from os import getenv
from openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=getenv("OPENAI_API_KEY"))

@app.route('/generate_ideas', methods=['POST'])
def generate_ideas():
    try:
        user_query = request.json.get('query')
        
        # Unified prompt to generate and rank ideas
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate 3 unique and innovative results for: {user_query}. Rank them based on relevance, potential impact, and feasibility. Return them as a JSON list with each idea as an object containing 'idea' and 'score' fields. Score should be out of 10, like 9.5. Order by the rank and no need numbering."}
            ],
            temperature=1,
            max_tokens=2048
        )
        
        # Parse GPT response as JSON
        ranked_ideas = eval(response.choices[0].message.content.strip())
        
        if len(ranked_ideas) < 3:
            return jsonify({"error": "Insufficient ideas generated."}), 500

        return jsonify({"ideas": ranked_ideas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    try:
        selected_idea = request.json.get('selected_idea')

        if not selected_idea:
            return jsonify({"error": "No idea selected. Please provide an idea."}), 400

        # Generate a detailed plan for the selected idea
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Give a detailed plan for this idea in short: {selected_idea}"}
            ],
            temperature=1,
            max_tokens=2048
        )
        suggestion = response.choices[0].message.content.strip()

        return jsonify({"suggestion": suggestion}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/explain_ranking', methods=['POST'])
def explain_ranking():
    try:
        idea = request.json.get('idea')

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Explain the relevance, potential impact, and feasibility of this idea in short: {idea}"}
            ],
            temperature=1,
            max_tokens=2048
        )

        explanation = response.choices[0].message.content.strip()
        return jsonify({"explanation": explanation}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)