# AndesAI
AndesAI is an intelligent project planning assistant powered by Llama LLM technology that helps teams and individuals streamline their project planning process through interactive guidance and automated visualization tools.

## Features

### Interactive Project Planning
- Guided brainstorming sessions to help identify project goals and scope
- Smart task breakdown that helps convert high-level objectives into actionable items
- Resource constraint analysis and optimization suggestions
- Data-driven estimation support for task durations and resource allocation

### Visualization Tools
- Automated Gantt Chart generation for project timeline visualization
- Interactive Kanban Board creation in Jira-style format
- Real-time updates and modifications to project visualizations
- Export capabilities to common project management formats

### AI-Powered Insights
- Intelligent suggestions based on project context and constraints
- Risk identification and mitigation recommendations
- Resource optimization proposals
- Timeline feasibility analysis

## Getting Started

### Prerequisites
- Docker installation
- Llama Model Deployment and OpenAI-style API access
- Python 3.8 or higher

### Open WebUI installation
```
docker run -d -p 8000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:latest
```

### Configuration
1. Access the Web Interface http://localhost:8000
2. Setup Model API Endpoint
Admin Panel -> Settings -> Connections - Manage OpenAI API Connections
2. Setup Function
Admin Panel -> Functions -> Create Functions -> Enter *visualise.py* content -> Enable the function
3. Setup Model
Workspace -> Models -> Create Model -> Name the model as AndesAI -> Enter *system_prompt.txt* content as system prompt -> Enable Visualise Action -> Upload *andesai.png* as model profile image

### Usage
1. Start chat:
New Chat -> Select AndesAI -> Describe your project ideas
2. Follow the AI's guidance and answer the questions accordingly
3. Once AndesAI has suggested it has enough information or provided a summary of your project plan, click the triple 4-point star button named "Visualise". AndesAI will be able to product a Gantt Chart and a Jira-style Kanban Board for your project.

## Architecture

AndesAI is built on three main components:
- Frontend: Open WebUI interface for user interaction
- Backend: Open WebUI integrated pipeline (To be extended to Python-based server and vector-database for better data processing)
- LLM Integration: Llama Model API for intelligent processing and suggestions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Llama Model team for their excellent LLM technology
- Open WebUI community for the robust interface framework

---

Made with ❤️ by the AndesAI Team during Llama Hackathon Oslo.