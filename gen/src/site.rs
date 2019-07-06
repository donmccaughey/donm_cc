use serde_yaml;
use std::error::Error;
use std::fs::create_dir_all;
use std::fs::File;
use std::io::BufReader;

use crate::options::Options;
use crate::page::Page;
use crate::report::Report;


#[derive(Debug, Deserialize)]
pub struct Site {
    pub name: String,
    pub home_page: Page,
}

impl Site {
    pub fn read(options: &Options, report: &Report)
        -> Result<Site, Box<dyn Error>>
    {
        report.will_read_site_definition();

        let file = File::open(&options.site_definition_file)?;
        let reader = BufReader::new(file);
        let site = serde_yaml::from_reader(reader)?;

        report.did_read_site_definition(&site);
        Ok(site)
    }

    pub fn generate(&self, options: &Options, report: &Report)
                    -> Result<(), Box<dyn Error>>
    {
        report.will_generate_site(&self);

        create_dir_all(&options.output_dir)?;
        self.home_page.generate(options, report)?;

        report.did_generate_site(&self);
        Ok(())
    }
}
