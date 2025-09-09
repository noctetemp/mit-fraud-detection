# app.py - Fraud Detection System Backend for Heroku
import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import random
from datetime import datetime
import openai

app = Flask(__name__)
CORS(app)

# Configure OpenAI (you can switch to any LLM)
openai.api_key = os.environ.get('OPENAI_API_KEY', '')

# Store session data (in production, use Redis or database)
sessions = {}

# HTML Template (embedded so you only need one file for frontend)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fraud Detection System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .main-content { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; }
        .panel { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .form-group { margin-bottom: 15px; }
        label { display: block; font-weight: 600; color: #333; margin-bottom: 5px; }
        input, select { width: 100%; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 30px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; width: 100%; margin-top: 10px; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .agent-card { background: #f8f9fa; border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #667eea; opacity: 0.5; transition: all 0.3s; }
        .agent-card.active { opacity: 1; background: linear-gradient(135deg, #f5f7ff 0%, #ffffff 100%); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .agent-header { display: flex; align-items: center; margin-bottom: 15px; }
        .agent-icon { width: 40px; height: 40px; background: #667eea; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; margin-right: 15px; }
        .agent-output { margin-top: 15px; padding: 15px; background: white; border-radius: 8px; display: none; }
        .agent-output.show { display: block; }
        .chat-interface { margin-top: 15px; padding: 15px; background: #f0f9ff; border-radius: 8px; display: none; }
        .chat-interface.show { display: block; }
        .chat-messages { max-height: 200px; overflow-y: auto; margin-bottom: 10px; padding: 10px; background: white; border-radius: 5px; }
        .chat-message { margin-bottom: 10px; padding: 8px; border-radius: 5px; }
        .message-agent { background: #e0e7ff; }
        .message-user { background: #f3f4f6; text-align: right; }
        .chat-input-group { display: flex; gap: 10px; }
        .chat-input { flex: 1; padding: 10px; border: 2px solid #e0e0e0; border-radius: 5px; }
        .btn-small { padding: 10px 20px; width: auto; margin: 0; }
        .loading { display: inline-block; width: 20px; height: 20px; border: 3px solid #f3f3f3; border-top: 3px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite; margin-left: 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .alert { padding: 15px; border-radius: 8px; margin: 15px 0; }
        .alert-danger { background: #fee2e2; border-left: 4px solid #ef4444; color: #991b1b; }
        .alert-warning { background: #fef3c7; border-left: 4px solid #f59e0b; color: #78350f; }
        .alert-success { background: #d1fae5; border-left: 4px solid #10b981; color: #065f46; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Federated Intelligence</h1>
            <p>AI-Powered Fraud Detection System</p>
        </div>

        <div class="main-content">
            <div class="panel">
                <h2>Transaction Input</h2>
                <div class="form-group">
                    <label>User Name</label>
                    <input type="text" id="userName" value="Joe Smith">
                </div>
                <div class="form-group">
                    <label>Transaction Amount ($)</label>
                    <input type="number" id="transactionAmount" value="40">
                </div>
                <div class="form-group">
                    <label>Previous Transactions (24h)</label>
                    <input type="number" id="previousTransactions" value="3000000">
                </div>
                <div class="form-group">
                    <label>Account Age (days)</label>
                    <input type="number" id="accountAge" value="365">
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" id="location" value="Singapore">
                </div>
                <button class="btn" onclick="startAnalysis()" id="startBtn">
                    🚀 Start Fraud Detection
                </button>
            </div>

            <div class="panel">
                <h2>Agent Analysis</h2>
                
                <div class="agent-card" id="agent1">
                    <div class="agent-header">
                        <div class="agent-icon">🔍</div>
                        <div>
                            <strong>Agent Hound</strong><br>
                            <small>ML Fraud Scoring</small>
                        </div>
                    </div>
                    <div class="agent-output" id="agent1-output"></div>
                    <div class="chat-interface" id="agent1-chat">
                        <div class="chat-messages" id="agent1-messages"></div>
                        <div class="chat-input-group">
                            <input type="text" class="chat-input" id="agent1-input" placeholder="Ask about the analysis...">
                            <button class="btn btn-small" onclick="sendMessage('agent1')">Send</button>
                            <button class="btn btn-small" onclick="nextAgent('agent1')">Next →</button>
                        </div>
                    </div>
                </div>

                <div class="agent-card" id="agent2">
                    <div class="agent-header">
                        <div class="agent-icon">📊</div>
                        <div>
                            <strong>Agent Fetch</strong><br>
                            <small>Pattern Analysis</small>
                        </div>
                    </div>
                    <div class="agent-output" id="agent2-output"></div>
                    <div class="chat-interface" id="agent2-chat">
                        <div class="chat-messages" id="agent2-messages"></div>
                        <div class="chat-input-group">
                            <input type="text" class="chat-input" id="agent2-input" placeholder="Discuss patterns...">
                            <button class="btn btn-small" onclick="sendMessage('agent2')">Send</button>
                            <button class="btn btn-small" onclick="nextAgent('agent2')">Next →</button>
                        </div>
                    </div>
                </div>

                <div class="agent-card" id="agent3">
                    <div class="agent-header">
                        <div class="agent-icon">⚖️</div>
                        <div>
                            <strong>Agent Judge</strong><br>
                            <small>Final Decision</small>
                        </div>
                    </div>
                    <div class="agent-output" id="agent3-output"></div>
                    <div class="chat-interface" id="agent3-chat">
                        <div class="chat-messages" id="agent3-messages"></div>
                        <div class="chat-input-group">
                            <input type="text" class="chat-input" id="agent3-input" placeholder="Discuss verdict...">
                            <button class="btn btn-small" onclick="sendMessage('agent3')">Send</button>
                        </div>
                    </div>
                </div>

                <div id="finalDecision" style="display:none; margin-top: 20px;">
                    <button class="btn" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="makeDecision('approve')">✅ Approve</button>
                    <button class="btn" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); margin-top: 5px;" onclick="makeDecision('review')">🔍 Manual Review</button>
                    <button class="btn" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); margin-top: 5px;" onclick="makeDecision('block')">🚫 Block</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_URL = window.location.origin;
        let sessionId = 'session-' + Date.now();
        let currentAgent = null;

        async function startAnalysis() {
            document.getElementById('startBtn').disabled = true;
            
            const transaction = {
                userName: document.getElementById('userName').value,
                transactionAmount: parseFloat(document.getElementById('transactionAmount').value),
                previousTransactions: parseInt(document.getElementById('previousTransactions').value),
                accountAge: parseInt(document.getElementById('accountAge').value),
                location: document.getElementById('location').value
            };

            // Reset UI
            document.querySelectorAll('.agent-card').forEach(card => {
                card.classList.remove('active');
                card.querySelector('.agent-output').classList.remove('show');
                card.querySelector('.chat-interface').classList.remove('show');
            });

            // Start with Agent 1
            await activateAgent('agent1', transaction);
        }

        async function activateAgent(agentId, transaction = null) {
            currentAgent = agentId;
            const card = document.getElementById(agentId);
            card.classList.add('active');

            let endpoint = '';
            if (agentId === 'agent1') {
                endpoint = '/api/analyze/hound';
            } else if (agentId === 'agent2') {
                endpoint = '/api/analyze/fetch';
            } else if (agentId === 'agent3') {
                endpoint = '/api/analyze/judge';
            }

            try {
                const response = await fetch(API_URL + endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ sessionId, transaction })
                });

                const data = await response.json();
                displayAgentOutput(agentId, data);
                
                card.querySelector('.chat-interface').classList.add('show');
                
                if (agentId === 'agent3') {
                    document.getElementById('finalDecision').style.display = 'block';
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error connecting to server. Please try again.');
            }
        }

        function displayAgentOutput(agentId, data) {
            const output = document.getElementById(agentId + '-output');
            let html = '';

            if (agentId === 'agent1') {
                html = `
                    <div class="alert ${data.fraudScore > 70 ? 'alert-danger' : data.fraudScore > 40 ? 'alert-warning' : 'alert-success'}">
                        <strong>Fraud Score: ${data.fraudScore}%</strong><br>
                        Confidence: ${data.confidence}%
                    </div>
                    <strong>Risk Factors:</strong>
                    <ul>${data.factors.map(f => `<li>${f}</li>`).join('')}</ul>
                `;
            } else if (agentId === 'agent2') {
                html = `
                    <strong>Similar Transactions: ${data.similarCount}</strong><br>
                    <strong>Historical Fraud Rate: ${data.fraudRate}%</strong><br>
                    ${data.anomalies.length > 0 ? `
                        <div class="alert alert-danger">
                            Anomalies Detected: ${data.anomalies.join(', ')}
                        </div>
                    ` : '<div class="alert alert-success">No anomalies detected</div>'}
                `;
            } else if (agentId === 'agent3') {
                html = `
                    <div class="alert ${data.finalScore > 70 ? 'alert-danger' : data.finalScore > 50 ? 'alert-warning' : 'alert-success'}">
                        <strong>${data.classification}</strong><br>
                        Final Score: ${data.finalScore}%<br>
                        ${data.recommendation}
                    </div>
                `;
            }

            output.innerHTML = html;
            output.classList.add('show');
        }

        async function sendMessage(agentId) {
            const input = document.getElementById(agentId + '-input');
            const message = input.value.trim();
            if (!message) return;

            const messagesDiv = document.getElementById(agentId + '-messages');
            messagesDiv.innerHTML += `<div class="chat-message message-user">You: ${message}</div>`;
            input.value = '';

            try {
                const response = await fetch(API_URL + '/api/chat/' + agentId, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ sessionId, message })
                });

                const data = await response.json();
                messagesDiv.innerHTML += `<div class="chat-message message-agent">Agent: ${data.response}</div>`;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            } catch (error) {
                messagesDiv.innerHTML += `<div class="chat-message message-agent">Agent: I'm processing your request...</div>`;
            }
        }

        async function nextAgent(currentAgentId) {
            if (currentAgentId === 'agent1') {
                await activateAgent('agent2');
            } else if (currentAgentId === 'agent2') {
                await activateAgent('agent3');
            }
        }

        async function makeDecision(decision) {
            await fetch(API_URL + '/api/decision', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sessionId, decision })
            });

            alert(`Decision recorded: ${decision.toUpperCase()}`);
            document.getElementById('startBtn').disabled = false;
        }

        // Enter key support
        document.querySelectorAll('.chat-input').forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const agentId = input.id.replace('-input', '');
                    sendMessage(agentId);
                }
            });
        });
    </script>
