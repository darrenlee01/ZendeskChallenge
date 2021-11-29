import requests
import base64


# The amount of data you display in the ticket list view and the single ticket view is up to you
# How you format and display the ticket data is up to you, just ensure it is easy to read
# The Ticket Viewer should handle the API being unavailable
# We need to see you write some unit tests for your application in a standard unit testing framework for your language of choice

# defend your design choice in your REAMDE and comments

# The challenge document says that meaningful comments will be looked upon favorably


# takes in the url to send a get request to
# takes in an access_token which is assumed to be a valid base64 encoded
#   authorization string
#
# returns a json dictionary containing all of the relevant ticket information
#    pertaining to the user from the access_token
def getTicketsPage(url, access_token):
    print(url)

    getTickets = requests.get(url,
                            headers={'Content-Type':'application/json',
                              'Authorization': 'Basic {}'.format(access_token)})

    if (not (200 <= getTickets.status_code < 300)):  #if not successful request
        print("Oh no! Issue with getting tickets")
        print("Reason:", getTickets.reason)
        return None

    getTickets = getTickets.json()

    return getTickets

# prints the page given the number of tickets to put on the page
# takes in allTicketsList which is the list of tickest to print from
# takes in a currPage which specifies the page range to print from the list
def printPage(allTicketsList, numTicketsPerPage, currPage):
    indent = "\t"
    startIndex = (currPage - 1) * numTicketsPerPage

    endIndex = min(len(allTicketsList), startIndex + numTicketsPerPage)


    print("\n\n")
    print("---------------------------------------------------------", end = "")
    print("--------------------------\n\n")


    for eachTicket in range(startIndex, endIndex):
        ticketInfo = allTicketsList[eachTicket]

        id = ticketInfo["id"]
        

        print(indent, "Ticket", id, "(" + ticketInfo["status"] + ") :")
        print(indent, "Subject:", ticketInfo["subject"])

        print("\n")

    print("\n\n")
    print("---------------------------------------------------------", end = "")
    print("--------------------------\n\n")

    print(indent, "Press enter when finished viewing page")
    input()

# displays all of the tickets by increments of 25 tickets
# allows user to toggle page number by going back or forth
# takes in allTickets which is the json dictionary containing all relevant
#   ticket info from the user
# takes in a ticketNum which specifies the total number of tickets
# takes in an authorize which is assumed to be a valid base64 encoded
#   authorization string of the given user

def displayAll(allTickets, ticketNum, authorize):

    indent = "\t"
    if (ticketNum == 0):
        print("\n\n")
        print(indent, "No tickets to show")
        return

    numTicketsPerPage = 25

    # assumed about the request that there is exactly a max of 100 tickets
    pageNum = 4
    
    showTickets = True
    currPage = 1

    allTicketsList = allTickets["requests"]

    while (showTickets):
        printPage(allTicketsList, numTicketsPerPage, currPage)

        print("\n\n")
        print("----------------------------------------------------------\n\n")
        print(indent, "Flipping Page Menu\n")
        print(indent, "Press 'a' to go to the previous page")
        print(indent, "Press 'd' to go to the next page")
        print(indent, "Type 'home' to go back to main menu\n\n")
        print("----------------------------------------------------------\n\n")

        validInput = False

        while (not validInput):
            print("Input: ", end="")
            flipPage = input()

            if (flipPage == "a"):  # user wants to flip to previous

                if (currPage <= 1):  

                    # if no more previous tickets
                    if (allTickets["previous_page"] == None): 
                        print(indent, "Already at the first page\n")
                    else:  # there are more previous tickets
                        currPage = 4  # set currPage to be the last page
                        allTickets = getTicketsPage(allTickets["previous_page"],
                                                    authorize)

                        if (allTickets == None):
                            return

                        allTicketsList = allTickets["requests"]

                        validInput = True
                else:
                    currPage -= 1
                    validInput = True

            elif (flipPage == "d"):  #user wants to flip the page forward

                #finding max possible page number from given list
                maxPage = len(allTicketsList) // numTicketsPerPage  

                if (len(allTicketsList) % numTicketsPerPage != 0):
                    maxPage += 1

                maxPage = min(pageNum, maxPage)

                if (currPage >= maxPage):

                    #if no more tickets after current page
                    if (allTickets["next_page"] == None): 
                        print(indent, "Already at the last page\n")
                    else:  #if there exists more tickets after
                        currPage = 1
                        allTickets = getTicketsPage(allTickets["next_page"],
                                                    authorize)
                        if (allTickets == None):
                            return
                        allTicketsList = allTickets["requests"]
                        validInput = True
                    
                else:
                    currPage += 1
                    validInput = True

            elif (flipPage == "home"):
                return
            else:
                print(indent, "Invalid input:", repr(flipPage))
    
    

