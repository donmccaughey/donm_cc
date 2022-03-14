use std::fmt::{Display, Formatter, LowerHex, Write};
use std::time::{SystemTime, UNIX_EPOCH};
use getrandom::getrandom;
use oorandom::Rand32;


pub fn generate_maze(width: i16, height: i16) -> String {
    let mut maze = Maze::new(width, height);
    maze.generate();
    let ascii = Ascii::new(&maze);
    ascii.to_string()
}


#[derive(Copy, Clone, Debug)]
struct Seed {
    value: u64,
}


impl Seed {
    fn new() -> Self {
        let mut seed_bytes = [0u8; 8];
        let value: u64;
        if let Ok(_) = getrandom(&mut seed_bytes) {
            value = u64::from_le_bytes(seed_bytes);
        } else if let Ok(unix_timestamp) = SystemTime::now().duration_since(UNIX_EPOCH) {
            value = unix_timestamp.as_micros() as u64;
        } else {
            value = 8015536314858786381;
        };
        Seed { value }
    }
}


impl Display for Seed {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.value)
    }
}


struct Randomizer {
    seed: Seed,
    rand32: Rand32,
}


impl Randomizer {
    fn new() -> Self {
        let seed = Seed::new();
        let rand32 = Rand32::new(seed.value);
        Randomizer { seed, rand32 }
    }

    fn choose_one<E: Copy>(&mut self, vector: Vec<E>) -> E {
        let count = vector.len() as u32;
        let i = self.rand32.rand_range(0..count) as usize;
        vector[i]
    }
}


#[derive(Copy, Clone, Debug)]
enum CellStatus {
    Empty, Visited,
}


/// An `Element` represents a wall or open space in the maze map.  Walls can be
/// horizontal, vertical or the intersection of horizontal and vertical walls.
///
///      01234
///    0 +-+-+
///    1 | | |
///    2 +-+-+
///
#[derive(Copy, Clone, Debug)]
enum ElementType {
    Cell { status: CellStatus },
    HorizontalOpening,
    VerticalOpening,
    HorizontalWall,
    VerticalWall,
    Intersection,
}


impl ElementType {
    fn is_boundary(&self) -> bool {
        matches!(self,
            Self::HorizontalWall | Self::VerticalWall
            | Self::HorizontalOpening | Self::VerticalOpening
        )
    }

    fn is_cell(&self) -> bool {
        matches!(self, Self::Cell { status: _ })
    }

    fn is_visited(&self) -> bool {
        matches!(self, Self::Cell { status: CellStatus::Visited })
    }

    fn new(x: i16, y: i16) -> ElementType {
        if y % 2 == 0 {
            if x % 2 == 0 {
                Self::Intersection
            } else {
                Self::HorizontalWall
            }
        } else {
            if x % 2 == 0 {
                Self::VerticalWall
            } else {
                Self::Cell { status: CellStatus::Empty }
            }
        }
    }
}


#[derive(Copy, Clone, Debug)]
struct Element {
    x: i16,
    y: i16,
    element_type: ElementType,
}


impl Element {
    fn is_boundary(&self) -> bool {
        self.element_type.is_boundary()
    }

    fn is_cell(&self) -> bool {
        self.element_type.is_cell()
    }

    fn is_visited(&self) -> bool {
        self.element_type.is_visited()
    }

    fn new(x: i16, y: i16) -> Self {
        Self {
            x, y,
            element_type: ElementType::new(x, y)
        }
    }

    fn remove_wall(&mut self) {
        assert!(self.element_type.is_boundary());
        self.element_type = match self.element_type {
            ElementType::HorizontalWall => ElementType::HorizontalOpening,
            ElementType::VerticalWall => ElementType::VerticalOpening,
            _ => self.element_type,
        };
    }

    fn visit(&mut self) {
        assert!(self.element_type.is_cell());
        self.element_type = ElementType::Cell { status: CellStatus::Visited }
    }
}


struct Grid {
    width: i16,
    height: i16,
    elements: Vec<Element>,
}


impl Grid {
    fn is_boundary(x: i16, y: i16) -> bool {
        ElementType::new(x, y).is_boundary()
    }

    fn is_cell(x: i16, y: i16) -> bool {
        ElementType::new(x, y).is_cell()
    }

    fn new(width: i16, height: i16) -> Grid {
        let element_count = width as usize * height as usize;
        let mut elements = Vec::with_capacity(element_count);

        for y in 0..height {
            for x in 0..width {
                elements.push(Element::new(x, y));
            }
        }

        Self { width, height, elements }
    }

    fn get(&self, x: i16, y: i16) -> Element {
        let i = y as usize * self.width as usize + x as usize;
        self.elements[i]
    }

    fn set(&mut self, x: i16, y: i16, element: Element) {
        assert_eq!(x, element.x);
        assert_eq!(y, element.y);
        let i = y as usize * self.width as usize + x as usize;
        self.elements[i] = element;
    }

