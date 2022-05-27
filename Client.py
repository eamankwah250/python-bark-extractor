# bark Client class
class Client:
    def __init__(self, firstname, data_received, job_type, state, zip, datails):
        self.firstname = firstname
        self.data_received = data_received
        self.job_type = job_type
        self.state = state
        self.zip = zip
        self.details = datails
        self.map = ""
        self.email = ""
        self.details = ""
        self.credits = 0
        self.area_code = 0
        self.phone = ""
        self.responded_professional_number = 0
        self.attachments = []
        self.online = False

    def get_info(self):
        return self.firstname

    def setMap(self, mapImage):
        self.map = mapImage

    def setAttachments(self, attachment):
        self.attachments.append(attachment)
