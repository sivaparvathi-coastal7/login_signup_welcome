import os
import sys
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
import json

# =========================
# CONFIG
# =========================
MODEL_NAME = "llama-3.3-70b-versatile"

PROJECT_ROOT = Path(__file__).resolve().parent
PROMPT_FILE = PROJECT_ROOT / "prompt.txt"

CONFIG_DIR = PROJECT_ROOT / "config"
TESTCASES_DIR = PROJECT_ROOT / "testcases"
OUTPUT_TESTS_DIR = PROJECT_ROOT / "tests"

OUTPUT_TESTS_DIR.mkdir(exist_ok=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# UTILITIES
# =========================
def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def inject_pythonpath(code: str) -> str:
    injection = (
        "import sys\n"
        "from pathlib import Path\n"
        "ROOT_DIR = Path(__file__).resolve().parent.parent\n"
        "sys.path.insert(0, str(ROOT_DIR))\n\n"
    )
    return injection + code

# =========================
# LLM INTEGRATION
# =========================
def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are an expert Playwright test automation engineer. Generate clean, executable Python test code using the provided locators and test cases."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()

def extract_code_only(text: str) -> str:
    """Extract Python code from LLM response"""
    # Handle code blocks
    if "```python" in text:
        code = text.split("```python")[1].split("```")[0].strip()
        return code
    elif "```" in text:
        code = text.split("```")[1].split("```")[0].strip()
        return code
    
    # Handle custom tags
    if "<BEGIN_CODE>" in text and "<END_CODE>" in text:
        code = text.split("<BEGIN_CODE>")[1].split("<END_CODE>")[0].strip()
        import html
        return html.unescape(code)
    
    # Return as-is if it looks like Python code
    stripped = text.strip()
    if stripped.startswith(("import ", "from ", "def ", "class ")):
        return stripped
    
    raise RuntimeError("Could not extract Python code from LLM response")
def generate_page_tests_fallback(page: str):
    """Fallback direct generation if LLM fails"""
    raw_testcase_code = read_file(TESTCASES_DIR / f"{page}_testcases.json")
    
    if not raw_testcase_code:
        return
    
    try:
        data = json.loads(raw_testcase_code)
        test_cases = data.get('testCases', [])
        
        if not test_cases:
            return
        
        # Generate test code directly from JSON inputs
        test_code = generate_imports(page)
        
        for test_case in test_cases:
            test_code += generate_test_from_inputs(test_case, page)
        
        # Apply minimal post-processing
        test_code = inject_pythonpath(test_code)
        test_code = fix_locator_usage(test_code)
        
        # Write fallback file
        test_dir = OUTPUT_TESTS_DIR / page
        out_path = test_dir / f"test_{page}.py"
        write_file(out_path, test_code)
        
        print(f"Generated fallback {out_path.name} for {page}")
        
    except Exception as e:
        print(f"Fallback generation also failed for {page}: {e}")

def generate_test_from_inputs(test_case: dict, page: str) -> str:
    """Generate individual test function using test case data"""
    test_id = test_case.get('id', '')
    title = test_case.get('title', '')
    inputs = test_case.get('inputs', {})
    steps = test_case.get('steps', [])
    expected = test_case.get('expected', [])
    
    # Convert test ID to function name
    func_name = test_id.lower().replace('_tc_', '_').replace('tc_', '')
    
    # Determine fixture type
    fixture = 'authenticated_page' if page == 'welcome' else 'page'
    
    # Generate test function with docstring
    test_code = f"def test_{func_name}({fixture}):\n"
    if title:
        test_code += f'    """Test: {title}"""\n'
    
    # Add navigation for non-welcome pages
    if page != 'welcome':
        url_var = f"{page.upper()}_URL"
        test_code += f"    {fixture}.goto({url_var}, timeout=60000)\n"
        test_code += f"    {fixture}.wait_for_load_state('networkidle')\n"
    
    # Generate test steps based on inputs
    locator_class = get_locator_class(page)
    
    # Process inputs
    for key, value in inputs.items():
        if key.endswith('_locator'):
            field_name = key.replace('_locator', '')
            if field_name in inputs:
                locator_ref = value.replace(f'{locator_class}.', '')
                test_code += f"    {fixture}.locator({locator_class}.{locator_ref}).fill('{inputs[field_name]}')\n"
        elif key.endswith(('_button', '_link', '_toggle')):
            locator_ref = value.replace(f'{locator_class}.', '')
            test_code += f"    {fixture}.locator({locator_class}.{locator_ref}).click()\n"
            test_code += f"    {fixture}.wait_for_load_state('networkidle')\n"
    
    # Handle confirm_password separately for signup
    if page == 'signup' and 'confirm_password' in inputs and 'confirm_password_locator' in inputs:
        locator_ref = inputs['confirm_password_locator'].replace(f'{locator_class}.', '')
        test_code += f"    {fixture}.locator({locator_class}.{locator_ref}).fill('{inputs['confirm_password']}')\n"
    
    # Add assertions based on test type
    if 'empty' in test_id.lower():
        if 'email' in inputs and inputs['email'] == '':
            test_code += f"    expect({fixture}.locator({locator_class}.EMAIL_INPUT)).to_have_js_property('validationMessage', 'Please fill out this field.')\n"
        elif 'password' in inputs and inputs['password'] == '':
            test_code += f"    expect({fixture}.locator({locator_class}.PASSWORD_INPUT)).to_have_js_property('validationMessage', 'Please fill out this field.')\n"
    elif 'invalid' in test_id.lower():
        if page == 'login':
            test_code += f"    expect({fixture}).to_have_url(LOGIN_URL)\n"
        elif page == 'signup':
            test_code += f"    expect({fixture}).to_have_url(SIGNUP_URL)\n"
    elif 'valid' in test_id.lower() and page == 'login':
        test_code += f"    expect({fixture}).not_to_have_url(LOGIN_URL)\n"
    elif 'modal' in test_id.lower():
        for key, value in inputs.items():
            if key.endswith(('_heading', '_modal')):
                locator_ref = value.replace(f'{locator_class}.', '')
                test_code += f"    expect({fixture}.locator({locator_class}.{locator_ref})).to_be_visible()\n"
                break
    
    return test_code + "\n"

def get_locator_class(page: str) -> str:
    """Get the appropriate locator class for the page"""
    mapping = {
        'login': 'LoginLocators',
        'signup': 'SignupLocators', 
        'welcome': 'WelcomeLocators'
    }
    return mapping.get(page, 'LoginLocators')

def generate_imports(page: str) -> str:
    """Generate appropriate imports for the page"""
    locator_class = get_locator_class(page)
    module_name = f"{page}_locators"
    
    imports = [
        "import sys",
        "from pathlib import Path", 
        "ROOT_DIR = Path(__file__).resolve().parent.parent",
        "sys.path.insert(0, str(ROOT_DIR))",
        "",
        f"from config.{module_name} import {locator_class}",
        "from playwright.sync_api import expect"
    ]
    
    if page != 'welcome':
        imports.insert(-1, f"from config.urls import {page.upper()}_URL")
    
    return "\n".join(imports) + "\n\n"

def fix_locator_usage(code: str) -> str:
    """Fix locator usage patterns"""
    import re
    
    # Fix expect patterns for visibility
    code = re.sub(r'expect\(page\.locator\(([^)]+)\)\)\.be_visible\(\)', r'expect(page.locator(\1)).to_be_visible()', code)
    code = re.sub(r'expect\(page\.locator\(([^)]+)\)\)\.to_have_js_property', r'expect(page.locator(\1)).to_have_js_property', code)
    
    # Remove any remaining 'await' keywords
    code = re.sub(r'\bawait\s+', '', code)
    
    return code

# =========================
# PAGE DISCOVERY
# =========================
def infer_pages():
    pages = []
    for tc_file in TESTCASES_DIR.glob("*_testcases.json"):
        page = tc_file.stem.replace("_testcases", "")
        locator_file = CONFIG_DIR / f"{page}_locators.py"
        if locator_file.exists():
            pages.append(page)
    return pages

# =========================
# GENERATE conftest.py
# =========================
def generate_conftest():
    content = """
import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
import logging
import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def context(browser, request):
    # Create unique video directory for each test
    test_name = request.node.name
    videos_dir = Path(f"videos/{test_name}")
    videos_dir.mkdir(parents=True, exist_ok=True)
    
    context = browser.new_context(record_video_dir=str(videos_dir))
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def authenticated_page(context):
    \"\"\"Login and navigate to welcome page with proper waits\"\"\"
    page = context.new_page()
    
    # Navigate to login with timeout
    page.goto("https://dev.vox.snappod.ai/login", timeout=30000)
    page.wait_for_load_state('domcontentloaded', timeout=15000)
    
    # Fill credentials with explicit waits
    email_input = page.locator("#login-email")
    email_input.wait_for(state='visible', timeout=10000)
    email_input.fill("tadikamallasivaparvathi@gmail.com")
    
    password_input = page.locator("#login-password")
    password_input.wait_for(state='visible', timeout=10000)
    password_input.fill("Siva@2001")
    
    # Click login and wait for navigation
    login_button = page.locator("button:has-text('Login')")
    login_button.wait_for(state='visible', timeout=10000)
    login_button.click()
    
    # Wait for login to complete
    page.wait_for_load_state('networkidle', timeout=20000)
    
    # Navigate to welcome page if not already there
    if 'welcome-to-snappod-ai' not in page.url:
        page.goto("https://dev.vox.snappod.ai/welcome-to-snappod-ai", timeout=30000)
        page.wait_for_load_state('domcontentloaded', timeout=15000)
    
    yield page
    page.close()

@pytest.fixture(autouse=True)
def log_test_info(request):
    test_name = request.node.name
    
    # Create separate log file for each test
    log_dir = Path("test_logs")
    log_dir.mkdir(exist_ok=True)
    
    test_logger = logging.getLogger(test_name)
    test_logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    for handler in test_logger.handlers[:]:
        test_logger.removeHandler(handler)
    
    # Add file handler for individual test
    file_handler = logging.FileHandler(f"test_logs/{test_name}.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    test_logger.addHandler(file_handler)
    
    test_logger.info(f"Starting test: {test_name}")
    start_time = datetime.datetime.now()
    
    yield
    
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    if hasattr(request.node, 'rep_call'):
        outcome = "PASSED" if request.node.rep_call.passed else "FAILED"
        if request.node.rep_call.failed:
            test_logger.error(f"Test {test_name}: {outcome} - Duration: {duration:.2f}s - Error: {request.node.rep_call.longrepr}")
        else:
            test_logger.info(f"Test {test_name}: {outcome} - Duration: {duration:.2f}s")
    else:
        test_logger.info(f"Test {test_name}: COMPLETED - Duration: {duration:.2f}s")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
"""
    write_file(OUTPUT_TESTS_DIR / "conftest.py", content.strip())
    print("conftest.py generated")

# =========================
# GENERATE TESTS PER PAGE
# =========================
def generate_page_tests(page: str, base_prompt: str):
    # Read locators and test cases
    locator_code = read_file(CONFIG_DIR / f"{page}_locators.py")
    testcase_code = read_file(TESTCASES_DIR / f"{page}_testcases.json")
    
    if not locator_code:
        print(f"Warning: No locators found for {page}")
        return
        
    if not testcase_code:
        print(f"Warning: No test cases found for {page}")
        return
    
    # Create comprehensive prompt for LLM
    page_prompt = f"""
{base_prompt}

PAGE: {page}

LOCATORS FILE CONTENT:
{locator_code}

TEST CASES JSON:
{testcase_code}

INSTRUCTIONS:
1. Read the locators from the {page}_locators.py file
2. Read the test cases from the JSON file
3. Generate one test function per test case using the specific inputs from each test case
4. Use the locator class references (e.g., {get_locator_class(page)}.EMAIL_INPUT)
5. Use the actual input values from each test case (not hardcoded values)
6. For welcome page, use authenticated_page fixture; for others use page fixture
7. Add proper assertions based on test case expectations

Generate complete Playwright pytest test file. Output ONLY Python code.
"""
    
    try:
        # Call LLM to generate tests
        print(f"Generating tests for {page} using LLM...")
        raw_output = call_llm(page_prompt)
        
        # Extract code from LLM response
        test_code = extract_code_only(raw_output)
        
        # Apply post-processing
        test_code = inject_pythonpath(test_code)
        test_code = fix_locator_usage(test_code)
        
        # Determine output file
        test_dir = OUTPUT_TESTS_DIR / page
        existing_files = list(test_dir.glob("*test*.py")) if test_dir.exists() else []
        
        if existing_files:
            out_path = existing_files[0]
        else:
            out_path = test_dir / f"test_{page}.py"
        
        write_file(out_path, test_code)
        
        print(f"Generated {out_path.name} for {page} using LLM")
        
    except Exception as e:
        print(f"Error generating tests for {page}: {e}")
        # Fallback to direct generation if LLM fails
        print(f"Falling back to direct generation for {page}")
        generate_page_tests_fallback(page)

# =========================
# MAIN
# =========================
def main():
    print("Generating tests using LLM (Groq) integration")

    base_prompt = read_file(PROMPT_FILE)
    if not base_prompt:
        raise RuntimeError("prompt.txt is empty or missing")

    pages = infer_pages()
    if not pages:
        raise RuntimeError("No pages detected")

    generate_conftest()

    for page in pages:
        generate_page_tests(page, base_prompt)

    print("LLM-based test generation completed successfully")

if __name__ == "__main__":
    main()