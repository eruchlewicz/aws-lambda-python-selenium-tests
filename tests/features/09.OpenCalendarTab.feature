@smoke
@navigation

Feature: Open calendar page

  Scenario: Open calendar
    Given User is logged in
    When User clicks Calendar button
    Then Calendar page is opened

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened