# Gemini-Interpreter

Gemini-Interpreter is a tool for interacting with language models built on **Gemini**. It is designed for executing natural language commands, data analysis, context management, and automating programming tasks using a powerful AI engine.

## Key Features

- **Gemini Integration**: Leverages the Gemini model for contextual interpretation of commands and user interaction, making the project cost-effective.
- **Python Support**: Works Python.
- **Natural Language Command Execution**: Write instructions in natural language, and the tool interprets and executes them.
- **Workflow Automation**: Code generation, execution, debugging, file and database management, and system command execution.
- **Explanation and Optimization**: Explains actions and suggests optimal solutions for tasks.

## Use Cases

- Generate and execute code based on textual descriptions.
- Manage files and execute system commands via natural language.
- Automate programming and data analysis processes.
- Serve as an educational platform for learning AI interactions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/python-shik/gemini-interpreter.git
   cd gemini-interpreter
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```bash
python main.py
```

### Interaction Examples

- **Example 1**: Executing a natural language command.
  ```
  >>> Write a function that calculates the factorial of a number.
  Generated:
  def factorial(n):
      if n == 0:
          return 1
      return n * factorial(n - 1)

  # Example input and output for clarity:
  >>> factorial(5)
  120
  ```

- **Example 2**: Executing a system command.
  ```
  >>> Create a new folder "Project" and move all .txt files into it.
  Executed: Folder "Project" created, .txt files moved.
  ```

- **Example 3**: Explaining complex code.
  ```
  >>> Explain what this code does: 
  def quicksort(arr):
      if len(arr) <= 1:
          return arr
      pivot = arr[len(arr) // 2]
      left = [x for x in arr if x < pivot]
      middle = [x for x in arr if x == pivot]
      right = [x for x in arr if x > pivot]
      return quicksort(left) + middle + quicksort(right)

  Response:
  This code implements the quicksort algorithm, which recursively sorts a list...
  ```

### Jailbreak Mode

You can try jailbreak mode with default jailbreak prompt.
```bash
python main.py --jailbreak
```

### Temperature set

You can set the temperature of the Model. 
(default: 1.0   min: 0.1   max: 2.0)
```bash
python main.py --temperature 0.7 
```


## Expansion Opportunities

- Support for additional programming languages.
- Integration with external services for data analysis or API requests, such as Google Cloud AI, AWS Lambda, or OpenAI APIs.
- Improved natural language processing.
- Development of a web interface for browser-based usage.

## Contributing

We welcome your suggestions and contributions! To contribute:
1. Fork the repository.
2. Create a branch with your changes:
   ```bash
   git checkout -b feature-name
   ```
3. Submit a Pull Request with a description of your changes.

## Contact

If you have questions or suggestions, feel free to create an Issue or contact the project author.
