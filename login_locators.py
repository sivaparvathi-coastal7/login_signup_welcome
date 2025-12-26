class LoginLocators:
    """
    Updated locators for the Login page matching JSON test case specifications
    Resolves conflicts between getByLabelText, current tests, and modal elements
    """

    # -----------------------------
    # Branding / Logo
    # -----------------------------
    SNAPPOD_LOGO_IMG = "[alt='SnapPod Logo']"  # From JSON: getByAltText('SnapPod Logo')
    LOGO_IMG = "[alt='Logo']"  # Alternative logo selector

    # -----------------------------
    # Headings & Text
    # -----------------------------
    WELCOME_BACK_H2 = "h2:has-text('Welcome Back!')"  # From JSON: getByRole('heading', { name: 'Welcome Back!' })
    OR_TEXT = "text=or"  # From JSON: getByText('or')
    DONT_HAVE_ACCOUNT_TEXT = "text=Don't have an account?"  # From JSON: getByText('Don\\'t have an account?')
    SIGNUP_QUESTION_DIV = "text=Don't have an account?"  # For current test compatibility

    # -----------------------------
    # Form Inputs - Primary selectors (reliable)
    # -----------------------------
    EMAIL_INPUT = "input[type='email']"  # Reliable email input selector
    PASSWORD_INPUT = "input[type='password']"  # Reliable password input selector

    # -----------------------------
    # Form Inputs - Alternative selectors
    # -----------------------------
    EMAIL_INPUT_ALT = "input[type='email']"  # Alternative email selector
    PASSWORD_INPUT_ALT = "input[type='password']"  # Alternative password selector

    # -----------------------------
    # Form Labels (separate from inputs)
    # -----------------------------
    EMAIL_LABEL = "label:has-text('Email')"  # Actual label elements
    PASSWORD_LABEL = "label:has-text('Password')"

    # -----------------------------
    # Password Toggle
    # -----------------------------
    SHOW_PASSWORD_BUTTON = "[aria-label='Show password']"  # From JSON: getByLabel('Show password')

    # -----------------------------
    # Navigation Links
    # -----------------------------
    FORGOT_PASSWORD_LINK = "a:has-text('Forgot Password')"  # From JSON: getByRole('link', { name: 'Forgot Password' })
    SIGNUP_HERE_LINK = "a:has-text('Sign Up Here')"  # From JSON: getByRole('link', { name: 'Sign Up Here' })

    # -----------------------------
    # Action Buttons
    # -----------------------------
    LOGIN_BUTTON = "button[type='submit']:has-text('Login')"  # More specific to avoid conflicts
    GOOGLE_LOGIN_BUTTON = "button:has-text('Sign in with Google')"  # From JSON: getByRole('button', { name: 'Sign in with Google' })

    # -----------------------------
    # Forgot Password Modal Elements
    # -----------------------------
    RESET_PASSWORD_CLOSE_BUTTON = "[aria-label='Close']"  # Modal close button
    RESET_PASSWORD_H3 = "h3:has-text('Reset Password')"  # From JSON: getByRole('heading', { name: 'Reset Password' })
    RESET_PASSWORD_DESC_P = "text=Enter your email address to receive a password reset code"  # Modal description
    RESET_PASSWORD_EMAIL_INPUT = "input[placeholder*='email']"  # Email input in modal (flexible placeholder)
    RESET_PASSWORD_SEND_CODE_BUTTON = "button:has-text('Send Reset Code')"  # Send code button

    # -----------------------------
    # Success/Error Messages (from JSON)
    # -----------------------------
    SUCCESS_MESSAGE = "text=Password reset email sent. Please check your inbox."
    INVALID_CREDENTIALS_ERROR = "text=Email does not exists,Please sign up first"

    # -----------------------------
    # Generic Elements (for current test compatibility)
    # -----------------------------
    GENERIC_DIV = "div"
    ROOT_DIV = "#root"

    # -----------------------------
    # Signup-related elements (used in current login tests)
    # -----------------------------
    START_CREATING_H1 = "h1:has-text('Start creating!')"
    ALREADY_HAVE_ACCOUNT_P = "text=Already have an account?"
    SIGNIN_HERE_LINK = "a:has-text('Sign In Here')"
    GOOGLE_SIGNUP_BUTTON = "button:has-text('Sign up with Google')"
    GOOGLE_SIGNUP_TEXT = "text=Sign up with Google"
    FACEBOOK_SIGNUP_BUTTON = "button:has-text('Sign up with Facebook')"
    FACEBOOK_SIGNUP_TEXT = "text=Sign up with Facebook"
    FIRST_NAME_INPUT = "[placeholder='Enter your first name']"
    LAST_NAME_INPUT = "[placeholder='Enter your last name']"
    PHONE_INPUT = "[placeholder*='phone']"
    CONFIRM_PASSWORD_INPUT = "[placeholder*='Re-Enter']"
    SIGNUP_BUTTON = "button[type='submit']:has-text('Sign Up')"