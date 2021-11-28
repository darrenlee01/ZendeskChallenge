import requests
from getpass import getpass


# The amount of data you display in the ticket list view and the single ticket view is up to you
# How you format and display the ticket data is up to you, just ensure it is easy to read
# The Ticket Viewer should handle the API being unavailable
# We need to see you write some unit tests for your application in a standard unit testing framework for your language of choice

# defend your design choice in your REAMDE and comments

# The challenge document says that meaningful comments will be looked upon favorably

# maybe cache?

def authenticate():
    url = "https://zccdarrenl.zendesk.com/api/v2/tickets/"


    print("First, login to view the tickets\n")

    for eachTry in range(3):

        print("Username: ", end="")
        username = input()
        pword = getpass()
        requestTickets = requests.get(url, auth=(username, pword))

        if (200 <= requestTickets.status_code < 300):
            print("\nAuthorized!\n")
            return requestTickets
        elif (requestTickets.reason == "Unauthorized"):
            print("\nCould not authenticate. Try again.\n")
        else:
            print("Issue with getting tickets")
            print("Reason:", requestTickets.reason)
            return None
    
    print("Failed too many times. Try again later.")
    return None

def printPage(allTicketsList, numTicketsPerPage, currPage, pageNum):
    indent = "\t"
    startIndex = (currPage - 1) * numTicketsPerPage

    endIndex = min(len(allTicketsList), startIndex + numTicketsPerPage)

    print()
    print(indent, "Page", str(currPage) + "/" + str(pageNum) )

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

def displayAll(allTicketsList, ticketNum):
    indent = "\t"
    if (ticketNum == 0):
        print("\n\n")
        print(indent, "No tickets to show")
        return

    numTicketsPerPage = 25

    pageNum = ticketNum // numTicketsPerPage
    if (ticketNum % numTicketsPerPage != 0):
        pageNum += 1
    
    showTickets = True
    currPage = 1

    while (showTickets):
        printPage(allTicketsList, numTicketsPerPage, currPage, pageNum)

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

            if (flipPage == "a"):
                if (currPage <= 1):
                    print(indent, "Already at the 1st page\n")
                else:
                    currPage -= 1
                    validInput = True
            elif (flipPage == "d"):
                if (currPage >= pageNum):
                    print(indent, "Already at the last page\n")
                else:
                    currPage += 1
                    validInput = True
            elif (flipPage == "home"):
                return
            else:
                print(indent, "Invalid input:", repr(flipPage))
    
    


def displayOne(allTickets):
    indent = "\t"

    validID = False

    id = 0

    for eachTry in range(5):

        print(indent, 
            "Input the id of the ticket you would like to see in detail\n")
        print("Input: ", end="")

        id = input()
        if (not id.isdigit()):
            print(indent, "id must be a digit:", repr(id))
        else:
            id = int(id)
            if (id in allTickets):
                validID = True
            else:
                print(indent, "Could not find id:", repr(id))
        
        if (validID):
            break
        else:
            print("Try again\n\n")

    if (not validID):
        print("Failed too many times. Try again later.")
        return

    ticketInfo = allTickets[id]

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

    
            
        
        

# Connect to the Zendesk API
# Request all the tickets for your account
# Display them in a list
# Display individual ticket details
# Page through tickets when more than 25 are returned

def main():

    print("Welcome to the Ticket Viewer!")

    getTickets = authenticate()

    if (getTickets == None):
        return


    getTickets = getTickets.json()
    allTicketsList = getTickets["tickets"]
    ticketNum = getTickets["count"]


    allTickets = {}

    for eachTicket in allTicketsList:
        newID = eachTicket["id"]
        allTickets[newID] = eachTicket  # aliasing, so no additional memory


    showTickets = True
    indent = "            "
    while (showTickets):
        print("\n\n")
        print("----------------------------------------------------------\n\n")
        print(indent, "Ticket Viewer Menu\n")
        print(indent, "Press 1 to show a single tickets")
        print(indent, "Press 2 to show all tickets")
        print(indent, "Type 'quit' to quit")
        print("\n\n----------------------------------------------------------\n")
        print("Input: ", end="")
        option = input()

        if (option == "1"):
            displayOne(allTickets)
        elif (option == "2"):
            displayAll(allTicketsList, ticketNum)
        elif (option == "quit"):
            showTickets = False
        else:
            print()
            print(indent, "Invalid option:", repr(option))
        
    print("\nBye!")





if __name__ == "__main__":
    main()

    

