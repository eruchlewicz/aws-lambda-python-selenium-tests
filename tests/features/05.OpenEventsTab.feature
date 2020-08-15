@smoke
@navigation

Feature: Open my events page

  Scenario: Open events
    Given User is logged in
    When User clicks Events button
    Then Events page is opened
    And Event signup button is displayed

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened