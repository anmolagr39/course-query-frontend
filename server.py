from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from hand import process_query
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='build', static_url_path='/')
CORS(app)

# Store previous matches in server memory
previous_matches = None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    global previous_matches
    try:
        data = request.json
        user_prompt = data.get('prompt')
        
        if not user_prompt:
            logger.warning("No prompt provided in request")
            return jsonify({'error': 'No prompt provided'}), 400

        logger.info(f"Processing query: {user_prompt}")
        
        # Run the async process_query function with previous matches
        results, current_matches, refined_response = asyncio.run(process_query(user_prompt, previous_matches))
        
        # Update previous_matches if new matches are found
        if current_matches and "None" not in current_matches:
            previous_matches = current_matches
            logger.info(f"Updated previous matches: {previous_matches}")
        
        # Handle case where no results are found
        if not results:
            logger.info("No results found for query")
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
        
        logger.info(f"Sending response: {response}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        error_message = f"An error occurred: {str(e)}"
        return jsonify({
            'error': error_message,
            'response': 'Sorry, I encountered an error. Please try again.',
            'metadata': None,
            'refined_response': None
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 