use std::fmt::{Display, Formatter};
use std::time::{SystemTime, UNIX_EPOCH};
use getrandom::getrandom;
use oorandom::Rand32;
use wasm_bindgen::prelude::*;
use crate::Element::{Boundary, Square, Intersection};
use crate::Fill::{Open, Solid};
use crate::Orientation::{Horizontal, Vertical};


/// Generate a seed.  Use the best available operating system source, via
/// the [getrandom](https://crates.io/crates/getrandom) crate.  Fall back
/// to the system time and finally an arbitrary seed on errors.
#[wasm_bindgen]
pub fn generate_seed() -> u64 {
    let mut seed_bytes = [0u8; 8];
    let value: u64;
    if let Ok(_) = getrandom(&mut seed_bytes) {
        value = u64::from_le_bytes(seed_bytes);
    } else if let Ok(unix_timestamp) = SystemTime::now().duration_since(UNIX_EPOCH) {
        value = unix_timestamp.as_micros() as u64;
    } else {
        value = 8015536314858786381;
    };
    value
}


#[wasm_bindgen]
pub fn generate_maze(width: i16, height: i16, seed: u64, format: &str) -> String {
    let mut maze = Maze::new(width, height, seed);
    maze.generate();
    if "unicode" == format {
        UnicodeRenderer::new(&maze).to_string()
    } else {
        AsciiRenderer::new(&maze).to_string()
    }
}


trait Choose {
    fn choose_one(&self, rand32: &mut Rand32) -> Location;
}


impl Choose for Vec<Location> {
    fn choose_one(&self, rand32: &mut Rand32) -> Location {
        let count = self.len() as u32;
        let i = rand32.rand_range(0..count) as usize;
        self[i]
    }
}


#[derive(Copy, Clone, Debug)]
enum SquareStatus {
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
enum Element {
    Square { status: SquareStatus },
    Boundary {
        fill: Fill,
        orientation: Orientation,
    },
    Intersection,
}


impl Element {
    fn is_boundary(&self) -> bool {
        matches!(self, Self::Boundary { .. })
    }

    fn is_square(&self) -> bool {
        matches!(self, Self::Square { .. })
    }

    fn is_visited(&self) -> bool {
        matches!(self, Self::Square { status: SquareStatus::Visited })
    }

    fn is_wall(&self) -> bool {
        !matches!(self, Self::Boundary { fill: Open, .. })
    }

    fn new(x: i16, y: i16) -> Element {
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
                Self::Square { status: SquareStatus::Empty }
            }
        }
    }
}


/// A `Location` holds an `Element` and its `(x, y)` coordinates.
#[derive(Copy, Clone, Debug)]
struct Location {
    element: Element,
    x: i16,
    y: i16,
}


impl Location {
    fn is_boundary(&self) -> bool {
        self.element.is_boundary()
    }

    fn is_square(&self) -> bool {
        self.element.is_square()
    }

    fn is_visited(&self) -> bool {
        self.element.is_visited()
    }

    fn new(element: Element, x: i16, y: i16) -> Self {
        Self { element, x, y }
    }

    fn remove_wall(&mut self) {
        assert!(self.is_boundary());
        if let Boundary { fill: _, orientation } = self.element {
            self.element = Boundary { fill: Open, orientation };
        }
    }

    fn visit(&mut self) {
        assert!(self.is_square());
        self.element = Square { status: SquareStatus::Visited }
    }
}


struct Grid {
    width: i16,
    height: i16,
    elements: Vec<Element>,
}


impl Grid {
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
        grid.set(Location {
            x: 1,
            y: 0,
            element: Boundary {
                fill: Fill::Start,
                orientation: Horizontal,
            }
        });

        // set finish point
        let xf = width - 2;
        let yf = height - 1;
        grid.set(Location {
            x: xf,
            y: yf,
            element: Boundary {
                fill: Fill::Finish,
                orientation: Horizontal,
            }
        });

