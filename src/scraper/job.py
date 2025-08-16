class Job:
    def __init__(self, title, company, location, date_posted, link, etat):
        self.title = title
        self.company = company
        self.location = location
        self.date_posted = date_posted
        self.link = link
        self.etat = etat
    def show(self):
        return f"Title: {self.title} \
            \nCompany: {self.company}\
            \nLocation: {self.location} \
            \nDate Posted: {self.date_posted} \
            \nLink: {self.link} \
            \nEtat: {self.etat} \
            \n ================================="
    def save_to_db(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (title, company, location, date_posted, link, etat)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.title, self.company, self.location, self.date_posted, self.link, self.etat))
        conn.commit()
        print(f"Job '{self.title}' saved to database.")
