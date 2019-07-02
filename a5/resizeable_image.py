import imagematrix
import numpy

class ResizeableImage(imagematrix.ImageMatrix):
    # comparing two paths
    def min_compare2(self, path1, energy1, path2, energy2):
        min_energy = min(energy1, energy2)

        if energy1 == min_energy:
            min_path = path1
        else:
            min_path = path2

        return min_energy, min_path

    def min_compare3(self, path1, energy1, path2, energy2, path3, energy3):
        min_energy = min(energy1, energy2, energy3)

        if energy1 == min_energy:
            min_path = path1
        elif energy2 == min_energy:
            min_path = path2
        else:
            min_path = path3

        return min_energy, min_path

    # Depth First Search
    def dfs(self, energy, col, row):
        # Base Case
        if row == 0:
            return [(col, row)], self.energy(col, row)

        # First Col, 2 paths
        elif col == 0:
            path1, energy1 = self.dfs(energy, col + 1, row - 1)
            path2, energy2 = self.dfs(energy, col, row - 1)

            min_energy, min_path = self.min_compare2(path1, energy1, path2, energy2)

        # Last Col, 2 paths
        elif col == self.width - 1:
            path1, energy1 = self.dfs(energy, col, row - 1)
            path2, energy2 = self.dfs(energy, col - 1, row - 1)

            min_energy, min_path = self.min_compare2(path1, energy1, path2, energy2)
        # The in between, 3 paths
        else:
            path1, energy1 = self.dfs(energy, col - 1, row - 1)
            path2, energy2 = self.dfs(energy, col, row - 1)
            path3, energy3 = self.dfs(energy, col + 1, row - 1)

            min_energy, min_path = self.min_compare3(path1, energy1, path2, energy2, path3, energy3)

        min_energy += energy[col][row]

        min_path.append((col, row))

        return min_path, min_energy


    def best_seam(self, dp=True):
        # get the height and width

        height = self.height
        width = self.width
        # Naive Algorithm
        if not dp:
            energy = numpy.zeros(shape=(height, width), dtype = numpy.int32)

            # get the energy levels
            for i in range(height):
                for j in range(width):
                    energy[j][i] = self.energy(j, i)

            min_paths = []
            for i in range(width):
                min_paths.append(tuple(self.dfs(energy, i, height - 1)))

            min_energy = min_paths[0][1]

            for i in range(width):
                if min_paths[i][1] < min_energy:
                    min_energy = min_paths[i][1]
                    col = i

            final_path = min_paths[col][0]

        # Dynamic Programming
        else:
            energy = {}
            path = {}

            for i in range(width):
                energy[i, 0] = self.energy(i, 0)

            for i in range(1, height):
                for j in range(width):

                    pos = j, i - 1

                    if (j - 1, i - 1) in energy.keys() and energy[j - 1, i - 1] < energy[pos]:
                        p = j - 1, i - 1

                    if (i + 1, j - 1) in energy.keys() and energy[j + 1, i - 1] < energy[pos]:
                        p = j + 1, i - 1

                    energy[j, i] = self.energy(i, j) + energy[pos]

                    path[j, i] = pos

            min_energy = energy[0, height - 1]

            col = None

            for i in range(width):
                if energy[i, height - 1] < min_energy:
                    min = energy[i, height - 1]
                    col = 1

            final_path = []
            current = col, height - 1
            while current in path.keys():
                current = path[current]
                final_path.append(current)

        return final_path

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
