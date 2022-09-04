class Mask:
    def __init__(self, nrows, ncols):
        self.nrows, self.ncols = nrows, ncols

    def apply(self, grid):
        """The default, no mask."""
        pass


class CircleMask(Mask):
    def apply(self, grid):
        """A circular mask to shape the grid."""
        r2 = min(self.ncols, self.nrows) ** 2 // 4
        cx, cy = self.ncols // 2, self.nrows // 2
        for irow in range(self.nrows):
            for icol in range(self.ncols):
                if (irow - cy) ** 2 + (icol - cx) ** 2 > r2:
                    grid[irow][icol] = "*"


class SquaresMask(Mask):
    def apply(self, grid):
        """A mask of overlapping squares to shape the grid."""
        a = int(0.38 * min(self.ncols, self.nrows))
        cy = self.nrows // 2
        cx = self.ncols // 2
        for irow in range(self.nrows):
            for icol in range(self.ncols):
                if a <= icol < self.ncols - a:
                    if irow < cy - a or irow > cy + a:
                        grid[irow][icol] = "*"
                if a <= irow < self.nrows - a:
                    if icol < cx - a or icol > cx + a:
                        grid[irow][icol] = "*"
