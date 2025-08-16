class Job:
    def __init__(self, title, company, location, date_posted, link, etat):
        self.title = title
        self.company = company
        self.location = location
        self.date_posted = date_posted
        self.link = link
        self.etat = etat
    def show(self):
        return f"Title: {self.title}, Company: {self.company}, Location: {self.location}, Date Posted: {self.date_posted}, Link: {self.link}, Etat: {self.etat}"
