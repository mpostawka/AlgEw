import numpy as np
from tqdm import tqdm
from car import basic_car, is_car_valid, code_to_car, car_to_code, random_car
from simulation import get_objective_func
from terrain import gen_terrain


def es(
    objective_function,
    chromosome_length,
    population_size,
    number_of_iterations,
    number_of_offspring,
    number_of_parents,
    sigma,
    tau,
    tau_0,
    log_frequency=1,
):

    best_solution = np.empty((1, chromosome_length))
    best_solution_objective_value = 0.00

    log_objective_values = np.empty((number_of_iterations, 4))
    log_best_solutions = np.empty((number_of_iterations, chromosome_length))
    log_best_sigmas = np.empty((number_of_iterations, chromosome_length))

    # generating an initial population
    current_population_solutions = sigma * np.random.rand(
        population_size, chromosome_length
    )
    for i in tqdm(range(population_size)):
        for j in range(10000):
            # code = 35.0 * (sigma * np.random.rand(1,chromosome_length) - sigma / 2.0)
            # car = code_to_car(code[0])
            car = random_car()
            if is_car_valid(car):
                print("The generated car is valid")
                break
        current_population_solutions[i] = car_to_code(car)
    current_population_sigmas = sigma * np.ones((population_size, chromosome_length))

    # evaluating the objective function on the current population
    current_population_objective_values = objective_function(
        current_population_solutions
    )

    for t in tqdm(range(number_of_iterations)):
        # regenerate terrain
        objective_function = get_objective_func(gen_terrain()[0])

        # selecting the parent indices by the roulette wheel method
        fitness_values = (
            current_population_objective_values
            - current_population_objective_values.min()
        )
        if fitness_values.sum() > 0:
            fitness_values = fitness_values / fitness_values.sum()
        else:
            fitness_values = 1.0 / population_size * np.ones(population_size)
        parent_indices = np.random.choice(
            population_size,
            (number_of_offspring, number_of_parents),
            True,
            fitness_values,
        ).astype(np.int64)

        # creating the children population by Global Intermediere Recombination
        children_population_solutions = np.zeros(
            (number_of_offspring, chromosome_length)
        )
        children_population_sigmas = np.zeros((number_of_offspring, chromosome_length))
        for i in range(number_of_offspring):
            children_population_solutions[i, :] = current_population_solutions[
                parent_indices[i, :], :
            ].mean(axis=0)
            children_population_sigmas[i, :] = current_population_sigmas[
                parent_indices[i, :], :
            ].mean(axis=0)

        # mutating the children population by adding random gaussian noise
        children_population_sigmas = children_population_sigmas * np.exp(
            tau * np.random.randn(number_of_offspring, chromosome_length)
            + tau_0 * np.random.randn(number_of_offspring, 1)
        )
        children_population_solutions = (
            children_population_solutions
            + children_population_sigmas
            * np.random.randn(number_of_offspring, chromosome_length)
            - children_population_sigmas / 2.0
        )

        # evaluating the objective function on the children population
        children_population_objective_values = objective_function(
            children_population_solutions
        )

        # replacing the current population by (Mu + Lambda) Replacement
        current_population_objective_values = np.hstack(
            [current_population_objective_values, children_population_objective_values]
        )
        current_population_solutions = np.vstack(
            [current_population_solutions, children_population_solutions]
        )
        current_population_sigmas = np.vstack(
            [current_population_sigmas, children_population_sigmas]
        )

        I = np.argsort(current_population_objective_values)[::-1]
        current_population_solutions = current_population_solutions[
            I[:population_size], :
        ]
        current_population_sigmas = current_population_sigmas[I[:population_size], :]
        current_population_objective_values = current_population_objective_values[
            I[:population_size]
        ]

        # recording some statistics
        if best_solution_objective_value < current_population_objective_values[0]:
            best_solution = current_population_solutions[0, :]
            best_solution_objective_value = current_population_objective_values[0]
        log_objective_values[t, :] = [
            current_population_objective_values.min(),
            current_population_objective_values.max(),
            current_population_objective_values.mean(),
            current_population_objective_values.std(),
        ]
        log_best_solutions[t, :] = current_population_solutions[0, :]
        log_best_sigmas[t, :] = current_population_sigmas[0, :]

        if np.mod(t, log_frequency) == 0:
            print(
                "Iteration %04d : best score = %0.8f, mean score = %0.8f."
                % (
                    t,
                    log_objective_values[: t + 1, 1].max(),
                    log_objective_values[t, 2],
                )
            )

    return (
        best_solution_objective_value,
        best_solution,
        log_objective_values,
        log_best_solutions,
        log_best_sigmas,
    )
