mod options;
mod report;
mod site_definition;

use options::Options;
use report::Report;
use site_definition::SiteDefinition;
use std::error::Error;


fn main() -> Result<(), Box<dyn Error>> {
    let options = Options::new();
    let report = Report::new(&options);

    let site_definition = SiteDefinition::read(&options, &report)?;
    site_definition.generate()
}
