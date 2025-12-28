from utils import read_file, write_file
from agents import Decomposer, Manager, AlgorithmExpert, IOExpert, Developer, Reviewer

def main():
    print("Starting Multi-Agent DSA Solver...")
    
    # 1. Ingestion
    problem_file = "PROBLEM.txt"
    problem_text = read_file(problem_file)
    if not problem_text or not problem_text.strip():
        print(f"CRITICAL ERROR: {problem_file} is empty or missing.")
        print(f"Please paste the problem statement into {problem_file} and try again.")
        return

    print(f"Read problem from {problem_file} ({len(problem_text)} chars).\n")

    # Initialize Agents
    decomposer = Decomposer("Decomposer", "Lead Decomposer")
    manager = Manager("Manager", "Project Manager")
    algo_expert = AlgorithmExpert("AlgoExpert", "Algorithm Specialist")
    io_expert = IOExpert("IOExpert", "IO Architect")
    developer = Developer("Developer", "Senior Developer")
    reviewer = Reviewer("Reviewer", "QA Lead")

    # 2. Decomposition Phase
    print("\n--- Phase 1: Decomposition ---")
    decomposition_result = decomposer.process(problem_text)
    print(f"Decomposition Output:\n{decomposition_result[:500]}...\n")

    # 3. Planning Phase
    print("\n--- Phase 2: Manager Planning ---")
    plan = manager.process(f"Here is the problem breakdown: {decomposition_result}")
    print(f"Manager Plan:\n{plan[:500]}...\n")

    # 4. Design Phase (Parallel-ish)
    print("\n--- Phase 3: Expert Design ---")
    
    algo_design = algo_expert.process(f"Problem Breakdown: {decomposition_result}\nManager Plan: {plan}")
    print(f"Algorithm Design:\n{algo_design[:500]}...\n")

    io_design = io_expert.process(f"Problem Breakdown: {decomposition_result}\nManager Plan: {plan}")
    print(f"IO Design:\n{io_design[:500]}...\n")

    # 5. Implementation Phase
    print("\n--- Phase 4: Development ---")
    dev_context = f"""
    Here is the Algorithm Design:
    {algo_design}
    
    Here is the IO Strategy:
    {io_design}
    
    Please write the full 'solution.py'.
    """
    initial_code = developer.process(dev_context)
    
    # Clean up code block (remove markdown backticks if present)
    clean_code = initial_code.replace("```python", "").replace("```", "").strip()
    write_file("solution.py", clean_code)
    print("Draft solution written to solution.py")

    # 6. Review Phase
    print("\n--- Phase 5: Review & Refine ---")
    review_feedback = reviewer.process(f"Here is the generated code:\n{clean_code}\n\nProblem context:\n{problem_text}")
    
    if "APPROVED" in review_feedback.upper():
        print("Reviewer APPROVED the solution.")
    else:
        print("Reviewer found issues. Sending back to Developer...")
        print(f"Feedback: {review_feedback}")
        
        fix_context = f"""
        The Reviewer found the following issues:
        {review_feedback}
        
        Please fix the code above and output the FULL corrected 'solution.py'.
        """
        fixed_code = developer.process(fix_context, previous_messages=[
            {"role": "assistant", "content": initial_code},
            {"role": "user", "content": fix_context}
        ])
        
        final_code = fixed_code.replace("```python", "").replace("```", "").strip()
        write_file("solution.py", final_code)
        print("Final solution written to solution.py")

    print("\nWorkflow Complete.")

if __name__ == "__main__":
    main()
