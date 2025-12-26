class WelcomeLocators:
    """Locators for welcome-to-snappod-ai page (authenticated page only)"""
    
    # Navigation elements
    SNAPPOD_LOGO = "[alt='SnapPod Logo']"
    POD_GALLERY_BUTTON = "button:has-text('Pod Gallery')"
    UPGRADE_BUTTON = "button:has-text('Upgrade')"
    USER_PROFILE_TJ = "div:has-text('TJ')"
    
    # Form inputs - React Select components (need click-to-open pattern)
    PODCAST_TOPIC_INPUT = "#rc_select_0 .react-select__control"  # React Select control
    PODCAST_TOPIC_DROPDOWN = "#rc_select_0 .react-select__menu"  # Dropdown menu
    LANGUAGE_INPUT = "#react-select-2 .react-select__control"  # React Select control
    LANGUAGE_DROPDOWN = "#react-select-2 .react-select__menu"  # Dropdown menu
    NUM_SPEAKERS_INPUT = "#react-select-3 .react-select__control"  # React Select control
    NUM_SPEAKERS_DROPDOWN = "#react-select-3 .react-select__menu"  # Dropdown menu
    CATEGORY_INPUT = "#react-select-4 .react-select__control"  # React Select control
    CATEGORY_DROPDOWN = "#react-select-4 .react-select__menu"  # Dropdown menu
    DURATION_INPUT = "#react-select-5 .react-select__control"  # React Select control
    DURATION_DROPDOWN = "#react-select-5 .react-select__menu"  # Dropdown menu
    TONE_INPUT = "#react-select-6 .react-select__control"  # React Select control
    TONE_DROPDOWN = "#react-select-6 .react-select__menu"  # Dropdown menu
    # Regular text inputs
    HOST_NAME_INPUT = "[name='host']"
    GUEST_NAME_INPUT = "[name='guest']"
    
    # Dropdown options
    ENGLISH_INDIAN_OPTION = "span:has-text('English (Indian)')"
    SPEAKERS_2_OPTION = "span:has-text('2')"
    BUSINESS_OPTION = "span:has-text('Business')"
    DURATION_2_5_4_OPTION = "span:has-text('2.5 - 4 Minutes')"
    FORMAL_OPTION = "span:has-text('Formal')"
    
    # AI Knowledge section
    AI_KNOWLEDGE_TOGGLE = "[role='switch']"
    SELECT_ARTIFACT_BUTTON = "button:has-text('Select Artifact')"
    
    # Action buttons
    GENERATE_SCRIPT_BUTTON = "button:has-text('GENERATE SCRIPT')"
    
    # Podcast gallery
    ALL_TAB = "div:has-text('All')"
    PODCAST_READY_ITEM = "article:has-text('Podcast Ready\\nStories of the G')"
    SCRIPT_READY_ITEM = "article:has-text('Script Ready\\nMaking Sense of t')"
    SCRIPT_FAILED_ITEM = "article:has-text('Script Failed\\nThe 5 AM Club Fa')"
    
    # Labels and indicators
    REQUIRED_INDICATOR = "span:has-text('*')"
    LANGUAGE_LABEL = "span:has-text('Language:')"
    NUM_SPEAKERS_LABEL = "span:has-text('No.of Speakers:')"
    CATEGORY_LABEL = "span:has-text('Category:')"
    DURATION_LABEL = "span:has-text('Duration:')"
    TONE_LABEL = "span:has-text('Tone:')"