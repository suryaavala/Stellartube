# Class to store video data
class videoInfo():
    def __init__(self, video_id, owner_id, upload_date, title, 
            description, price, filename, thumbnail_location):
        self.id = video_id
        self.owner_id = owner_id
        self.upload_date = upload_date
        self.title = title
        self.description = description
        self.price = price
        self.filename = filename
        self.thumbnail_location = thumbnail_location
