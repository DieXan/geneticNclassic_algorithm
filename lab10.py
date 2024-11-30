import time
import random
import string

# Функция для загрузки паролей из файла
def load_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Полный перебор
def brute_force(passwords, target_password):
    start_time = time.time()
    for password in passwords:
        if password == target_password:
            end_time = time.time()
            return password, end_time - start_time
    end_time = time.time()
    return None, end_time - start_time

# Генетический алгоритм
def genetic_algorithm(passwords, target_password, pop_size=9999, generations=999999, mutation_rate=0.01):
    def fitness(password):
        return sum(1 for a, b in zip(password, target_password) if a == b)

    def mutate(password, mutation_rate):
        password = list(password)
        for i in range(len(password)):
            if random.random() < mutation_rate:
                password[i] = random.choice(string.ascii_letters + string.digits + string.punctuation)
        return ''.join(password)

    def crossover(parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    population = [random.choice(passwords) for _ in range(pop_size)]
    start_time = time.time()
    for generation in range(generations):
        fitness_scores = [fitness(password) for password in population]
        if max(fitness_scores) == len(target_password):
            end_time = time.time()
            return population[fitness_scores.index(max(fitness_scores))], end_time - start_time
        population = sorted(population, key=fitness, reverse=True)[:pop_size // 2]
        new_population = population[:]
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
        population = new_population
    end_time = time.time()
    return None, end_time - start_time

def main():
    file_path = 'passwords.txt'  # Путь к файлу с паролями
    target_password = 'zoosporiferous'  # Эталонный пароль

    passwords = load_passwords(file_path)

    # Генетический алгоритм
    genetic_password, genetic_time = genetic_algorithm(passwords, target_password)
    print(f"Генетический  алгоритм: Найденный пароль = {genetic_password}, Время = {genetic_time} сек.")

    # Полный перебор
    brute_force_password, brute_force_time = brute_force(passwords, target_password)
    print(f"БрутФорс: Найденный пароль = {brute_force_password}, Время = {brute_force_time} сек.")

if __name__ == "__main__":
    main()