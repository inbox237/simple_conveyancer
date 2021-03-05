from locust import HttpUser, task, between
from faker import Faker
import uuid
import random
import time

class QuickstartUser(HttpUser):
    wait_time = between(1,4)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.artists = []
        self.faker = Faker()
        self.token = None
    
    def on_start(self):
        id = str(uuid.uuid4())
        while self.token == None:
            try:
                self.client.post(
                    "/auth/register", 
                    json={"email": f"test{id}@test.com", "password":"secret"}
                )
                response = self.client.post(
                    "/auth/login", 
                    json={"email": f"test{id}@test.com", "password":"secret"}
                )
                self.token = response.json()["token"]
            except:
                time.sleep(3)
    
    @task
    def index_page(self):
        self.client.get("/artists/")
    
    @task(3)
    def create_artist(self):
        if self.token:
            response = self.client.post(
                "/artists/",
                json={ "title": self.faker.catch_phrase() },
                headers={ "Authorization": f"Bearer {self.token}"}
            )
            if response.status_code < 400:
                self.artists.append(response.json()["id"])
    
    @task(2)
    def update_artist(self):
        if len(self.artists) > 0 and self.token:
            artist_id = random.choice(self.artists)
            self.client.put(
                f"/artists/{artist_id}", 
                json={ "title": self.faker.catch_phrase() },
                headers={ "Authorization": f"Bearer {self.token}"}
            )
    
    @task(2)
    def delete_artist(self):
        if len(self.artists) > 0 and self.token:
            artist_id = random.choice(self.artists)
            response = self.client.delete(
                f"/artists/{artist_id}",
                headers={ "Authorization": f"Bearer {self.token}"}
            )
            if response.status_code < 400:
                self.artists.remove(artist_id)