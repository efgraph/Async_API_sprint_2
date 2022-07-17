import subprocess

def run_postman_tests(state):
    if not state.get_state('postman_tests'):
        state.set_state('postman_tests', True)
        subprocess.call(['newman', 'run', './postman_collection.json'])