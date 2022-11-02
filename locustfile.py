import time
import json
from locust import FastHttpUser, HttpUser, task, between, constant_throughput
import string
import random
from datetime import datetime

class RegisteredUser(HttpUser):
    weight = 1
    #wait_time = constant_throughput(5)

    @task(4)
    def index(self):
        self.client.get('/index')

    @task(1)
    def newPost(self):
        self.client.post('/index', data=({'body': "Yo, {} digo HOLA a las {}".format(self.username, datetime.now())}))

    def on_start(self):
        u = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        p = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
        self.client.post('/auth/register', data={"username": u, "password": p, "password2": p})
        self.username = u
        

        response = self.client.post('/auth/login', data={"username": u, "password": p})
        #self.token = response.cookies['session']

class AnnonUser(HttpUser):
    weight = 5

    @task(4)
    def index(self):
        self.client.get('/index')