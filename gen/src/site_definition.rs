use std::error::Error;

use crate::report::Report;
use crate::options::Options;


#[derive(Debug)]
pub struct SiteDefinition<'o, 'r> {
    pub options: &'o Options,
    pub report: &'r Report<'o>,
}

impl<'o, 'r> SiteDefinition<'o, 'r> {
    pub fn read(options: &'o Options, report: &'r Report<'o>)
        -> Result<SiteDefinition<'o, 'r>, Box<dyn Error>>
    {
        report.will_read_site_definition();

        let site_definition = SiteDefinition {
            options: options,
            report: report,
        };

        report.did_read_site_definition();
        Ok(site_definition)
    }

    pub fn generate(&self) -> Result<(), Box<dyn Error>> {
        self.report.will_generate_site();

        self.report.did_generate_site();
        Ok(())
    }
}
