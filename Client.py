# bark Client class
class Client:
    def __init__(self, firstname, data_received, zip, datails, state):
        self.firstname = firstname
        self.data_received = data_received
        self.zip = zip
        self.details = datails
        self.state = state
        self.map = ""
        self.email = ""
        self.details = ""
        self.credits = 0
        self.area_code = 0
        self.phone = ""
        self.responded_professional_number = 0
        self.lastname = ""
        self.attachments = []
        self.online = False

    def get_info(self):
        return self.firstname

    def setMap(self, mapImage):
        self.map = mapImage

    def setAttachments(self, attachment):
        self.attachments.append(attachment)