    fn update(&mut self, element: Element) {
        self.set(element.x, element.y, element);
    }

    fn orthogonal_neighbors(&self, x: i16, y: i16, distance: i16) -> Vec<Element> {
        let mut neighbors = Vec::new();
        let left = x - distance;
        if left >= 0 {
            neighbors.push(self.get(left, y));
        }
        let right = x + distance;
        if right < self.width {
            neighbors.push(self.get(right, y));
        }
        let above = y - distance;
        if above >= 0 {
            neighbors.push(self.get(x, above));
        }
        let below = y + distance;
        if below < self.height {
            neighbors.push(self.get(x, below));
        }
        neighbors
    }

    fn remove_wall(&mut self, x: i16, y: i16) {
        assert!(Grid::is_boundary(x, y));
        let mut element = self.get(x, y);
        assert!(element.is_boundary());
        element.remove_wall();
        self.update(element);
    }

    fn visit(&mut self, x: i16, y: i16) {
        assert!(Grid::is_cell(x, y));
        let mut element = self.get(x, y);
        assert!(element.is_cell());
        element.visit();
        self.update(element);
    }
}


struct Maze {
    grid: Grid,
    randomizer: Randomizer,
    width: i16,
    height: i16,
}


impl Maze {
    fn new(width: i16, height: i16) -> Self {
        let grid_width = 2 * width + 1;
        let grid_height = 2 * height + 1;
        Self {
            grid: Grid::new(grid_width, grid_height),
            randomizer: Randomizer::new(),
            width,
            height,
        }
    }

    fn generate(&mut self) {
        let mut starting_cell = self.get_cell(0, 0);
        starting_cell.visit();
        self.grid.update(starting_cell);

        let mut stack = vec![starting_cell];
        while let Some(current_cell) = stack.pop() {
            let unvisited_neighbors = self.unvisited_neighbors_of(&current_cell);
            if !unvisited_neighbors.is_empty() {
                stack.push(current_cell);
                let mut chosen_cell = self.randomizer.choose_one(unvisited_neighbors);
                self.remove_wall_between(&current_cell, &chosen_cell);
                chosen_cell.visit();
                self.grid.update(chosen_cell);
                stack.push(chosen_cell);
            }
        }
    }

    fn get_cell(&self, x: i16, y: i16) -> Element {
        let grid_x = 2 * x + 1;
        let grid_y = 2 * y + 1;
        self.grid.get(grid_x, grid_y)
    }

    fn neighbors_of(&self, cell: &Element) -> Vec<Element> {
        assert!(cell.is_cell());
        let neighbors = self.grid.orthogonal_neighbors(cell.x, cell.y, 2);
        neighbors
    }

    fn unvisited_neighbors_of(&self, cell: &Element) -> Vec<Element> {
        let neighbors = self.neighbors_of(cell);
        neighbors.into_iter()
            .filter(|cell| {
                !cell.is_visited()
            })
            .collect()
    }

    fn get_wall_between(&mut self, cell1: &Element, cell2: &Element) -> Element {
        assert!(cell1.is_cell());
        assert!(cell2.is_cell());

        // cell1 left of cell2
        if cell1.x + 2 == cell2.x && cell1.y == cell2.y {
            return self.grid.get(cell1.x + 1, cell1.y)
        }
        // cell1 right of cell2
        if cell1.x - 2 == cell2.x && cell1.y == cell2.y {
            return  self.grid.get(cell1.x - 1, cell1.y)
        }
        // cell1 above of cell2
        if cell1.x == cell2.x && cell1.y + 2 == cell2.y {
            return  self.grid.get(cell1.x, cell1.y + 1)
        }
        // cell1 below of cell2
        if cell1.x == cell2.x && cell1.y - 2 == cell2.y {
            return  self.grid.get(cell1.x, cell1.y - 1)
        }

        panic!("Cells are not adjacent!");
    }

    fn remove_wall_between(&mut self, cell1: &Element, cell2: &Element) {
        let mut element = self.get_wall_between(cell1, cell2);
        element.remove_wall();
        self.grid.update(element);
    }
}


struct Ascii<'m> {
    maze: &'m Maze,
}


impl<'m> Ascii<'m> {
    fn new(maze: &'m Maze) -> Self {
        Self { maze }
    }
}


impl<'m> Display for Ascii<'m> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.maze.grid.height {
            for x in 0..self.maze.grid.width {
                let element = self.maze.grid.get(x, y);
                match element.element_type {
                    ElementType::Cell { .. } => f.write_str("  ")?,
                    ElementType::HorizontalOpening => f.write_str("  ")?,
                    ElementType::VerticalOpening => f.write_str(" ")?,
                    ElementType::HorizontalWall => f.write_str("--")?,
                    ElementType::VerticalWall => f.write_str("|")?,
                    ElementType::Intersection => f.write_str("+")?,
                }
            }
            f.write_str("\n")?;
        }
        Ok(())
    }
}
