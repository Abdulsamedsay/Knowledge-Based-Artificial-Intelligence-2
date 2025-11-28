from circuitplotter import plot_circuit
from guesscomponentsgame import choose_components, score_function
from conflictsets import ConflictSetRetriever
from hittingsets import run_hitting_set_algorithm
from os.path import join
from hittingsets import assert_minimality


if __name__ == '__main__':

    document = "circuit1.txt"

    game = False

    # It only makes sense to play the game if you have the hitting set algorithm implemented.
    if game:
        # If you play the game, choose conflict sets, compute hitting sets:
        plot_circuit(document)
        chosen_conflict_sets = choose_components()
        print("Your chosen conflict sets:", chosen_conflict_sets)

        # run_hitting_set_algorithm now returns: (minimal_diagnoses, nodes_expanded, runtime)
        chosen_minimal_hitting_sets, nodes_expanded_game, runtime_game = run_hitting_set_algorithm(
            chosen_conflict_sets
        )

        print("Your minimal hitting sets:", chosen_minimal_hitting_sets)
        print(f"Nodes expanded (game): {nodes_expanded_game}, runtime: {runtime_game:.6f} s\n")

    # Collect conflict sets:
    csr = ConflictSetRetriever(join("circuits", document))
    conflict_sets = csr.retrieve_conflict_sets()
    print("Actual conflict sets:", conflict_sets)

    # Collect minimal hitting sets:
    if len(conflict_sets) == 0:
        print("This circuit works correctly, there are no faulty components!")
    else:
        # Again, 3 return values: minimal_diagnoses, nodes_expanded, runtime
        minimal_hitting_sets, nodes_expanded, runtime = run_hitting_set_algorithm(conflict_sets)

        print("Minimal hitting sets:", minimal_hitting_sets)
        print(f"Nodes expanded: {nodes_expanded}, runtime: {runtime:.6f} s\n")

    # Give score on similarity between the two sets:
    if game:
        score = score_function(conflict_sets, chosen_conflict_sets)
        print(f"Your score: {score:.2f}%")
