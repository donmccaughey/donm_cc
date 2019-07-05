use crate::options::Options;


#[derive(Debug)]
pub struct Report<'o> {
    pub options: &'o Options,
}

impl<'o> Report<'o> {
    pub fn new(options: &'o Options) -> Report {
        Report {
            options: options,
        }
    }

    pub fn will_read_site_definition(&self) {
        let site_definition_file = self.options.site_definition_file.to_string_lossy();
        println!("Reading site data from {}", site_definition_file);
    }

    pub fn did_read_site_definition(&self) {

    }

    pub fn will_generate_site(&self) {
        let output_dir = self.options.output_dir.to_string_lossy();
        println!("Generating site HTML to {}", output_dir);
    }

    pub fn did_generate_site(&self) {

    }
}
