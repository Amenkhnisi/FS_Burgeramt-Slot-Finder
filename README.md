<!DOCTYPE html>
<html lang="en">

<body>

  <h1>🏛️ Burgeramt Slot Finder</h1>


  <div class="badges">
    <img src="https://img.shields.io/badge/Frontend-Vercel-blue?logo=vercel" alt="Frontend Vercel Badge" />
    <img src="https://img.shields.io/badge/Backend-Render-green?logo=render" alt="Backend Render Badge" />
    <img src="https://img.shields.io/badge/Bot-AWS_ECS-orange?logo=amazon-aws" alt="Bot AWS ECS Badge" />
    <img src="https://img.shields.io/badge/CI/CD-GitHub_Actions-black?logo=github-actions" alt="GitHub Actions Badge" />
    <img src="https://img.shields.io/badge/Stack-FastAPI_+_React_+_Vite-purple?logo=fastapi" alt="Stack Badge" />
        <img src="https://img.shields.io/badge/Text_Simplifier-OpenAI-8A2BE2?logo=openai" alt="OpenAI Badge" />
  </div>
  <br/>
  <p>A full-stack web application designed to simplify the process of finding appointment slots at German Burgerämter (citizen offices). It integrates real-time slot monitoring, Telegram bot alerts, and a text simplification API to decode bureaucratic language — making German administration more accessible.</p>

  <h2>🚀 Tech Stack</h2>
  <ul>
    <li><strong>Frontend:</strong> React + Vite</li>
    <li><strong>Backend:</strong> FastAPI</li>
    <li><strong>Database:</strong> PostgreSQL or SQLite</li>
    <li><strong>Integrations:</strong> Telegram Bot, OpenAPI (Text Simplifier)</li>
  </ul>

  <h2>📦 Features</h2>
  <ul>
    <li>🔍 <strong>Slot Finder:</strong> Monitors Burgeramt appointment availability in real-time.</li>
    <li>📲 <strong>Telegram Alerts:</strong> Sends instant notifications when new slots are found.</li>
    <li>🧠 <strong>Text Simplifier:</strong> Uses OpenAPI to translate complex bureaucratic German into plain language.</li>
    <li>🌐 <strong>RESTful API:</strong> Clean and documented endpoints for frontend/backend communication.</li>
    <li>🛡️ <strong>Secure & Performant:</strong> Built with modern frameworks and best practices.</li>
  </ul>

  <h2>🧠 Text Simplifier (OpenAI)</h2>
  <p>German bureaucracy often uses long, complex language that can be hard to understand. This app integrates an OpenAI-powered text simplifier that:</p>
  <ul>
    <li>Analyzes official Burgeramt descriptions and instructions</li>
    <li>Returns simplified, plain-language versions for easier comprehension</li>
    <li>Accessible via both frontend UI and backend API</li>
    <li>Powered by OpenAI's language model via secure API calls</li>
  </ul>

  <h2>🛠️ Installation</h2>
  <h3>1. Clone the repository</h3>
  <pre><code>git clone https://github.com/Amenkhnisi/FS_Burgeramt-Slot-Finder.git
cd FS_Burgeramt-Slot-Finder</code></pre>

  <h3>2. Backend Setup (FastAPI)</h3>
  <pre><code>cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload</code></pre>

  <h3>3. Frontend Setup (React + Vite)</h3>
  <pre><code>cd frontend
