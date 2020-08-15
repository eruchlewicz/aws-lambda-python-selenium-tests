@smoke
@login

Feature: Login to DJ

  Scenario: Login
    Given Home page is opened
    And User opens Login page
    When User enters credentials
    And User clicks Login button
    Then Camps page is opened

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened