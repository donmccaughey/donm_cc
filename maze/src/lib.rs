use std::fmt::{Display, Formatter};
use std::time::{SystemTime, UNIX_EPOCH};
use getrandom::getrandom;
use oorandom::Rand32;
use wasm_bindgen::prelude::*;
use crate::ElementType::{Boundary, Cell, Intersection};
use crate::Fill::{Open, Solid};
use crate::Orientation::{Horizontal, Vertical};


#[wasm_bindgen]
pub fn generate_maze(width: i16, height: i16, output: &str) -> String {
    let mut maze = Maze::new(width, height);
    maze.generate();
    if "unicode" == output {
        UnicodeRenderer::new(&maze).to_string()
    } else {
        AsciiRenderer::new(&maze).to_string()
    }
}


/// A value for seeding the pseudorandom number generator.
#[derive(Copy, Clone, Debug)]
struct Seed {
    value: u64,
}


impl Seed {
    /// Generate a seed.  Use the best available operating system source, via
    /// the [getrandom](https://crates.io/crates/getrandom) crate.  Fall back
    /// to the system time and finally an arbitrary seed on errors.
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


/// A pseudorandom number generator.  Wraps a [Seed] and
/// [oorandom](https://crates.io/crates/oorandom)'s [Rand32].
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

    /// Choose one element randomly from a [Vec].
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


#[derive(Copy, Clone, Debug)]
enum Fill {
    Open, Solid, Start, Finish
}


#[derive(Copy, Clone, Debug)]
enum Orientation {
    Horizontal, Vertical,
}


#[derive(Copy, Clone, Debug)]
enum ElementType {
    Cell { status: CellStatus },
    Boundary {
        fill: Fill,
        orientation: Orientation,
    },
    Intersection,
}


impl ElementType {
    fn is_boundary(&self) -> bool {
        matches!(self, Self::Boundary { fill: _, orientation: _ })
    }

    fn is_cell(&self) -> bool {
        matches!(self, Self::Cell { status: _ })
    }

    fn is_visited(&self) -> bool {
        matches!(self, Self::Cell { status: CellStatus::Visited })
    }

    fn is_wall(&self) -> bool {
        !matches!(self, Self::Boundary { fill: Open, orientation: _ })
    }

