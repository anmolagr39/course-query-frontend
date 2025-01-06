import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from hand import process_query
import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
async def handle_query():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
        
    try:
        results, matches, refined_response = await process_query(prompt)
        return jsonify({
            'results': results,
            'matches': matches,
            'refined_response': refined_response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#if __name__ == '__main__':
 #   port = int(os.environ.get('PORT', 5000))
   # app.run(host='0.0.0.0', port=port) 