</body>
</html>
'''

# Synthetic database for testing
def generate_synthetic_data():
    data = []
    for i in range(200):
        is_fraud = random.random() > 0.8
        data.append({
            'transactionAmount': random.randint(10, 50000) if is_fraud else random.randint(10, 5000),
            'previousTransactions': random.randint(1, 50) if is_fraud else random.randint(1, 500),
            'accountAge': random.randint(1, 30) if is_fraud else random.randint(30, 1000),
            'fraudScore': random.randint(0, 100),
            'isFraud': is_fraud
        })
    return data

synthetic_db = generate_synthetic_data()

# Agent Analysis Functions
def analyze_hound(transaction):
    """Agent Hound - ML Fraud Scoring"""
    fraud_score = 30  # Base score
    factors = []
    
    # Analyze transaction patterns
    if transaction['transactionAmount'] > 10000:
        fraud_score += 20
        factors.append('High transaction amount')
    
    if transaction['transactionAmount'] < 100 and transaction['previousTransactions'] > 100000:
        fraud_score += 45
        factors.append('ANOMALY: Tiny amount with massive transaction history')
    elif transaction['previousTransactions'] > 10000:
        fraud_score += 25
        factors.append('Very high transaction frequency')
    elif transaction['previousTransactions'] > 1000:
        fraud_score += 15
        factors.append('High transaction frequency')
    
    if transaction['accountAge'] < 30:
        fraud_score += 15
        factors.append('New account (<30 days)')
    
    fraud_score = min(max(fraud_score, 0), 100)
    confidence = min(90, 50 + len(factors) * 5)
    
    return {
        'fraudScore': fraud_score,
        'confidence': confidence,
        'factors': factors,
        'timestamp': datetime.now().isoformat()
    }

def analyze_fetch(fraud_score, transaction):
    """Agent Fetch - Historical Pattern Analysis"""
    # Find similar transactions
    similar = [t for t in synthetic_db if abs(t['fraudScore'] - fraud_score) < 20]
    
    # Check for anomalies
    anomalies = []
    if similar:
        avg_amount = sum(t['transactionAmount'] for t in similar) / len(similar)
        avg_prev = sum(t['previousTransactions'] for t in similar) / len(similar)
        
        if abs(transaction['transactionAmount'] - avg_amount) > avg_amount * 2:
            anomalies.append('Transaction Amount')
        
        if abs(transaction['previousTransactions'] - avg_prev) > avg_prev * 2:
            anomalies.append('Previous Transactions')
    
    fraud_count = sum(1 for t in similar if t['isFraud'])
    fraud_rate = (fraud_count / len(similar) * 100) if similar else 0
    
    return {
        'similarCount': len(similar),
        'fraudRate': round(fraud_rate),
        'anomalies': anomalies,
        'timestamp': datetime.now().isoformat()
    }

def analyze_judge(hound_data, fetch_data):
    """Agent Judge - Final Classification"""
    final_score = hound_data['fraudScore']
    
    # Adjust based on patterns
    if fetch_data['fraudRate'] > 60:
        final_score += 15
    elif fetch_data['fraudRate'] < 20:
        final_score -= 10
    
    # Penalty for anomalies
    final_score += len(fetch_data['anomalies']) * 10
    
    final_score = min(max(final_score, 0), 100)
    
    if final_score >= 70:
        classification = 'HIGH RISK - FRAUD'
        recommendation = 'Block transaction immediately'
    elif final_score >= 50:
        classification = 'SUSPICIOUS'
        recommendation = 'Flag for manual review'
    else:
        classification = 'LEGITIMATE'
        recommendation = 'Approve transaction'
    
    return {
        'classification': classification,
        'finalScore': final_score,
        'recommendation': recommendation,
        'timestamp': datetime.now().isoformat()
    }

def get_llm_response(agent_name, message, context):
    """Get response from OpenAI (or fallback to simple responses)"""
    if not openai.api_key or openai.api_key == 'your-api-key-here':
        # Fallback responses when no API key
        responses = {
            'agent1': f"The fraud score is based on the risk factors identified. {context.get('factors', [])}",
            'agent2': f"I found {context.get('similarCount', 0)} similar transactions with a {context.get('fraudRate', 0)}% fraud rate.",
            'agent3': f"Based on all factors, my recommendation is: {context.get('recommendation', 'Review needed')}"
        }
        return responses.get(agent_name, "I'm analyzing the data based on the patterns detected.")
    
    try:
        # Use OpenAI when API key is available
        system_prompts = {
            'agent1': "You are Agent Hound, a fraud detection ML specialist. Be concise and technical.",
            'agent2': "You are Agent Fetch, analyzing historical patterns. Focus on statistical insights.",
            'agent3': "You are Agent Judge, making final fraud decisions. Be decisive and clear."
        }
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompts.get(agent_name, "You are a fraud detection agent.")},
                {"role": "user", "content": f"Context: {json.dumps(context)}\n\nUser question: {message}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except:
        return "I'm analyzing the patterns in your transaction. The data shows interesting indicators."

# Flask Routes
@app.route('/')
def index():
    """Serve the HTML page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze/hound', methods=['POST'])
def api_hound():
    data = request.json
    session_id = data.get('sessionId')
    transaction = data.get('transaction')
    
    result = analyze_hound(transaction)
    
    if session_id not in sessions:
        sessions[session_id] = {}
    sessions[session_id]['hound'] = result
    sessions[session_id]['transaction'] = transaction
    
    return jsonify(result)

@app.route('/api/analyze/fetch', methods=['POST'])
def api_fetch():
    data = request.json
    session_id = data.get('sessionId')
    
    if session_id not in sessions:
        return jsonify({'error': 'No session found'}), 400
    
    hound_data = sessions[session_id].get('hound')
    transaction = sessions[session_id].get('transaction')
    
    result = analyze_fetch(hound_data['fraudScore'], transaction)
    sessions[session_id]['fetch'] = result
    
    return jsonify(result)

@app.route('/api/analyze/judge', methods=['POST'])
def api_judge():
    data = request.json
    session_id = data.get('sessionId')
    
    if session_id not in sessions:
        return jsonify({'error': 'No session found'}), 400
    
    hound_data = sessions[session_id].get('hound')
    fetch_data = sessions[session_id].get('fetch')
    
    result = analyze_judge(hound_data, fetch_data)
    sessions[session_id]['judge'] = result
    
    return jsonify(result)

@app.route('/api/chat/<agent_name>', methods=['POST'])
def api_chat(agent_name):
    data = request.json
    session_id = data.get('sessionId')
    message = data.get('message')
    
    if session_id not in sessions:
        return jsonify({'error': 'No session found'}), 400
    
    # Get context for the agent
    context = sessions[session_id].get(agent_name.replace('agent', '').replace('1', 'hound').replace('2', 'fetch').replace('3', 'judge'), {})
    
    response = get_llm_response(agent_name, message, context)
    
    return jsonify({'response': response})

@app.route('/api/decision', methods=['POST'])
def api_decision():
    data = request.json
    session_id = data.get('sessionId')
    decision = data.get('decision')
    
    if session_id in sessions:
        sessions[session_id]['decision'] = decision
    
    return jsonify({'status': 'success', 'decision': decision})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)