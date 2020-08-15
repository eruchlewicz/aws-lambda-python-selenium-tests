@smoke
@navigation

Feature: Open my retreats page

  Scenario: Open retreats
    Given User is logged in
    When User clicks Retreats button
    Then Retreats page is opened
    And Retreat signup button is displayed

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened