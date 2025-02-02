"""
Acknowledgement: Edit from Iqbal's template
title: Make charts out of your data v2
author: Iqbal Maulana
author_url: https://github.com/iqballx?tab=repositories
author_linkedin: https://www.linkedin.com/in/iqbaalm/
funding_url: https://github.com/open-webui
version: 2.0.0
"""

import httpx
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os
from open_webui.models.files import Files
import uuid
import logging
from openai import AsyncOpenAI
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT_GANTT_CHART = """

Objective:
Your goal is to read the project task/resource data, schedule the task, present the data using Gantt Chart and produce the HTML to display it.

Steps:

	1.	Read and Examine the project task/resource data:
	•	Understand the tasks to be completed, resource available, and resource required to complete each task.
	2.	Schedule the Task:
	•	Schedule the task in a temporal manner, considering the priority and resource constrains
	3.	Generate HTML:
	•	Create the HTML code to present the data using the Gantt Chart.
    4.	Calibrate the chart scale based on the data:
	•	based on the data try to make the scale of the chart as readable as possible.

Key Considerations:

	-	Your output should only include HTML code, without any additional text.
    -   Generate only HTML. Do not include any additional words or explanations.
    -   Make to remove any character other non alpha numeric from the data.
    -   is the generated HTML Calibrate the chart scale based on the data for eveything to be readable.
    -   Generate complete html code.

Example (Number of Days are Indicative, Please adjust accordingly): 
<!DOCTYPE html>
<html>
<head>
    <style>
        .gantt-container {
            padding: 20px;
            font-family: Arial, sans-serif;
        }

        .gantt-header {
            display: grid;
            grid-template-columns: 200px repeat(30, 30px);
            margin-bottom: 10px;
        }

        .day-header {
            text-align: center;
            font-weight: bold;
            font-size: 12px;
            padding: 5px;
            background-color: #f0f0f0;
            border-right: 1px solid #ddd;
        }

        .gantt-body {
            display: grid;
            grid-template-columns: 200px repeat(30, 30px);
        }

        .task-name {
            padding: 10px;
            font-size: 14px;
            border-bottom: 1px solid #ddd;
            background-color: #f8f8f8;
        }

        .task-cell {
            border-right: 1px solid #eee;
            border-bottom: 1px solid #ddd;
            position: relative;
        }

        .task-bar {
            position: absolute;
            height: 80%;
            top: 10%;
            border-radius: 3px;
            transition: all 0.3s ease;
        }

        .task-bar:hover {
            opacity: 0.8;
            transform: scale(1.02);
        }

        .task-1 { background-color: #FF6B6B; }
        .task-2 { background-color: #4ECDC4; }
        .task-3 { background-color: #45B7D1; }
        .task-4 { background-color: #96CEB4; }
        .task-5 { background-color: #FFEEAD; }
    </style>
</head>
<body>
    <div class="gantt-container">
        <div class="gantt-header">
            <div class="day-header">Tasks</div>
            <!-- Generate 30 day headers -->
            <script>
                for (let i = 1; i <= 30; i++) {
                    document.write(`<div class="day-header">${i}</div>`);
                }
            </script>
        </div>
        <div class="gantt-body">
            <!-- Task 1 -->
            <div class="task-name">Project Planning</div>
            <script>
                for (let i = 1; i <= 30; i++) {
                    const cell = `<div class="task-cell">
                        ${i >= 1 && i <= 5 ? '<div class="task-bar task-1" style="width: 100%;"></div>' : ''}
                    </div>`;
                    document.write(cell);
                }
            </script>

            <!-- Task 2 -->
            <div class="task-name">Design Phase</div>
            <script>
                for (let i = 1; i <= 30; i++) {
                    const cell = `<div class="task-cell">
                        ${i >= 4 && i <= 10 ? '<div class="task-bar task-2" style="width: 100%;"></div>' : ''}
                    </div>`;
                    document.write(cell);
                }
            </script>

            <!-- Task 3 -->
            <div class="task-name">Development</div>
            <script>
                for (let i = 1; i <= 30; i++) {
                    const cell = `<div class="task-cell">
                        ${i >= 8 && i <= 20 ? '<div class="task-bar task-3" style="width: 100%;"></div>' : ''}
                    </div>`;
                    document.write(cell);
                }
            </script>

            <!-- Task 4 -->
            <div class="task-name">Testing</div>
            <script>
                for (let i = 1; i <= 30; i++) {
                    const cell = `<div class="task-cell">
                        ${i >= 18 && i <= 25 ? '<div class="task-bar task-4" style="width: 100%;"></div>' : ''}
                    </div>`;
                    document.write(cell);
                }
            </script>

            <!-- Task 5 -->
            <div class="task-name">Deployment</div>
            <script>
                for (let i = 1; i <= 30; i++) {
                    const cell = `<div class="task-cell">
                        ${i >= 24 && i <= 28 ? '<div class="task-bar task-5" style="width: 100%;"></div>' : ''}
                    </div>`;
                    document.write(cell);
                }
            </script>
        </div>
    </div>
</body>
</html>
"""

