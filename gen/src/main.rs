#[macro_use]
extern crate serde_derive;

mod abs_path;
mod banner;
mod content_folder;
mod error;
mod item;
mod options;
mod page;
mod report;
mod site_def;
mod site_file;
mod site_folder;

use options::Options;
use report::Report;
use site_def::SiteDef;
use std::error::Error;


fn main() -> Result<(), Box<dyn Error>> {
    let options = Options::new();
    let report = Report::new(options.verbose);
    let site_def = SiteDef::read(&options.site_root, &report)?;
    // site.generate(&options, &report)
    Ok(())
}