# attempts to display a single ticket where it prompts user to input ticket id
# takes in an access_token which is assumed to be a valid base64 encoded
#   authorization string
def displayOne(access_token):
    indent = "\t"

    validID = False

    id = 0

    requestTicket = None

    for eachTry in range(5):  #gives user 5 tries to input a valid id

        print(indent, 
            "Input the id of the ticket you would like to see in detail\n")
        print("Input: ", end="")

        id = input()
        if (not id.isdigit()):
            print(indent, "id must be a digit:", repr(id))
        else:

            url = "https://zccdarrenl.zendesk.com/api/v2/requests/" + id

            requestTicket = requests.get(url,
                            headers={'Content-Type':'application/json',
                              'Authorization': 'Basic {}'.format(access_token)})
            
            # successful
            if (200 <= requestTicket.status_code < 300):  
                validID = True

            # could not find token
            elif (requestTicket.reason == "Not Found"):
                print(indent, "Could not find id:", repr(id))
        
            # found, but not given permission
            elif (requestTicket.reason == "Forbidden"): 
                print(indent, "You do not have access to this ticket")

            # other issue
            else:
                print(indent, "Problem with getting ticket:", 
                                                        requestTicket.reason)
        
        if (validID):
            break
        else:
            print("Try again\n\n")

    if (not validID):
        print("Failed too many times. Try again later.")
        return

    ticketInfo = requestTicket.json()
    ticketInfo = ticketInfo["request"]

    print("\n\n")
    print("---------------------------------------------------------", end = "")
    print("--------------------------\n\n")

    print(indent, "Ticket", id, "(" + ticketInfo["status"] + ")",  ":\n")
    print(indent, "URL:", ticketInfo["url"])
    print(indent, "Requester:", ticketInfo["requester_id"])
    print(indent, "Assignee:", ticketInfo["assignee_id"])
    print(indent, "Subject:", ticketInfo["subject"])

    print("\n")
    print(ticketInfo["description"])

    print("\n\n")

    print("---------------------------------------------------------", end = "")
    print("------------------------\n\n")

    print(indent, "press enter to go back to the main menu")
    input()

# authenticates user by trying to get from specified url
# returns None if could not authenticate after 3 tries
# returns (authenticate, requestTickets)
#       where authenticate is the base64 encoded authentication string
#       where requestTickets is the json dictionary containing all of the 
#           relevant ticket information pertaining to the user
def authenticate(url):


    print("First, input email address to view the tickets\n")



    for eachTry in range(3):  #gives user 3 tries

        print("Username: ", end="")
        username = input()


        # authorize user through base64 encoding
        authorize = (username + 
                            "/token:D4tuG0rAUZtM7Krc2mCO7GOHQ8zxQlTg1QlpWIRs")

        bytes = base64.b64encode(authorize.encode('ascii'))

        access_token = bytes.decode('ascii')

        requestTickets = requests.get(url,
                            headers={'Content-Type':'application/json',
                              'Authorization': 'Basic {}'.format(access_token)})

        

        if (200 <= requestTickets.status_code < 300):  # if request successful 
            print("\nAuthorized!\n")
            return (access_token, requestTickets.json())
        elif (requestTickets.reason == "Unauthorized"):  # if unauthorized
            print("\nCould not authenticate. Try again.\n")
        else:  # other issue with get request
            print("Oh no! Issue with getting tickets")
            print("Reason:", requestTickets.reason)
            return None
    
    print("Failed too many times. Try again later.")
    return None
        
        

def main():

    print("\n\nWelcome to the Ticket Viewer!")


    url = "https://zccdarrenl.zendesk.com/api/v2/requests/"

    result = authenticate(url)

    if (result == None):
        return

    (authorize, allTickets) = result

    ticketNum = allTickets["count"]

    if (ticketNum == 0):
        print("\n\nNo tickets to show!\n")
        return


    showTickets = True
    indent = "            "
    while (showTickets):
        print("\n\n")
        print("----------------------------------------------------------\n\n")
        print(indent, "Ticket Viewer Menu\n")
        print(indent, "Press 1 to show a single tickets")
        print(indent, "Press 2 to show all tickets")
        print(indent, "Type 'quit' to quit\n\n")
        print("----------------------------------------------------------\n")
        print("Input: ", end="")
        option = input()

        if (option == "1"):
            displayOne(authorize)
        elif (option == "2"):
            displayAll(allTickets, ticketNum, authorize)
        elif (option == "quit"):
            showTickets = False
        else:
            print()
            print(indent, "Invalid option:", repr(option))
        
    print("\nBye!")





if __name__ == "__main__":
    main()

    

