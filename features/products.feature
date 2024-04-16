Feature: The product service back-end
    As a Product Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | category | available | description    | price   | image_url
        | X          | X        | True      | X              | X       | X
        | X          | X        | True      | X              | X       | X
        | X          | X        | False     | X              | X       | X
        | X          | X        | True      | X              | X       | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "iPhone"
    And I set the "Category" to "Electronics"
    And I select "False" in the "Available" dropdown
    And I select "Apple iPhone 13" in the "Description" dropdown
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
    And I should see "iPhone" in the "Name" field
    And I should see "Electronics" in the "Category" field
    And I should see "False" in the "Available" dropdown
    And I should see "Apple iPhone 13" in the "Description" dropdown
    And I should see "100" in the "Price" field

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iPhone" in the results
    And I should see "Camera" in the results
    And I should not see "Watch" in the results

Scenario: Search for electronics
    When I visit the "Home Page"
    And I set the "Category" to "Electronics"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iPhone" in the results
    And I should not see "Camera" in the results
    And I should not see "Watch" in the results

Scenario: Search for available
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iPhone" in the results
    And I should see "Camera" in the results
    And I should see "Watch" in the results
    And I should not see "Blanket" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "iPhone"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iPhone" in the "Name" field
    And I should see "Electronics" in the "Category" field
    When I change "Name" to "Camera"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Camera" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Camera" in the results
    And I should not see "iPhone" in the results