npm install
npm run dev</code></pre>

  <h3>4. Telegram Bot Setup</h3>
  <ul>
    <li>Create a bot via <a href="https://t.me/BotFather" target="_blank">BotFather</a></li>
    <li>Add your bot token to the <code>.env</code> file</li>
    <li>Run the bot service:</li>
  </ul>
  <pre><code>python telegram_bot.py</code></pre>

  <h2>📚 API Documentation</h2>
  <ul>
    <li>Swagger UI: <code>http://localhost:8000/docs</code></li>
    <li>Redoc: <code>http://localhost:8000/redoc</code></li>
  </ul>

  <h2>🧪 Testing</h2>
  <pre><code>pytest</code></pre>

  <h2>🌍 Deployment Overview</h2>
  <table>
    <thead>
      <tr>
        <th>Component</th>
        <th>Platform</th>
        <th>Deployment Method</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Frontend</strong></td>
        <td><a href="https://fs-burgeramt-slot-finder.vercel.app" target="_blank">Vercel</a></td>
        <td>GitHub CI/CD → Vercel</td>
      </tr>
      <tr>
        <td><strong>Backend API</strong></td>
        <td><a href="https://fs-burgeramt-slot-finder.onrender.com" target="_blank">Render</a></td>
        <td>GitHub CI/CD → Render</td>
      </tr>
      <tr>
        <td><strong>Telegram Bot</strong></td>
        <td>AWS ECS</td>
        <td>Containerized via GitHub CI/CD</td>
      </tr>
    </tbody>
  </table>

  <h2>🔄 CI/CD Pipeline</h2>
  <ul>
    <li>Automated builds and deployments using <strong>GitHub Actions</strong></li>
    <li>Environment variables managed securely via Vercel, Render, and AWS dashboards</li>
    <li>Telegram bot containerized and deployed via ECS task definitions</li>
    <li>Frontend and backend auto-deploy on push to <code>main</code> branch</li>
  </ul>

  <h2>🌐 Live URLs</h2>
  <ul>
    <li><strong>Frontend App:</strong> <a href="https://fs-burgeramt-slot-finder.vercel.app" target="_blank">Frontend URl</a></li>
    <li><strong>Backend API:</strong> <a href="https://fs-burgeramt-slot-finder.onrender.com/docs" target="_blank">Backend API URL</a></li>
    <li><strong>Telegram Bot:</strong> Accessible via <code>@BerlinAppointmentapiBot</code> on Telegram</li>
  </ul>
  <h2> Screenshots </h2>
<img width="500" height="600" alt="Screenshot 2026-01-07 151012" src="https://github.com/user-attachments/assets/1f86a214-0fec-4f9f-a542-936e31638288" />
<img width="500" height="600" alt="Screenshot 2026-01-07 151105" src="https://github.com/user-attachments/assets/b81a5ca3-8791-4d1e-b27e-7938b5d415ad" />
<img width="500" height="600" alt="Screenshot 2026-01-07 151258" src="https://github.com/user-attachments/assets/89b90e10-b598-4561-8617-7750e543c516" />
<img width="500" height="600" alt="Screenshot 2026-01-07 151415" src="https://github.com/user-attachments/assets/29400466-285a-4106-bc09-b8475192b898" />
<img width="500" height="600" alt="Screenshot 2026-01-07 151527" src="https://github.com/user-attachments/assets/fed1758f-2e44-44d0-9cbe-bd32dc9a3ce8" />
<img width="500" height="600" alt="Screenshot 2026-01-07 154145" src="https://github.com/user-attachments/assets/460af52f-e6e7-49b1-a1fb-4dfb3d9a01b9" />
<img width="500" height="600" alt="Screenshot 2026-01-07 152541" src="https://github.com/user-attachments/assets/a1d222e0-4871-457f-9915-644e32ecf0b5" />
<img width="500" height="750" alt="Screenshot 2026-01-07 154307" src="https://github.com/user-attachments/assets/2cda6539-c27b-4df3-8f55-13ec16103793" />


  <h2>📊 Architecture Diagram</h2>
  <div class="diagram">
    <img width="600" height="350"  src="https://copilot.microsoft.com/th/id/BCO.db0e21e7-25c9-4df9-a44b-69ca2f568bd5.png" alt="Architecture Diagram" />
    <p><em>Diagram: Frontend (Vercel) → Backend (Render) → Database + Telegram Bot (AWS ECS)</em></p>
  </div>

  <h2>📄 License</h2>
  <p>This project is licensed under the MIT License. See the <code>LICENSE</code> file for details.</p>

  <h2>🤝 Contributing</h2>
  <p>Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.</p>

  <h2>📬 Contact</h2>
  <ul>
    <li>GitHub: <a href="https://github.com/Amenkhnisi" target="_blank">@Amenkhnisi</a></li>
    <li>Telegram: <code><img width="150" height="150" alt="image" src="https://github.com/user-attachments/assets/1dd5d0a3-470a-488a-8c6f-af162f54ef08" />
</code></li>
  </ul>

  <h2>🌟 Acknowledgments</h2>
  <ul>
    <li>German civic tech community</li>
    <li>FastAPI & React contributors</li>
    <li>OpenAPI ecosystem</li>
  </ul>


