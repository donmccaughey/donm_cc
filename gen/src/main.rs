#[macro_use]
extern crate serde_derive;

mod error;
mod options;
mod page;
mod report;
mod site;

use options::Options;
use report::Report;
use site::Site;
use std::error::Error;


fn main() -> Result<(), Box<dyn Error>> {
    let options = Options::new();
    let report = Report::new(&options);
    let site = Site::read(&options, &report)?;
    site.generate(&options, &report)
}
