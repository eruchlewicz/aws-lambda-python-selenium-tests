@smoke
@password

Feature: Change password

  Scenario: Check change password button
    Given User is logged in
    And User clicks Account button
    Then Change password button is displayed

  Scenario: Open change password page
    When User clicks Change Password button
    Then Change password page is opened

  Scenario: Change password to the new one
    When User enters current password 'test_password_123'
    And User enters new password twice 'test_password_1234'
    And User clicks Change Password button
    Then Account page is opened

  Scenario: Revert changes
    When User clicks Change Password button
    And User enters current password 'test_password_1234'
    And User enters new password twice 'test_password_123'
    And User clicks Change Password button
    Then Account page is opened

  Scenario: Logout
    When User clicks Logout button
    Then Home page is opened