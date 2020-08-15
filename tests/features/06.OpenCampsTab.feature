@smoke
@navigation

Feature: Open my camps page

  Scenario: Open camps
    Given User is logged in
    When User clicks Camps button
    Then Camps page is opened
    And Camp signup button is displayed

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened