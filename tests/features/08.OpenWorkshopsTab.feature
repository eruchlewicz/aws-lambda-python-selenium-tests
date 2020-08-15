@smoke
@navigation

Feature: Open my workshops page

  Scenario: Open workshops
    Given User is logged in
    When User clicks Workshops button
    Then Workshops page is opened
    And Workshop signup button is displayed

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened