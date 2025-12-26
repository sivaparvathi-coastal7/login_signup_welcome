class SignupLocators:
    """
    Updated locators for the Sign-Up page matching JSON test case specifications
    Resolves conflicts between getByLabelText, getByPlaceholderText, and current test requirements
    """

    # -----------------------------
    # Branding / Logo
    # -----------------------------
    SNAPPOD_LOGO_IMG = "[alt='Logo']"  # From JSON: getByAltText('Logo')
    LOGO_IMG = "[alt='Logo']"

    # -----------------------------
    # Headings & Text
    # -----------------------------
    START_CREATING_H1 = "h1:has-text('Start creating!')"  # From JSON: getByRole('heading', { name: 'Start creating!' })
    ALREADY_HAVE_ACCOUNT_P = "text=Already have an account?"  # From JSON: getByText('Already have an account?')

    # -----------------------------
    # Navigation Links
    # -----------------------------
    SIGNIN_HERE_LINK = "a:has-text('Sign In Here')"  # From JSON: getByRole('link', { name: 'Sign In Here' })

    # -----------------------------
    # Social Sign-Up Options
    # -----------------------------
    GOOGLE_SIGNUP_BUTTON = "button:has-text('Sign up with Google')"  # From JSON: getByRole('button', { name: 'Sign up with Google' })
    GOOGLE_SIGNUP_TEXT = "text=Sign up with Google"  # For current test compatibility
    FACEBOOK_SIGNUP_BUTTON = "button:has-text('Sign up with Facebook')"  # From JSON: getByRole('button', { name: 'Sign up with Facebook' })
    FACEBOOK_SIGNUP_TEXT = "text=Sign up with Facebook"  # For current test compatibility

    # -----------------------------
    # User Input Fields - Primary selectors (JSON placeholder-based)
    # -----------------------------
    FIRST_NAME_INPUT = "[placeholder='Enter your first name']"  # From JSON: getByPlaceholderText('Enter your first name')
    LAST_NAME_INPUT = "[placeholder='Enter your last name']"  # From JSON: getByPlaceholderText('Enter your last name')
    PHONE_INPUT = "[placeholder='1 (702) 123-4567']"  # From JSON: getByPlaceholderText('1 (702) 123-4567')
    EMAIL_INPUT = "[placeholder='Enter your Email Address']"  # From JSON: getByPlaceholderText('Enter your Email Address')
    PASSWORD_INPUT = "[placeholder='Enter password']"  # From JSON: getByPlaceholderText('Enter password')
    CONFIRM_PASSWORD_INPUT = "[placeholder='Re-Enter your Password']"  # From JSON: getByPlaceholderText('Re-Enter your Password')

    # -----------------------------
    # User Input Fields - Alternative selectors (JSON label-based)
    # -----------------------------
    FIRST_NAME_INPUT_LABEL = "[aria-label='First Name *']"  # From JSON: getByLabelText('First Name *')
    LAST_NAME_INPUT_LABEL = "[aria-label='Last Name *']"  # From JSON: getByLabelText('Last Name *')
    PHONE_INPUT_LABEL = "[aria-label='Phone Number']"  # From JSON: getByLabelText('Phone Number')
    EMAIL_INPUT_LABEL = "[aria-label='Email *']"  # From JSON: getByLabelText('Email *')
    PASSWORD_INPUT_LABEL = "[aria-label='Password *']"  # From JSON: getByLabelText('Password *')
    CONFIRM_PASSWORD_INPUT_LABEL = "[aria-label='Re-Enter Password *']"  # From JSON: getByLabelText('Re-Enter Password *')

    # -----------------------------
    # Form Labels (separate from inputs)
    # -----------------------------
    FIRST_NAME_LABEL = "label:has-text('First Name')"  # Actual label elements
    LAST_NAME_LABEL = "label:has-text('Last Name')"
    PHONE_LABEL = "label:has-text('Phone Number')"
    EMAIL_LABEL = "label:has-text('Email')"
    PASSWORD_LABEL = "label:has-text('Password')"
    CONFIRM_PASSWORD_LABEL = "label:has-text('Re-Enter Password')"

    # -----------------------------
    # Actions
    # -----------------------------
    SIGNUP_BUTTON = "button[type='submit']:has-text('Sign Up')"  # More specific to avoid strict mode violation

    # -----------------------------
    # Error Messages (from JSON test cases)
    # -----------------------------
    PASSWORD_MISMATCH_ERROR = "text=Passwords do not match."
    PASSWORD_LENGTH_ERROR = "text=Password must be at least 8 characters long."
    PHONE_FORMAT_ERROR = "text=Please enter a valid phone number."

    # -----------------------------
    # Generic Elements
    # -----------------------------
    GENERIC_DIV = "div"
    ROOT_DIV = "#root"