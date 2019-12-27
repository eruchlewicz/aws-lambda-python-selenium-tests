@smoke
@login

Feature: Login to DJ

  Scenario: Open login page
     Given Home page is opened
     When User opens Login page
     Then Login page is opened

  Scenario: Login
     When User enters credentials
     And User clicks Login button
     Then User is logged in