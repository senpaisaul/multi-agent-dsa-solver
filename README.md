# Multi-Agent DSA Solver

This project implements a multi-agent system designed to solve Data Structures and Algorithms (DSA) and Competitive Programming problems autonomously. It utilizes a team of specialized AI agents to decompose, plan, design, implement, and review solutions.

## Project Structure

- **`orchestrator.py`**: The main entry point of the application. It orchestrates the entire workflow, managing the interaction between different agents and phases (Decomposition, Planning, Design, Development, Review).
- **`agents.py`**: Defines the `Agent` base class and specific agent roles:
  - `Decomposer`: Breaks down the problem into mathematical and algorithmic sub-tasks.
  - `Manager`: Plans the development process and coordinates experts.
  - `AlgorithmExpert`: Designs the optimal algorithm.
  - `IOExpert`: Handles efficient Input/Output strategies.
  - `Developer`: Implements the solution in Python.
  - `Reviewer`: specifices quality assurance and correctness checks.
- **`utils.py`**: Contains utility functions for file operations and interactions with the OpenAI API.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**:
    - Create a `.env` file in the root directory.
    - Add your OpenAI API key:
      ```
      OPENAI_API_KEY=your_api_key_here
      ```
      *(Note: The `utils.py` handles loading this file)*

## Usage

1.  Place your problem statement in a file named `PROBLEM.txt`.
2.  Run the orchestrator:
    ```bash
    python orchestrator.py
    ```
3.  The system will:
    - Read the problem from `PROBLEM.txt`.
    - Go through decomposition, planning, and design phases.
    - Generate a solution in `solution.py`.
    - Review and refine the solution if necessary.

## Inputs and Outputs

- **Input**: `PROBLEM.txt` (The problem statement).
- **Output**: `solution.py` (The generated Python solution code).

## License

[MIT License](LICENSE)
