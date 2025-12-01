Feature: Google Chrome New Tab Page Functionality
  As a user of Google Chrome
  I want the "New Tab" page to be functional, reliable, and secure
  So I can have a seamless browsing experience

Background:
  Given a new tab is open in the Chrome browser

@browser-window @tab-management @happy-path
Scenario: Open a new tab
  When I click the "new tab" button
  Then a new active tab should be opened

@browser-window @tab-management @happy-path
Scenario: Close an inactive tab
  Given I have multiple tabs open
  When I click the close button on an inactive tab
  Then that specific tab should be closed

@browser-window @window-management @happy-path
Scenario: Close the only tab in the window
  Given I have only one tab open in the window
  When I click the close button on the active tab
  Then the Chrome window should be closed

@browser-window @window-management
Scenario Outline: Use window management controls
  When I click the "<button_name>" button
  Then the browser window should be "<expected_state>"

  Examples:
    | button_name | expected_state |
    | Close       | closed         |
    | Minimize    | minimized      |
    | Maximize    | full-screen    |

@browser-window @tab-management @edge-case
Scenario: Rapidly open many tabs
  When I rapidly click the "new tab" button 20 times
  Then the UI should remain responsive
  And the tab titles should shrink to fit

@navigation @happy-path
Scenario: Navigation controls state on a fresh new tab
  Then the "Back" navigation button should be disabled
  And the "Forward" navigation button should be disabled

@navigation @address-bar
Scenario Outline: Using the address bar for navigation and search
  When I type "<input_text>" into the address bar and press Enter
  Then I should be navigated to the "<expected_destination>" page

  Examples:
    | input_text         | expected_destination   |
    | www.google.com     | Google homepage        |
    | QA test strategy   | Google search results  |
    | htp://test         | Google search results  |
    | www. incomplete    | Google search results  |

@navigation @ui
Scenario Outline: Browser menu icons are functional
  When I click the "<icon_name>" icon
  Then the corresponding "<menu_name>" menu should open

  Examples:
    | icon_name       | menu_name             |
    | Extensions      | Extensions dropdown   |
    | Profile         | Profile dropdown      |
    | Three-dot menu  | Three-dot menu        |

@security @xss @address-bar
Scenario: Entering an XSS payload into the address bar
  When I enter "<script>alert('XSS')</script>" into the address bar and press Enter
  Then a search for the script text should be performed
  And no script alert should be executed

@main-content @search @happy-path
Scenario: Searching from the main content search bar
  When I type "Cucumber Gherkin" into the search field and press Enter
  Then I should be navigated to the Google search results page

@main-content @shortcuts @happy-path
Scenario: Clicking an existing shortcut
  When I click the "Google Drive" shortcut
  Then I should be navigated to the Google Drive website

@main-content @shortcuts @happy-path
Scenario: Adding a valid new shortcut
  When I click the "Add shortcut" button
  And I enter "My Test Site" in the name field
  And I enter "https://www.example.com" in the URL field
  And I click the "Done" button
  Then a new shortcut named "My Test Site" should appear on the page

@main-content @shortcuts @edge-case
Scenario Outline: Attempt to add a shortcut with invalid data
  Given I have the "Add shortcut" dialog open
  When I enter "<Name>" in the name field
  And I enter "<URL>" in the URL field
  And I attempt to save the shortcut
  Then the shortcut should not be created
  And an error message for the invalid "<field>" should be displayed

  Examples:
    | Name           | URL                     | field |
    |                | https://www.example.com | Name  |
    | My Test Site   |                         | URL   |
    | My Other Site  | not-a-valid-url         | URL   |

@security @xss @shortcuts
Scenario: Stored XSS in the shortcut name field
  Given I have the "Add shortcut" dialog open
  When I enter "<script>alert('XSS')</script>" in the name field
  And I enter "https://www.safe.com" in the URL field
  And I click the "Done" button
  Then the new shortcut is created
  When I view the shortcut on the new tab page
  Then the shortcut name should be displayed as plain text
  And no script alert should be executed

@security @xss @shortcuts
Scenario: Stored XSS in the shortcut URL field
  Given I have the "Add shortcut" dialog open
  When I enter "Malicious JS Link" in the name field
  And I enter "javascript:alert('XSS')" in the URL field
  And I click the "Done" button
  Then the new shortcut is created
  When I click the "Malicious JS Link" shortcut
  Then no client-side script should be executed

@security @sqli
Scenario Outline: Entering SQL Injection payloads into input fields
  When I enter the payload "' OR 1=1; --" into the <input_field>
  And I submit the action
  Then the application should handle the input as a literal string
  And the UI should not crash or display a server error

  Examples:
    | input_field         |
    | address bar         |
    | search bar          |
    | shortcut name field |
    | shortcut URL field  |

@customization @happy-path
Scenario: Open and use the Customise Chrome panel
  When I click the "Customise Chrome" button
  Then the customization side panel should open
  When I select a new background from the panel
  Then the new tab page background should update immediately

@customization @edge-case
Scenario: Customise panel state after page reload
  Given the customization side panel is open
  When I reload the new tab page
  Then the customization side panel should be closed