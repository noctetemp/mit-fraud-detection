# app.py - Elegant Fraud Detection System
import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import random
from datetime import datetime
import openai

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY', '')

# Store session data
sessions = {}

# Elegant Modern HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Federated Intelligence - MIT</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #1e293b;
            --gray: #64748b;
            --light: #f1f5f9;
            --white: #ffffff;
            --shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 25px 50px -12px rgb(0 0 0 / 0.25);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        /* Animated Background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(139, 92, 246, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(236, 72, 153, 0.2) 0%, transparent 50%);
            animation: backgroundShift 20s ease infinite;
            z-index: -1;
        }

        @keyframes backgroundShift {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(-20px, -20px) rotate(120deg); }
            66% { transform: translate(20px, -10px) rotate(240deg); }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }

        /* Header */
        .header {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
            animation: fadeInDown 0.8s ease;
        }

        .header h1 {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, #ffffff, #e0e7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .header .subtitle {
            font-size: 1.25rem;
            opacity: 0.95;
            font-weight: 300;
            letter-spacing: 0.5px;
        }

        .header .badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 0.5rem 1.5rem;
            border-radius: 2rem;
            margin-top: 1rem;
            font-size: 0.875rem;
            font-weight: 500;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        /* Main Grid */
        .main-grid {
            display: grid;
            grid-template-columns: 400px 1fr;
            gap: 2rem;
            animation: fadeInUp 0.8s ease;
        }

        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Glass Panel */
        .glass-panel {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
            border: 1px solid rgba(255, 255, 255, 0.5);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .glass-panel:hover {
            transform: translateY(-2px);
            box-shadow: 0 30px 60px -15px rgb(0 0 0 / 0.3);
        }

        .panel-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .panel-title::before {
            content: '';
            width: 4px;
            height: 24px;
            background: linear-gradient(to bottom, var(--primary), var(--secondary));
            border-radius: 2px;
        }

        /* Form Styles */
        .form-group {
            margin-bottom: 1.25rem;
        }

        .form-label {
            display: block;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--gray);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-input {
            width: 100%;
            padding: 0.875rem 1rem;
            border: 2px solid var(--light);
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            background: var(--white);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
            transform: translateY(-1px);
        }

        select.form-input {
            cursor: pointer;
        }

        /* Modern Button */
        .btn {
            position: relative;
            padding: 1rem 2rem;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s;
        }

        .btn:hover::before {
            transform: translateX(100%);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            width: 100%;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        }

        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .btn-small {
            padding: 0.625rem 1.25rem;
            font-size: 0.875rem;
            width: auto;
        }

        .btn-success {
            background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        }

        .btn-warning {
            background: linear-gradient(135deg, var(--warning) 0%, #d97706 100%);
        }

        .btn-danger {
            background: linear-gradient(135deg, var(--danger) 0%, #dc2626 100%);
        }

        /* Agent Cards */
        .agent-card {
            background: linear-gradient(145deg, #f8fafc, #ffffff);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 2px solid transparent;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .agent-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
            transition: left 0.6s ease;
        }

        .agent-card.active {
            border-color: var(--primary);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.15);
            transform: scale(1.02);
        }

        .agent-card.active::before {
            left: 100%;
        }

        .agent-card.completed {
            border-color: var(--success);
        }

        .agent-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .agent-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            transition: transform 0.3s ease;
        }

        .agent-card.active .agent-icon {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .agent-info {
            flex: 1;
        }

        .agent-name {
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--dark);
        }

        .agent-role {
            font-size: 0.875rem;
            color: var(--gray);
        }

        .agent-status {
            padding: 0.375rem 0.875rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .status-pending {
            background: var(--light);
            color: var(--gray);
        }

        .status-active {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }

        .status-completed {
            background: var(--success);
            color: white;
        }

        /* Agent Output */
        .agent-output {
            margin-top: 1rem;
            padding: 1.25rem;
            background: rgba(99, 102, 241, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(99, 102, 241, 0.1);
            display: none;
            animation: slideDown 0.4s ease;
        }

        .agent-output.show {
            display: block;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Chat Interface */
        .chat-interface {
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(241, 245, 249, 0.5);
            border-radius: 12px;
            display: none;
        }

        .chat-interface.show {
            display: block;
            animation: fadeIn 0.4s ease;
        }

        .chat-messages {
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 1rem;
            padding: 0.75rem;
            background: white;
            border-radius: 8px;
        }

        .chat-messages::-webkit-scrollbar {
            width: 6px;
        }

        .chat-messages::-webkit-scrollbar-track {
            background: var(--light);
            border-radius: 3px;
        }

        .chat-messages::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 3px;
        }

        .chat-message {
            margin-bottom: 0.75rem;
            padding: 0.75rem;
            border-radius: 8px;
            animation: messageSlide 0.3s ease;
        }

        @keyframes messageSlide {
            from {
                opacity: 0;
                transform: translateX(-10px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .message-agent {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border-left: 3px solid var(--primary);
        }

        .message-user {
            background: var(--light);
            text-align: right;
            border-right: 3px solid var(--secondary);
        }

        .chat-input-group {
            display: flex;
            gap: 0.75rem;
        }

        .chat-input {
            flex: 1;
            padding: 0.75rem;
            border: 2px solid var(--light);
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .chat-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        /* Alert Styles */
        .alert {
            padding: 1rem 1.25rem;
            border-radius: 12px;
            margin: 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            animation: alertSlide 0.4s ease;
        }

        @keyframes alertSlide {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .alert-danger {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
            border-left: 4px solid var(--danger);
            color: #991b1b;
        }

        .alert-warning {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(245, 158, 11, 0.05));
            border-left: 4px solid var(--warning);
            color: #92400e;
        }

        .alert-success {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
            border-left: 4px solid var(--success);
            color: #064e3b;
        }

        /* Metric Cards */
        .metric-card {
            background: white;
            padding: 1.25rem;
            border-radius: 12px;
            margin: 0.75rem 0;
            border-left: 4px solid;
            border-image: linear-gradient(to bottom, var(--primary), var(--secondary)) 1;
            transition: transform 0.3s ease;
        }

        .metric-card:hover {
            transform: translateX(4px);
        }

        .metric-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--gray);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Decision Buttons */
        .decision-container {
            margin-top: 1.5rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
            border-radius: 12px;
            display: none;
        }

        .decision-container.show {
            display: block;
            animation: fadeIn 0.4s ease;
        }

        .decision-buttons {
            display: flex;
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .decision-buttons .btn {
            flex: 1;
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
            margin-left: 0.5rem;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2.5rem;
            }
            
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .decision-buttons {
                flex-direction: column;
            }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: var(--light);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(to bottom, var(--primary), var(--secondary));
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(to bottom, var(--primary-dark), var(--secondary));
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Federated Intelligence</h1>
            <p class="subtitle">Next-Generation AI Fraud Detection System</p>
            <div class="badge">MIT Impact Project 5 • Group 4</div>
        </div>

        <div class="main-grid">
            <div class="glass-panel">
                <h2 class="panel-title">Transaction Analysis</h2>
                
                <div class="form-group">
                    <label class="form-label">Account Holder</label>
                    <input type="text" class="form-input" id="userName" value="Joe Smith" placeholder="Enter name">
                </div>

                <div class="form-group">
                    <label class="form-label">Transaction Amount</label>
                    <input type="number" class="form-input" id="transactionAmount" value="40" placeholder="USD">
                </div>

                <div class="form-group">
                    <label class="form-label">24h Transaction Count</label>
                    <input type="number" class="form-input" id="previousTransactions" value="3000000" placeholder="Count">
                </div>

                <div class="form-group">
                    <label class="form-label">Account Age</label>
                    <input type="number" class="form-input" id="accountAge" value="365" placeholder="Days">
                </div>

                <div class="form-group">
                    <label class="form-label">Location</label>
                    <input type="text" class="form-input" id="location" value="Singapore" placeholder="City">
                </div>

                <div class="form-group">
                    <label class="form-label">Device Type</label>
                    <select class="form-input" id="deviceType">
                        <option value="mobile">Mobile Device</option>
                        <option value="desktop">Desktop</option>
                        <option value="tablet">Tablet</option>
                        <option value="atm">ATM</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Time Period</label>
                    <select class="form-input" id="timeOfDay">
                        <option value="morning">Morning (6AM-12PM)</option>
                        <option value="afternoon">Afternoon (12PM-6PM)</option>
                        <option value="evening">Evening (6PM-12AM)</option>
                        <option value="night">Night (12AM-6AM)</option>
                    </select>
                </div>

                <button class="btn btn-primary" onclick="startAnalysis()" id="startBtn">
                    <span>Initialize Analysis</span>
                    <span class="loading" id="loadingSpinner" style="display: none;"></span>
                </button>
            </div>

            <div class="glass-panel">
                <h2 class="panel-title">Intelligent Agent Network</h2>
                
                <div class="agent-card" id="agent1">
                    <div class="agent-header">
                        <div class="agent-icon">🔍</div>
                        <div class="agent-info">
                            <div class="agent-name">Agent Hound</div>
                            <div class="agent-role">Federated ML Analysis</div>
                        </div>
                        <div class="agent-status status-pending" id="agent1-status">Pending</div>
                    </div>
                    <div class="agent-output" id="agent1-output"></div>
                    <div class="chat-interface" id="agent1-chat">
                        <div class="chat-messages" id="agent1-messages"></div>
                        <div class="chat-input-group">
                            <input type="text" class="chat-input" id="agent1-input" placeholder="Query the agent...">
                            <button class="btn btn-small btn-primary" onclick="sendMessage('agent1')">Send</button>
                            <button class="btn btn-small btn-warning" onclick="nextAgent('agent1')">Next →</button>
                        </div>
                    </div>
                </div>

                <div class="agent-card" id="agent2">
                    <div class="agent-header">
                        <div class="agent-icon">📊</div>
                        <div class="agent-info">
                            <div class="agent-name">Agent Fetch</div>
                            <div class="agent-role">Pattern Recognition</div>
                        </div>
                        <div class="agent-status status-pending" id="agent2-status">Pending</div>
                    </div>
                    <div class="agent-output" id="agent2-output"></div>
                    <div class="chat-interface" id="agent2-chat">
                        <div class="chat-messages" id="agent2-messages"></div>
                        <div class="chat-input-group">
                            <input type="text" class="chat-input" id="agent2-input" placeholder="Analyze patterns...">
                            <button class="btn btn-small btn-primary" onclick="sendMessage('agent2')">Send</button>
                            <button class="btn btn-small btn-warning" onclick="nextAgent('agent2')">Next →</button>
                        </div>
                    </div>
                </div>

                <div class="agent-card" id="agent3">
                    <div class="agent-header">
                        <div class="agent-icon">⚖️</div>
                        <div class="agent-info">
                            <div class="agent-name">Agent Judge</div>
                            <div class="agent-role">Risk Assessment</div>
                        </div>
                        <div class="agent-status status-pending" id="agent3-status">Pending</div>
                    </div>
                    <div class="agent-output" id="agent3-output"></div>
                    <div class="chat-interface" id="agent3-chat">
                        <div class="chat-messages" id="agent3-messages"></div>
                        <div class="chat-input-group">
                            <input type="text" class="chat-input" id="agent3-input" placeholder="Discuss verdict...">
                            <button class="btn btn-small btn-primary" onclick="sendMessage('agent3')">Send</button>
                        </div>
                    </div>
                </div>

                <div class="decision-container" id="finalDecision">
                    <h3 style="margin-bottom: 1rem; color: var(--dark);">Final Decision Required</h3>
                    <div class="decision-buttons">
                        <button class="btn btn-success" onclick="makeDecision('approve')">
                            ✅ Approve
                        </button>
                        <button class="btn btn-warning" onclick="makeDecision('review')">
                            🔍 Review
                        </button>
                        <button class="btn btn-danger" onclick="makeDecision('block')">
                            🚫 Block
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_URL = window.location.origin;
        let sessionId = 'session-' + Date.now();

        async function startAnalysis() {
            const btn = document.getElementById('startBtn');
            const spinner = document.getElementById('loadingSpinner');
            btn.disabled = true;
            spinner.style.display = 'inline-block';
            
            const transaction = {
                userName: document.getElementById('userName').value,
                transactionAmount: parseFloat(document.getElementById('transactionAmount').value),
                previousTransactions: parseInt(document.getElementById('previousTransactions').value),
                accountAge: parseInt(document.getElementById('accountAge').value),
                location: document.getElementById('location').value,
                deviceType: document.getElementById('deviceType').value,
                timeOfDay: document.getElementById('timeOfDay').value
            };

            // Reset UI
            document.querySelectorAll('.agent-card').forEach(card => {
                card.classList.remove('active', 'completed');
                card.querySelector('.agent-output').classList.remove('show');
                card.querySelector('.chat-interface').classList.remove('show');
                card.querySelector('.agent-status').className = 'agent-status status-pending';
                card.querySelector('.agent-status').textContent = 'Pending';
            });
            document.getElementById('finalDecision').classList.remove('show');

            // Start analysis
            setTimeout(async () => {
                spinner.style.display = 'none';
                await activateAgent('agent1', transaction);
            }, 500);
        }

        async function activateAgent(agentId, transaction = null) {
            const card = document.getElementById(agentId);
            const status = document.getElementById(agentId + '-status');
            
            card.classList.add('active');
            status.className = 'agent-status status-active';
            status.textContent = 'Processing';

            let endpoint = '';
            if (agentId === 'agent1') endpoint = '/api/analyze/hound';
            else if (agentId === 'agent2') endpoint = '/api/analyze/fetch';
            else if (agentId === 'agent3') endpoint = '/api/analyze/judge';

            try {
                const response = await fetch(API_URL + endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ sessionId, transaction })
                });

                const data = await response.json();
                
                setTimeout(() => {
                    displayAgentOutput(agentId, data);
                    status.className = 'agent-status status-completed';
                    status.textContent = 'Complete';
                    card.querySelector('.chat-interface').classList.add('show');
                    
                    if (agentId === 'agent3') {
                        document.getElementById('finalDecision').classList.add('show');
                    }
                }, 800);
            } catch (error) {
                console.error('Error:', error);
                status.textContent = 'Error';
            }
        }

        function displayAgentOutput(agentId, data) {
            const output = document.getElementById(agentId + '-output');
            let html = '';

            if (agentId === 'agent1') {
                const riskLevel = data.fraudScore > 70 ? 'danger' : data.fraudScore > 40 ? 'warning' : 'success';
                html = `
                    <div class="metric-card">
                        <div class="metric-label">Fraud Probability Score</div>
                        <div class="metric-value">${data.fraudScore}%</div>
                    </div>
                    <div class="alert alert-${riskLevel}">
                        <div>
                            <strong>Confidence Level:</strong> ${data.confidence}%<br>
                            <strong>Risk Factors Identified:</strong>
                            <ul style="margin: 0.5rem 0 0 1.5rem;">
                                ${data.factors.map(f => `<li>${f}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                `;
            } else if (agentId === 'agent2') {
                html = `
                    <div class="metric-card">
                        <div class="metric-label">Similar Patterns Found</div>
                        <div class="metric-value">${data.similarCount}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Historical Fraud Rate</div>
                        <div class="metric-value">${data.fraudRate}%</div>
                    </div>
                    ${data.anomalies && data.anomalies.length > 0 ? `
                        <div class="alert alert-danger">
                            <div>
                                <strong>⚠️ Critical Anomalies:</strong><br>
                                ${data.anomalies.map(a => `• ${a}`).join('<br>')}
                            </div>
                        </div>
                    ` : '<div class="alert alert-success">✓ Pattern within normal parameters</div>'}
                `;
            } else if (agentId === 'agent3') {
                const alertType = data.finalScore > 70 ? 'danger' : data.finalScore > 50 ? 'warning' : 'success';
                const icon = data.finalScore > 70 ? '🚨' : data.finalScore > 50 ? '⚠️' : '✅';
                html = `
                    <div class="alert alert-${alertType}">
                        <div>
                            <strong style="font-size: 1.25rem;">${icon} ${data.classification}</strong><br>
                            <div style="margin-top: 0.75rem;">
                                <strong>Risk Score:</strong> ${data.finalScore}%<br>
                                <strong>Action:</strong> ${data.recommendation}
                            </div>
                        </div>
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
            messagesDiv.innerHTML += `<div class="chat-message message-user"><strong>You:</strong> ${message}</div>`;
            input.value = '';

            try {
                const response = await fetch(API_URL + '/api/chat/' + agentId, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ sessionId, message })
                });

                const data = await response.json();
                messagesDiv.innerHTML += `<div class="chat-message message-agent"><strong>Agent:</strong> ${data.response}</div>`;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            } catch (error) {
                messagesDiv.innerHTML += `<div class="chat-message message-agent"><strong>Agent:</strong> Processing your query...</div>`;
            }
        }

        async function nextAgent(currentAgentId) {
            const card = document.getElementById(currentAgentId);
            card.classList.remove('active');
            card.classList.add('completed');
            
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

            const emoji = decision === 'approve' ? '✅' : decision === 'review' ? '🔍' : '🚫';
            const color = decision === 'approve' ? '#10b981' : decision === 'review' ? '#f59e0b' : '#ef4444';
            
            // Modern notification
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 2rem;
                right: 2rem;
                background: white;
                padding: 1.5rem 2rem;
                border-radius: 12px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                display: flex;
                align-items: center;
                gap: 1rem;
                z-index: 1000;
                animation: slideInRight 0.4s ease;
                border-left: 4px solid ${color};
            `;
            notification.innerHTML = `
                <span style="font-size: 2rem;">${emoji}</span>
                <div>
                    <strong style="font-size: 1.125rem;">Decision Recorded</strong><br>
                    <span style="color: #64748b;">Transaction ${decision}</span>
                </div>
            `;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.4s ease';
                setTimeout(() => notification.remove(), 400);
            }, 3000);
            
            document.getElementById('startBtn').disabled = false;
        }

        // Keyboard support
        document.querySelectorAll('.chat-input').forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const agentId = input.id.replace('-input', '');
                    sendMessage(agentId);
                }
            });
        });

        // Add slide animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
'''

# [Keep all the Python backend code exactly the same as before]
# ... rest of the Python code remains unchanged ...

# Synthetic database generation
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

# [All the analyze functions remain the same]
def analyze_hound(transaction):
    """Agent Hound - ML Fraud Scoring"""
    fraud_score = 30
    factors = []
    
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
    
    if transaction.get('timeOfDay') == 'night':
        fraud_score += 10
        factors.append('Unusual time (night)')
    
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
    similar = []
    for t in synthetic_db:
        score_similar = abs(t['fraudScore'] - fraud_score) < 20
        amount_similar = abs(t['transactionAmount'] - transaction['transactionAmount']) < transaction['transactionAmount'] * 0.5 if transaction['transactionAmount'] > 0 else False
        prev_trans_similar = abs(t['previousTransactions'] - transaction['previousTransactions']) < transaction['previousTransactions'] * 0.5 if transaction['previousTransactions'] > 0 else False
        
        if score_similar or (amount_similar and prev_trans_similar):
            similar.append(t)
    
    anomalies = []
    avg_amount = 0
    avg_prev = 0
    avg_age = 0
    
    if similar:
        avg_amount = sum(t['transactionAmount'] for t in similar) / len(similar)
        avg_prev = sum(t['previousTransactions'] for t in similar) / len(similar)
        avg_age = sum(t['accountAge'] for t in similar) / len(similar)
        
        if abs(transaction['transactionAmount'] - avg_amount) > avg_amount * 2:
            anomalies.append(f'Transaction Amount (${transaction["transactionAmount"]} vs cluster avg ${avg_amount:.2f})')
        
        if abs(transaction['previousTransactions'] - avg_prev) > avg_prev * 2:
            anomalies.append(f'Previous Transactions ({transaction["previousTransactions"]:,} vs cluster avg {avg_prev:.0f})')
        
        if abs(transaction['accountAge'] - avg_age) > avg_age * 2:
            anomalies.append(f'Account Age ({transaction["accountAge"]} days vs cluster avg {avg_age:.0f} days)')
        
        if transaction['transactionAmount'] < 100 and transaction['previousTransactions'] > 100000:
            pattern_found = any(
                t['transactionAmount'] < 100 and t['previousTransactions'] > 100000 
                for t in similar
            )
            if not pattern_found:
                anomalies.append('CRITICAL: No legitimate user shows this tiny amount + massive history pattern')
    
    fraud_count = sum(1 for t in similar if t['isFraud'])
    fraud_rate = (fraud_count / len(similar) * 100) if similar else 0
    
    return {
        'similarCount': len(similar),
        'fraudRate': round(fraud_rate),
        'anomalies': anomalies,
        'timestamp': datetime.now().isoformat()
    }

def analyze_judge(hound_data, fetch_data, transaction):
    """Agent Judge - Final Classification"""
    final_score = hound_data['fraudScore']
    
    if fetch_data['fraudRate'] > 60:
        final_score += 15
    elif fetch_data['fraudRate'] < 20:
        final_score -= 10
    
    final_score += len(fetch_data['anomalies']) * 10
    
    if transaction['transactionAmount'] < 100 and transaction['previousTransactions'] > 100000:
        final_score = max(final_score, 85)
    
    final_score = min(max(final_score, 0), 100)
    
    if final_score >= 70:
        classification = 'HIGH RISK - FRAUD DETECTED'
        recommendation = f'Block transaction immediately. ${transaction["transactionAmount"]} with {transaction["previousTransactions"]:,} previous transactions is extremely suspicious.'
    elif final_score >= 50:
        classification = 'SUSPICIOUS ACTIVITY'
        recommendation = 'Flag for manual review. Unusual pattern detected.'
    else:
        classification = 'LEGITIMATE TRANSACTION'
        recommendation = 'Approve transaction'
    
    return {
        'classification': classification,
        'finalScore': final_score,
        'recommendation': recommendation,
        'timestamp': datetime.now().isoformat()
    }

def get_llm_response(agent_name, message, context):
    """Get response from OpenAI with full context"""
    transaction = context.get('transaction', {})
    
    if not openai.api_key or openai.api_key == '':
        if 'amount' in message.lower():
            return f"The transaction amount is ${transaction.get('transactionAmount', 40)}. With {transaction.get('previousTransactions', 3000000):,} previous transactions in 24 hours, this is highly suspicious."
        
        if 'context' in message.lower() or 'information' in message.lower():
            return f"I'm analyzing a ${transaction.get('transactionAmount', 40)} transaction from {transaction.get('userName', 'the user')} with {transaction.get('previousTransactions', 3000000):,} previous transactions. The fraud score is {context.get('fraudScore', 75)}% with key risk factors identified."
        
        return f"This transaction shows highly unusual patterns. ${transaction.get('transactionAmount', 40)} with {transaction.get('previousTransactions', 3000000):,} previous transactions is a major red flag."
    
    try:
        system_prompts = {
            'agent1': "You are Agent Hound, a fraud detection ML specialist.",
            'agent2': "You are Agent Fetch, analyzing historical patterns.",
            'agent3': "You are Agent Judge, making final fraud decisions."
        }
        
        context_message = f"""
        Transaction: ${transaction.get('transactionAmount')} with {transaction.get('previousTransactions'):,} previous transactions
        Fraud Score: {context.get('fraudScore')}%
        User Question: {message}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompts.get(agent_name, "You are a fraud detection agent.")},
                {"role": "user", "content": context_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except:
        return f"The transaction is ${transaction.get('transactionAmount', 40)} with {transaction.get('previousTransactions', 3000000):,} previous transactions."

# [All Flask routes remain exactly the same]
@app.route('/')
def index():
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
    transaction = sessions[session_id].get('transaction')
    
    result = analyze_judge(hound_data, fetch_data, transaction)
    sessions[session_id]['judge'] = result
    
    return jsonify(result)

@app.route('/api/chat/<agent_name>', methods=['POST'])
def api_chat(agent_name):
    data = request.json
    session_id = data.get('sessionId')
    message = data.get('message')
    
    if session_id not in sessions:
        return jsonify({'error': 'No session found'}), 400
    
    session_data = sessions[session_id]
    
    context = {
        'transaction': session_data.get('transaction', {}),
        'fraudScore': session_data.get('hound', {}).get('fraudScore'),
        'confidence': session_data.get('hound', {}).get('confidence'),
        'factors': session_data.get('hound', {}).get('factors', []),
        'similarCount': session_data.get('fetch', {}).get('similarCount'),
        'fraudRate': session_data.get('fetch', {}).get('fraudRate'),
        'anomalies': session_data.get('fetch', {}).get('anomalies', []),
        'classification': session_data.get('judge', {}).get('classification'),
        'recommendation': session_data.get('judge', {}).get('recommendation')
    }
    
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