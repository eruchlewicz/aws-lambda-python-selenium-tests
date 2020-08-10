@smoke
@account

Feature: Open account details page

  Scenario: Open account details
    Given User is logged in
    When User clicks Account button
    Then Account page is opened
    And User data is displayed

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened