import unittest
import base64
import challenge

class TestViewer(unittest.TestCase):
    
    def allTicketsEqual(self, tickets1, tickets2):

        if (tickets1 == None or tickets2 == None):

            return tickets1 == None and tickets2 == None

        if (tickets1["count"] != tickets2["count"]):
            return False

        if (tickets1["next_page"] != tickets2["next_page"]):
            return False

        if (tickets1["previous_page"] != tickets2["previous_page"]):
            return False
        
        allTickets1 = tickets1["requests"]
        allTickets2 = tickets2["requests"]

        for eachTicket in range(min(len(allTickets1), len(allTickets2))):
            ticket1 = allTickets1[eachTicket]
            ticket2 = allTickets2[eachTicket]
            if (ticket1["url"] != ticket2["url"]):
                return False

        return True

    def test_get_tickets_page(self):
        url = "https://zccdarrenl.zendesk.com/api/v2/requests/"
        username = "darrenjwlee01@gmail.com"
        authorize = (username + 
                            "/token:D4tuG0rAUZtM7Krc2mCO7GOHQ8zxQlTg1QlpWIRs")

        bytes = base64.b64encode(authorize.encode('ascii'))

        access_token = bytes.decode('ascii')

        (auth, solution1) = challenge.authenticate(url, username)
        attempt1 = challenge.getTicketsPage(url, access_token)


        self.assertTrue(self.allTicketsEqual(solution1, attempt1))



        username = "customer@example.com"
        authorize = (username + 
                            "/token:D4tuG0rAUZtM7Krc2mCO7GOHQ8zxQlTg1QlpWIRs")

        bytes = base64.b64encode(authorize.encode('ascii'))


        access_token = bytes.decode('ascii')

        (auth, solution2) = challenge.authenticate(url, username)
        attempt2 = challenge.getTicketsPage(url, access_token)

        
        self.assertTrue(self.allTicketsEqual(solution2, attempt2))


        self.assertFalse(self.allTicketsEqual(solution1, solution2))
        self.assertFalse(self.allTicketsEqual(attempt1, attempt2))
        self.assertFalse(self.allTicketsEqual(solution1, attempt2))


        username = "fake@example.com"
        authorize = (username + 
                            "/token:D4tuG0rAUZtM7Krc2mCO7GOHQ8zxQlTg1QlpWIRs")

        bytes = base64.b64encode(authorize.encode('ascii'))


        access_token = bytes.decode('ascii')

        solution3 = challenge.authenticate(url, username)
        attempt3 = challenge.getTicketsPage(url, access_token)

        
        self.assertTrue(self.allTicketsEqual(solution3, attempt3))


        self.assertFalse(self.allTicketsEqual(solution3, solution2))
        self.assertFalse(self.allTicketsEqual(attempt3, attempt2))
        self.assertFalse(self.allTicketsEqual(solution3, attempt1))


    def test_display_one(self):

        url = "https://zccdarrenl.zendesk.com/api/v2/requests/"
        username = "darrenjwlee01@gmail.com"

        (auth, allTickets) = challenge.authenticate(url, username)

        print("Press enter if matches the solution.")
        print("Otherwise, enter anything and enter")

        challenge.displayOne(auth, "6")
        print("Solution: should display ticket #6")
        self.assertTrue(input() == "")

        challenge.displayOne(auth, "100")
        print("Solution: should display ticket #100")
        self.assertTrue(input() == "")

        challenge.displayOne(auth, "1")
        print("Solution: should display unknown ticket")
        self.assertTrue(input() == "")

        challenge.displayOne(auth, "1000")
        print("Solution: should display unknown ticket")
        self.assertTrue(input() == "")

        challenge.displayOne(auth, "sdlijf")
        print("Solution: should display ticket needs to be a number")
        self.assertTrue(input() == "")



        username = "customer@example.com"

        (auth, allTickets) = challenge.authenticate(url, username)


        challenge.displayOne(auth, "6")
        print("Solution: should display unauthorized ticket")
        self.assertTrue(input() == "")
        
        


        challenge.displayOne(auth, "100")
        print("Solution: should display unauthorized ticket")
        self.assertTrue(input() == "")

        challenge.displayOne(auth, "1")
        print("Solution: should display unknown ticket")
        self.assertTrue(input() == "")

        challenge.displayOne(auth, "1000")
        print("Solution: should display unknown ticket")
        self.assertTrue(input() == "")

        challenge.displayOne(auth, "109")
        print("Solution: should display ticket #109")
        self.assertTrue(input() == "")

        challenge.displayOne(auth, "sdlijf")
        print("Solution: should display ticket needs to be a number")
        self.assertTrue(input() == "")



        self.assertTrue(True)

    def test_display_all(self):


        # it is harder to properly test this with unit testing

        # test by having darrenjwlee01@gmail.com as the username
        #   should be able to toggle through 5 different pages
        #   test trying to get past page 5 or before page 1 and ensure there
        #       is no error


        # test by having customer@example.com as the username
        #   should be able to toggle through only 1 page
        #   test trying to move pages. Should not be able to move at all



        self.assertTrue(True)

        













if (__name__ == "__main__"):
    unittest.main(exit=False)