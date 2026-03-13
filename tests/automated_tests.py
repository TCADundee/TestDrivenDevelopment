#This file was originally used in place of pytest to run all tests in a specific order. It has since been replaced by pytest, but is kept here for reference and potential future use.
import sys
import inspect
import os
import io
import threading
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import test_question
import test_quiz
import test_quiz_manager
import test_scoreboard

class CapsysCapture:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._out = StringIO()
        self._err = StringIO()
        self._old_stdout = None
        self._old_stderr = None
    
    def start_capture(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        self._out = io.StringIO()
        self._err = io.StringIO()
        sys.stdout = self._out
        sys.stderr = self._err
    
    def stop_capture(self):
        if self._old_stdout:
            sys.stdout = self._old_stdout
        if self._old_stderr:
            sys.stderr = self._old_stderr
    
    def readouterr(self):
        class Output:
            def __init__(self, out, err):
                self.out = out.getvalue()
                self.err = err.getvalue()
        return Output(self._out, self._err)

def get_initial_files():
    quizzes_dir = "quizzes"
    initial_files = set()
    
    if os.path.exists(quizzes_dir):
        for file in os.listdir(quizzes_dir):
            initial_files.add(file)
    
    return initial_files

def cleanup_test_files(initial_files):
    quizzes_dir = "quizzes"
    
    if not os.path.exists(quizzes_dir):
        return
    
    current_files = set(os.listdir(quizzes_dir))
    files_to_delete = current_files - initial_files
    
    for file in files_to_delete:
        file_path = os.path.join(quizzes_dir, file)
        try:
            os.remove(file_path)
        except Exception as e:
            continue
    
    print(f"{'='*60}\n")

def get_test_functions_in_order(module):
    """Get test functions from module in the order they appear in the source file."""
    try:
        source = inspect.getsource(module)
        lines = source.split('\n')
        
        test_functions = []
        for line in lines:
            if line.startswith('def test_'):
                # Extract function name
                func_name = line.split('(')[0].replace('def ', '').strip()
                # Get the actual function object
                if hasattr(module, func_name):
                    test_functions.append((func_name, getattr(module, func_name)))
        
        return test_functions
    except:
        # Fallback to alphabetical order if source inspection fails
        return [(name, obj) for name, obj in inspect.getmembers(module) 
                if name.startswith("test_") and callable(obj)]

def run_all_tests(initial_files):
    test_modules = [test_question, test_quiz, test_quiz_manager, test_scoreboard]
    # test_modules = [test_quiz_manager]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    errors = []

    for module in test_modules:
        try:
            print(f"\n{'='*60}")
            print(f"Running tests from {module.__name__}")
            print(f"{'='*60}")
            
            for name, obj in get_test_functions_in_order(module):
                total_tests += 1
                test_name = f"{module.__name__}.{name}"
                
                try:
                    sig = inspect.signature(obj)
                    params = list(sig.parameters.keys())
                    
                    if "capsys" in params:
                        capsys = CapsysCapture()
                        try:
                            capsys.start_capture()
                            obj(capsys)
                        finally:
                            capsys.stop_capture()
                    else:
                        obj()
                    
                    print(f"✓ PASSED: {test_name}")
                    passed_tests += 1
                    
                except AssertionError as e:
                    print(f"✗ FAILED: {test_name}")
                    print(f"  AssertionError: {e}")
                    failed_tests += 1
                    errors.append((test_name, str(e)))
                    
                except Exception as e:
                    print(f"✗ ERROR: {test_name}")
                    print(f"  {type(e).__name__}: {e}")
                    failed_tests += 1
                    errors.append((test_name, f"{type(e).__name__}: {e}"))
        except Exception as e:
            print(f"Error processing module {module.__name__}: {type(e).__name__}: {e}")
            continue
    
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    
    if errors:
        print(f"\n{'='*60}")
        print("FAILURES AND ERRORS")
        print(f"{'='*60}")
        for test_name, error in errors:
            print(f"\n{test_name}")
            print(f"  {error}")
    
    print(f"\n{'='*60}\n")
    
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    initial_files = get_initial_files()
    exit_code = run_all_tests(initial_files)
    cleanup_test_files(initial_files)
    sys.exit(exit_code)
