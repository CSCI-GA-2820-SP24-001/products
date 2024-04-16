Feature: The product service back-end
    As a Product Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name            | category    | available | description           | price   | 
        | Apple iPhone 13 | Smart Phones| True      | Used Apple iPhone 13  | 100     | 
        | Fujifilm Camera | Cameras     | True      | Used 1986 Fuji Camera | 85      | 
        | Garmin Watch    | Watches     | False     | New Garmin Smartwatch | 100     | 
        | Bose Headphones | Headphones  | True      | New Bose Headphones   | 120     | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Apple iPhone 13"
    And I set the "Category" to "Smart Phones"
    And I select "False" in the "Available" dropdown
    And I select "Used Apple iPhone 13" in the "Description" dropdown
    And I set the "Price" to "100"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Apple iPhone 13" in the "Name" field
    And I should see "Smart Phones" in the "Category" field
    And I should see "True" in the "Available" dropdown
    And I should see "Used Apple iPhone 13" in the "Description" dropdown
    And I should see "100" in the "Price" field

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Apple iPhone 13" in the results
    And I should see "Fujifilm Camera" in the results
    And I should not see "Garmin Watch" in the results

Scenario: Search for electronics
    When I visit the "Home Page"
    And I set the "Category" to "Smart Phones"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Apple iPhone 13" in the results
    And I should not see "Fujifilm Camera" in the results
    And I should not see "Garmin Watch" in the results

Scenario: Search for available
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Fujifilm Camera" in the results
    And I should see "Apple iPhone 13" in the results
    And I should not see "Garmin Watch" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "Apple iPhone 13"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Apple iPhone 13" in the "Name" field
    And I should see "Smart Phones" in the "Category" field
    When I change "Name" to "Apple iPhone 14"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Apple iPhone 14" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Apple iPhone 14" in the results
    And I should not see "Apple iPhone 13" in the results