        grid
    }

    fn get(&self, x: i16, y: i16) -> Location {
        let i = y as usize * self.width as usize + x as usize;
        Location::new(self.elements[i], x, y)
    }

    fn set(&mut self, location: Location) {
        let i = location.y as usize * self.width as usize + location.x as usize;
        self.elements[i] = location.element;
    }

    fn get_left_neighbor(&self, x: i16, y: i16, distance: i16) -> Option<Location> {
        let left = x - distance;
        if left >= 0 {
            Some(self.get(left, y))
        } else {
            None
        }
    }

    fn get_right_neighbor(&self, x: i16, y: i16, distance: i16) -> Option<Location> {
        let right = x + distance;
        if right < self.width {
            Some(self.get(right, y))
        } else {
            None
        }
    }

    fn get_top_neighbor(&self, x: i16, y: i16, distance: i16) -> Option<Location> {
        let top = y - distance;
        if top >= 0 {
            Some(self.get(x, top))
        } else {
            None
        }
    }

    fn get_bottom_neighbor(&self, x: i16, y: i16, distance: i16) -> Option<Location> {
        let bottom = y + distance;
        if bottom < self.height {
            Some(self.get(x, bottom))
        } else {
            None
        }
    }

    fn orthogonal_neighbors(&self, x: i16, y: i16, distance: i16) -> Vec<Location> {
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
}


struct Maze {
    grid: Grid,
    seed: u64,
}


impl Maze {
    fn new(width: i16, height: i16, seed: u64) -> Self {
        let grid_width = 2 * width + 1;
        let grid_height = 2 * height + 1;
        Self {
            grid: Grid::new(grid_width, grid_height),
            seed,
        }
    }

    fn generate(&mut self) {
        let mut rand32 = Rand32::new(self.seed);

        let mut starting_square = self.get_square(0, 0);
        starting_square.visit();
        self.grid.set(starting_square);

        let mut stack = vec![starting_square];
        while let Some(current_square) = stack.pop() {
            let unvisited_neighbors = self.unvisited_neighbors_of(&current_square);
            if !unvisited_neighbors.is_empty() {
                stack.push(current_square);
                let mut chosen_square = unvisited_neighbors.choose_one(&mut rand32);
                self.remove_wall_between(&current_square, &chosen_square);
                chosen_square.visit();
                self.grid.set(chosen_square);
                stack.push(chosen_square);
            }
        }
    }

    fn get_square(&self, x: i16, y: i16) -> Location {
        let grid_x = 2 * x + 1;
        let grid_y = 2 * y + 1;
        self.grid.get(grid_x, grid_y)
    }

    fn neighbors_of(&self, square: &Location) -> Vec<Location> {
        assert!(square.is_square());
        let neighbors = self.grid.orthogonal_neighbors(square.x, square.y, 2);
        neighbors
    }

    fn unvisited_neighbors_of(&self, square: &Location) -> Vec<Location> {
        let neighbors = self.neighbors_of(square);
        neighbors.into_iter()
            .filter(|square| {
                !square.is_visited()
            })
            .collect()
    }

    fn get_boundary_between(&mut self, square1: &Location, square2: &Location) -> Location {
        assert!(square1.is_square());
        assert!(square2.is_square());

        // square1 left of square2
        if square1.x + 2 == square2.x && square1.y == square2.y {
            return self.grid.get(square1.x + 1, square1.y)
        }
        // square1 right of square2
        if square1.x - 2 == square2.x && square1.y == square2.y {
            return  self.grid.get(square1.x - 1, square1.y)
        }
        // square1 above of square2
        if square1.x == square2.x && square1.y + 2 == square2.y {
            return  self.grid.get(square1.x, square1.y + 1)
        }
        // square1 below of square2
        if square1.x == square2.x && square1.y - 2 == square2.y {
            return  self.grid.get(square1.x, square1.y - 1)
        }

        panic!("Squares are not adjacent!");
    }

    fn remove_wall_between(&mut self, square1: &Location, square2: &Location) {
        let mut location = self.get_boundary_between(square1, square2);
        location.remove_wall();
        self.grid.set(location);
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


fn is_wall(location: Option<Location>) -> bool {
    if let Some(location) = location {
        location.element.is_wall()
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
                let location = self.maze.grid.get(x, y);
                match location.element {
                    Square { .. } => f.write_str("  ")?,
                    Boundary { fill: Solid, orientation: Horizontal } => f.write_str("--")?,
                    Boundary { fill: Solid, orientation: Vertical } => f.write_str("|")?,
                    Boundary { orientation: Horizontal, .. } => f.write_str("  ")?,
                    Boundary { orientation: Vertical, .. } => f.write_str(" ")?,
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
                let location = self.maze.grid.get(x, y);
                match location.element {
                    Square { .. } => f.write_str("  ")?,
                    Boundary { fill: Solid, orientation: Horizontal } => f.write_str("\u{2500}\u{2500}")?,
                    Boundary { fill: Solid, orientation: Vertical } => f.write_str("\u{2502}")?,
                    Boundary { orientation: Horizontal, .. } => f.write_str("  ")?,
                    Boundary { orientation: Vertical, .. } => f.write_str(" ")?,
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
