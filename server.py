from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from hand import process_query

app = Flask(__name__)
CORS(app, resources={r"/query": {"origins": "http://localhost:3000"}})

# Store previous matches in server memory
previous_matches = None

@app.route('/query', methods=['POST'])
def handle_query():
    global previous_matches
    data = request.json
    user_prompt = data.get('prompt')
    
    if not user_prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # Run the async process_query function with previous matches
        results, current_matches, refined_response = asyncio.run(process_query(user_prompt, previous_matches))
        
        # Update previous_matches if new matches are found
        if current_matches and "None" not in current_matches:
            previous_matches = current_matches
        
        # Handle case where no results are found
        if not results:
            return jsonify({
                'response': 'No results found',
                'metadata': None,
                'refined_response': None
            })
        
        # Format the response
        response = {
            'response': results[0]['metadata'] if results else 'No results found',
            'metadata': current_matches if current_matches else None,
            'refined_response': refined_response
        }
        
        return jsonify(response)
    except Exception as e:
        print(f"Error processing query: {str(e)}")  # Add logging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 