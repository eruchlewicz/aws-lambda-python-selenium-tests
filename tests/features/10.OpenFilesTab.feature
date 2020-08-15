@smoke
@navigation

Feature: Open files page

  Scenario: Open files
    Given User is logged in
    When User clicks Files button
    Then Files page is opened

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened