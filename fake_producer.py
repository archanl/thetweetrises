from flask import Flask
import random

app = Flask(__name__)

lats = [i/100.0 for i in range(0, 9001)]
longs = [i/100.0 for i in range(-18000, 18001)]

def randCoord():
    return (random.choice(lats), random.choice(longs))

@app.route('/')
def main():
    return randCoord()


if __name__ == "__main__":
    app.run()
