# ZendeskChallenge


## Installation

First, make sure to pip install the requests library using the command
`python -m pip install requests`

Then, download `challenge.py` to run the program


## Usage

First, make an account as a customer at www.zccdarrenl.zendesk.com/. Then, you should be able to make tickets using your account. From there, you will be able to use the program to read all of the tickets that are accessible for your account.

Now that you have an account, simply run the progam and input your email into the program. After passing authentication, you will be prompted to choose how to view the tickets.

### Viewing Options

You can view your tickets through 2 different formats: view a single ticket or view all tickets.

#### Viewing a single ticket

Simply input the ticket id and the program should show the ticket you chose. It will show the status, url, requester id, assignee id, and subject of the ticket. However, if you inputted an id that could not be found, is not accessible with your account, or is an invalid input, the program will explain the issue and prompt you to try again.


#### Viewing all tickets

This viewing option shows 25 tickets at a time, starting from the very first 25 tickets. You will able to toggle showing the next 25 tickets or the previous 25 tickets. If you attempt to make the page number out of bounds, the program will handle this issue and explain this is not a valid operation.

Each ticket shown has less details than using the single ticket viewing option. In this case, it only shows the status and subject of the ticket. To see the ticket in more detail, please use the single ticket viewing option.


## Testing

To test this program, download the `test_viewer.py` file and run the program. Because the original program depends on outputting to the terminal, it was harder to properly use unit testing to test all the functions. Therefore, the testing program asks the user to check the print statements and ensure it matches the printed solution. 




## Implementation Details

To get a single ticket, I simply used the API request `/api/v2/requests/id` to retrieve information about a particular ticket.

To get all tickets, I used the API request `/api/v2/requests/` to retrieve the current 100 tickets. If the page is toggled to exceed the 100 ticket range, the `next_page` or `previous_page` field was used to retrieve the next or previous 100 tickets. Although this implementation is not efficient when the user toggles back and forth between 2 different pages, this is an unlikely circumstance. Although saving all of the different pages of 100 tickets would save on immediate runtime efficiency, this would significantly take up memory. Therefore, I chose this implementation.