SYSTEM_PROMPT_KANBAN_BOARD = """

Objective:
Your goal is to read the project task/resource data, present the data using Jira-style Kanban Board and produce the HTML to display it.

Steps:

	1.	Read and Examine the project task/resource data:
	•	Understand the tasks to be completed.
	3.	Generate HTML:
	•	Create the HTML code to present the data using the Jira-style Kanban Board.
    4.	Calibrate the chart scale based on the data:
	•	based on the data try to make the scale of the chart as readable as possible.

Key Considerations:

	-	Your output should only include HTML code, without any additional text.
    -   Generate only HTML. Do not include any additional words or explanations.
    -   Make to remove any character other non alpha numeric from the data.
    -   is the generated HTML Calibrate the chart scale based on the data for eveything to be readable.
    -   Generate complete html code.

Example: 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, "Helvetica Neue", Arial, sans-serif;
        }

        :root {
            --primary-bg: #0052CC;
            --secondary-bg: #F4F5F7;
            --card-bg: #FFFFFF;
            --text-primary: #172B4D;
            --text-secondary: #5E6C84;
            --border-color: #DFE1E6;
            --column-width: 300px;
        }

        body {
            background-color: var(--secondary-bg);
            color: var(--text-primary);
        }

        .header {
            background-color: var(--primary-bg);
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            font-size: 1.5rem;
            font-weight: 500;
        }

        .board-container {
            padding: 2rem;
            overflow-x: auto;
        }

        .board {
            display: flex;
            gap: 1rem;
            min-height: calc(100vh - 150px);
        }

        .column {
            background: var(--secondary-bg);
            border-radius: 8px;
            min-width: var(--column-width);
            max-width: var(--column-width);
        }

        .column-header {
            padding: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .column-count {
            background: var(--border-color);
            border-radius: 12px;
            padding: 0.25rem 0.75rem;
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        .column-content {
            padding: 0.5rem;
            min-height: 100px;
        }

        .card {
            background: var(--card-bg);
            border-radius: 6px;
            padding: 1rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
        }

        .card-title {
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        .card-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        .priority {
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .priority-high {
            background: #FFEBE6;
            color: #DE350B;
        }

        .priority-medium {
            background: #E3FCEF;
            color: #006644;
        }

        .priority-low {
            background: #DEEBFF;
            color: #0747A6;
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>Project Alpha Kanban Board</h1>
    </header>

    <div class="board-container">
        <div class="board">
            <div class="column">
                <div class="column-header">
                    <span>To Do</span>
                    <span class="column-count">8</span>
                </div>
                <div class="column-content">
                    <div class="card">
                        <div class="card-title">Implement user authentication</div>
                        <div class="card-meta">
                            <span>PROJ-123</span>
                            <span class="priority priority-high">High</span>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-title">Design landing page mockups</div>
                        <div class="card-meta">
                            <span>PROJ-124</span>
                            <span class="priority priority-medium">Medium</span>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-title">Update documentation</div>
                        <div class="card-meta">
                            <span>PROJ-125</span>
                            <span class="priority priority-low">Low</span>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-title">Integrate payment gateway</div>
                        <div class="card-meta">
                            <span>PROJ-126</span>
                            <span class="priority priority-high">High</span>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-title">Set up CI/CD pipeline</div>
                        <div class="card-meta">
                            <span>PROJ-127</span>
                            <span class="priority priority-medium">Medium</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="column">
                <div class="column-header">
                    <span>In Progress</span>
                    <span class="column-count">0</span>
                </div>
                <div class="column-content">
                </div>
            </div>

            <div class="column">
                <div class="column-header">
                    <span>Review</span>
                    <span class="column-count">0</span>
                </div>
                <div class="column-content">
                </div>
            </div>

            <div class="column">
                <div class="column-header">
                    <span>Done</span>
                    <span class="column-count">0</span>
                </div>
                <div class="column-content">
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

USER_PROMPT_GENERATE_HTML = """
Giving this query  {Query} generate the necessary html qurty.
"""

# Initialize OpenAI client


class FileData(BaseModel):
    id: str
    filename: str
    meta: Dict[str, Any]
    path: str


class Action:
    class Valves(BaseModel):
        show_status: bool = Field(
            default=True, description="Show status of the action."
        )
        html_filename: str = Field(
            default="json_visualizer.html",
            description="Name of the HTML file to be created or retrieved.",
        )
        OPENAI_KEY: str = "AndesAI"
        OPENAI_URL: str = "http://195.242.10.83:8001/v1"
        MODEL_NAME: str = "Llama3.3"

    def __init__(self):
        self.valves = self.Valves()
        self.openai = None
        self.html_content = """

        """

    def create_or_get_file(self, user_id: str, json_data: str) -> str:

        filename = str(int(time.time() * 1000)) + self.valves.html_filename
        directory = "action_embed"

        logger.debug(f"Attempting to create or get file: {filename}")

        # Check if the file already exists
        existing_files = Files.get_files()
        for file in existing_files:
            if (
                file.filename == f"{directory}/{user_id}/{filename}"
                and file.user_id == user_id
            ):
                logger.debug(f"Existing file found. Updating content.")
                # Update the existing file with new JSON data
                self.update_html_content(file.meta["path"], json_data)
                return file.id

        # If the file doesn''t exist, create it
        base_path = os.path.join("uploads", directory)
        os.makedirs(base_path, exist_ok=True)
        file_path = os.path.join(base_path, filename)

        logger.debug(f"Creating new file at: {file_path}")
        self.update_html_content(file_path, json_data)

        file_id = str(uuid.uuid4())
        meta = {
            "source": file_path,
            "title": "Modern JSON Visualizer",
            "content_type": "text/html",
            "size": os.path.getsize(file_path),
            "path": file_path,
        }

        # Create a new file entry
        file_data = FileData(
            id=file_id,
            filename=f"{directory}/{user_id}/{filename}",
            meta=meta,
            path=file_path,
        )
        new_file = Files.insert_new_file(user_id, file_data)
        logger.debug(f"New file created with ID: {new_file.id}")
        return new_file.id

    def update_html_content(self, file_path: str, html_content: str):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.debug(f"HTML content updated at: {file_path}")

    async def action(
        self,
        body: dict,
        __user__=None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> Optional[dict]:
        logger.debug(f"action:{__name__} started")

        await __event_emitter__(
            {
                "type": "status",
                "data": {
                    "description": "Analysing Data",
                    "done": False,
                },
            }
        )

        if __event_emitter__:

            original_content = body["messages"][-1]["content"]
            try:
                self.openai = AsyncOpenAI(
                    api_key=self.valves.OPENAI_KEY,
                    base_url=self.valves.OPENAI_URL,
                    http_client=httpx.AsyncClient(),
                )

                user_id = __user__["id"]
                response = await self.openai.chat.completions.create(
                    model=self.valves.MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT_GANTT_CHART},
                        {
                            "role": "user",
                            "content": USER_PROMPT_GENERATE_HTML.format(
                                Query=body["messages"][-1]["content"]
                            ),
                        },
                    ],
                    n=1,
                    stop=None,
                    temperature=0.7,
                )

                html_content = response.choices[0].message.content
                file_id = self.create_or_get_file(user_id, html_content)
                html_embed_tag_gantt_chart = f"{{{{HTML_FILE_ID_{file_id}}}}}"

                response = await self.openai.chat.completions.create(
                    model=self.valves.MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT_KANBAN_BOARD},
                        {
                            "role": "user",
                            "content": USER_PROMPT_GENERATE_HTML.format(
                                Query=body["messages"][-1]["content"]
                            ),
                        },
                    ],
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                html_content = response.choices[0].message.content
                file_id = self.create_or_get_file(user_id, html_content)
                html_embed_tag_kanban_board = f"{{{{HTML_FILE_ID_{file_id}}}}}"

                # Append the HTML embed tag to the original content on a new line
                body["messages"][-1][
                    "content"
                ] = f"{original_content}\n\n{html_embed_tag_gantt_chart}\n\n{html_embed_tag_kanban_board}"

                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Visualise the chart",
                            "done": True,
                        },
                    }
                )
                logger.debug(f" objects visualized")

            except Exception as e:
                error_message = f"Error visualizing JSON: {str(e)}"
                logger.error(f"Error: {error_message}")
                body["messages"][-1]["content"] += f"\n\nError: {error_message}"

                if self.valves.show_status:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": "Error Visualizing JSON",
                                "done": True,
                            },
                        }
                    )

        logger.debug(f"action:{__name__} completed")
        return body
