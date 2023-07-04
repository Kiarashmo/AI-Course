import numpy as np
import tensorflow as tf
import copy
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))

def fitness_function(position):
    model.set_weights(position)
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=128, epochs=5, verbose=0)
    y_pred = model.predict(x_test)
    y_pred = np.argmax(y_pred, axis=1)
    y_true = np.argmax(y_test, axis=1)
    accuracy = accuracy_score(y_true, y_pred)
    return -accuracy

class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = [np.zeros_like(p) for p in position]
        self.best_position = copy.deepcopy(self.position)
        self.best_fitness = fitness_function(self.position)

    def update_velocity(self, global_best_position, w, c1, c2):
        r1 = [np.random.random(p.shape) for p in self.position]
        r2 = [np.random.random(p.shape) for p in self.position]
        self.velocity = [w * v + c1 * r1i * (p_best - p) + c2 * r2i * (g_best - p)
                         for v, r1i, r2i, p_best, g_best, p in zip(self.velocity, r1, r2, self.best_position, global_best_position, self.position)]

    def update_position(self):
        self.position = [p + v for p, v in zip(self.position, self.velocity)]
        fitness = fitness_function(self.position)
        if fitness < self.best_fitness:
            self.best_position = copy.deepcopy(self.position)
            self.best_fitness = fitness

def mpso_optimization(num_particles, num_iterations, w, c1, c2):
    global_best_position = None
    global_best_fitness = -np.inf
    particles = []

    for _ in range(num_particles):
        position = [layer + np.random.uniform(low=-1, high=1, size=layer.shape) for layer in model.get_weights()]
        particle = Particle(position)
        particles.append(particle)

        if particle.best_fitness > global_best_fitness:
            global_best_position = [np.copy(pos) for pos in particle.best_position]
            global_best_fitness = particle.best_fitness

    for _ in range(num_iterations):
        for particle in particles:
            particle.update_velocity(global_best_position, w, c1, c2)
            particle.update_position()

            if particle.best_fitness > global_best_fitness:
                global_best_position = [np.copy(pos) for pos in particle.best_position]
                global_best_fitness = particle.best_fitness

    return global_best_position

num_particles = 10
num_iterations = 20
w = 0.5
c1 = 1
c2 = 2

best_weights = mpso_optimization(num_particles, num_iterations, w, c1, c2)

model.set_weights(best_weights)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy) 