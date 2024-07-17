from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
import pygame

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Python Game')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen
        pygame.display.flip()
        time.sleep(0.016)  # Frame rate

        # Emit game state to clients
        socketio.emit('game_update', {'data': 'Game state data'})

    pygame.quit()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    game_thread = threading.Thread(target=game_loop)
    game_thread.start()
    socketio.run(app)