    fn new(x: i16, y: i16) -> ElementType {
        if y % 2 == 0 {
            if x % 2 == 0 {
                Self::Intersection
            } else {
                Self::Boundary { fill: Solid, orientation: Horizontal }
            }
        } else {
            if x % 2 == 0 {
                Self::Boundary { fill: Solid, orientation: Vertical }
            } else {
                Self::Cell { status: CellStatus::Empty }
            }
        }
    }
}


/// An `Element` represents a square on the maze map, or a boundary between
/// squares.  Boundaries can be horizontal, vertical or the intersection of
/// horizontal and vertical boundaries.
///
///      0 1 2 3 4
///    0 + - + - +
///    1 |   |   |
///    2 + - + - +
///
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
        if let Boundary { fill: _, orientation } = self.element_type {
            self.element_type = Boundary { fill: Open, orientation };
        }
    }

    fn visit(&mut self) {
        assert!(self.element_type.is_cell());
        self.element_type = Cell { status: CellStatus::Visited }
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

        let mut grid = Self { width, height, elements };

        // set start point
        grid.set(1, 0, Element {
            x: 1,
            y: 0,
            element_type: Boundary {
                fill: Fill::Start,
                orientation: Horizontal,
            }
        });

        // set finish point
        let xf = width - 2;
        let yf = height - 1;
        grid.set(xf, yf, Element {
            x: xf,
            y: yf,
            element_type: Boundary {
                fill: Fill::Finish,
                orientation: Horizontal,
            }
        });

        grid
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

    fn get_left_neighbor(&self, x: i16, y: i16, distance: i16) -> Option<Element> {
        let left = x - distance;
        if left >= 0 {
            Some(self.get(left, y))
        } else {
            None
        }
    }

    fn get_right_neighbor(&self, x: i16, y: i16, distance: i16) -> Option<Element> {
        let right = x + distance;
        if right < self.width {
            Some(self.get(right, y))
        } else {
            None
        }
    }

    fn get_top_neighbor(&self, x: i16, y: i16, distance: i16) -> Option<Element> {
        let top = y - distance;
        if top >= 0 {
            Some(self.get(x, top))
        } else {
            None
        }
    }

    fn get_bottom_neighbor(&self, x: i16, y: i16, distance: i16) -> Option<Element> {
        let bottom = y + distance;
        if bottom < self.height {
            Some(self.get(x, bottom))
        } else {
            None
        }
    }

    fn orthogonal_neighbors(&self, x: i16, y: i16, distance: i16) -> Vec<Element> {
        let mut neighbors = Vec::new();
        if let Some(neighbor) = self.get_left_neighbor(x, y, distance) {
            neighbors.push(neighbor);
        }
        if let Some(neighbor) = self.get_top_neighbor(x, y, distance) {
            neighbors.push(neighbor);
        }
        if let Some(neighbor) = self.get_right_neighbor(x, y, distance) {
            neighbors.push(neighbor);
        }
        if let Some(neighbor) = self.get_bottom_neighbor(x, y, distance) {
            neighbors.push(neighbor);
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


const HLINE: char = '\u{2500}';
const VLINE: char = '\u{2502}';

// Four-way intersection: Left, Top, Right, Bottom
const LTRB: char = '\u{253c}'; // ┼

// Three-way intersections
const LTR: char = '\u{2534}'; // ┴
const TRB: char = '\u{251c}'; // ├
const RBL: char = '\u{252c}'; // ┬
const BLT: char = '\u{2524}'; // ┤

// Two-way intersections
const LT: char = '\u{2518}'; // ┘
const TR: char = '\u{2514}'; // └
const RB: char = '\u{250c}'; // ┌
const BL: char = '\u{2510}'; // ┐


fn is_wall(element: Option<Element>) -> bool {
    if let Some(element) = element {
        element.element_type.is_wall()
    } else {
        false
    }
}


fn ascii_char_for_intersection(grid: &Grid, x: i16, y: i16) -> char {
    let left = is_wall(grid.get_left_neighbor(x, y, 1));
    let top = is_wall(grid.get_top_neighbor(x, y, 1));
    let right = is_wall(grid.get_right_neighbor(x, y, 1));
    let bottom = is_wall(grid.get_bottom_neighbor(x, y, 1));

    // four-way intersection
    if left && top && right && bottom {
        return '+';
    }

    // three-way intersections
    if left && top && right {
        return '+';
    }
    if top && right && bottom {
        return '+';
    }
    if right && bottom && left {
        return '+';
    }
    if bottom && left && top {
        return '+';
    }

    // two-way intersections
    if left && top {
        return '+';
    }
    if top && right {
        return '+';
    }
    if right && bottom {
        return '+';
    }
    if bottom && left {
        return '+';
    }
    if left && right {
        return '-';
    }
    if top && bottom {
        return '|';
    }

    // one-way intersection
    if left || right {
        return '-';
    }
    if top || bottom {
        return '|';
    }

    '+'
}


fn unicode_char_for_intersection(grid: &Grid, x: i16, y: i16) -> char {
    let left = is_wall(grid.get_left_neighbor(x, y, 1));
    let top = is_wall(grid.get_top_neighbor(x, y, 1));
    let right = is_wall(grid.get_right_neighbor(x, y, 1));
    let bottom = is_wall(grid.get_bottom_neighbor(x, y, 1));

    // four-way intersection
    if left && top && right && bottom {
        return LTRB;
    }

    // three-way intersections
    if left && top && right {
        return LTR;
    }
    if top && right && bottom {
        return TRB;
    }
    if right && bottom && left {
        return RBL;
    }
    if bottom && left && top {
        return BLT;
    }

    // two-way intersections
    if left && top {
        return LT;
    }
    if top && right {
        return TR;
    }
    if right && bottom {
        return RB;
    }
    if bottom && left {
        return BL;
    }
    if left && right {
        return HLINE;
    }
    if top && bottom {
        return VLINE;
    }

    // one-way intersection
    if left || right {
        return HLINE;
    }
    if top || bottom {
        return VLINE;
    }

    '*'
}


struct AsciiRenderer<'m> {
    maze: &'m Maze,
}


impl<'m> AsciiRenderer<'m> {
    fn new(maze: &'m Maze) -> Self {
        Self { maze }
    }
}


impl<'m> Display for AsciiRenderer<'m> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.maze.grid.height {
            for x in 0..self.maze.grid.width {
                let element = self.maze.grid.get(x, y);
                match element.element_type {
                    Cell { .. } => f.write_str("  ")?,
                    Boundary { fill: Solid, orientation: Horizontal } => f.write_str("--")?,
                    Boundary { fill: Solid, orientation: Vertical } => f.write_str("|")?,
                    Boundary { fill: _, orientation: Horizontal } => f.write_str("  ")?,
                    Boundary { fill: _, orientation: Vertical } => f.write_str(" ")?,
                    Intersection => {
                        write!(f, "{}", ascii_char_for_intersection(&self.maze.grid, x, y))?
                    },
                }
            }
            f.write_str("\n")?;
        }
        Ok(())
    }
}


struct UnicodeRenderer<'m> {
    maze: &'m Maze,
}


impl<'m> UnicodeRenderer<'m> {
    fn new(maze: &'m Maze) -> Self {
        Self { maze }
    }
}


impl<'m> Display for UnicodeRenderer<'m> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.maze.grid.height {
            for x in 0..self.maze.grid.width {
                let element = self.maze.grid.get(x, y);
                match element.element_type {
                    Cell { .. } => f.write_str("  ")?,
                    Boundary { fill: Solid, orientation: Horizontal } => f.write_str("\u{2500}\u{2500}")?,
                    Boundary { fill: Solid, orientation: Vertical } => f.write_str("\u{2502}")?,
                    Boundary { fill: _, orientation: Horizontal } => f.write_str("  ")?,
                    Boundary { fill: _, orientation: Vertical } => f.write_str(" ")?,
                    Intersection => {
                        write!(f, "{}", unicode_char_for_intersection(&self.maze.grid, x, y))?
                    },
                }
            }
            f.write_str("\n")?;
        }
        Ok(())
    }
}
