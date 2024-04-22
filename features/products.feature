Feature: The product service back-end
    As a Product Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        |  name      | category | available | description    | price   | image_url                 | like|
        | iPhone     | Phones   | True      | Used iPhone    | 100     | https://shorturl.at/oNQV6 | 0   |
        | Camera     | Cameras  | True      | Used Camera    | 85      | https://shorturl.at/pqxBW | 0   | 
        | Watch      | Watches  | False     | New Watch      | 100     | https://shorturl.at/jrwDO | 0   |
        | Headphones | Misc     | True      | New Headphones | 120     | https://shorturl.at/oFKYZ | 0   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "iPhone"
    And I set the "Category" to "Phones"
    And I select "True" in the "Available" dropdown
    And I set the "Description" to "Used iPhone"
    And I set the "Price" to "100"
    And I set the "Image_URL" to "https://shorturl.at/oNQV6"
    And I set the "Like" to "0"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "iPhone" in the "Name" field
    And I should see "Phones" in the "Category" field
    And I should see "True" in the "Available" dropdown
    And I should see "Used iPhone" in the "Description" field
    And I should see "100" in the "Price" field
    And I should see "https://shorturl.at/oNQV6" in the "Image_URL" field
    And I should see "0" in the "Like" field