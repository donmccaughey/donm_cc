use crate::options::Options;
use crate::page::Page;
use crate::site::Site;


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
        match self.options.verbose {
            0 => (),
            1 => {
                let site_definition_file = self.options.site_definition_file.to_string_lossy();
                println!("Reading site data from '{}'", site_definition_file);
            },
            _ => {
                let site_definition_file = self.options.site_definition_file.to_string_lossy();
                println!("Will read site data from '{}'", site_definition_file);
            },
        }
    }

    pub fn did_read_site_definition(&self, site: &Site) {
        match self.options.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Did read data for site \"{}\"", site.name);
            },
        }
    }

    pub fn will_generate_site(&self, site: &Site) {
        match self.options.verbose {
            0 => (),
            1 => {
                let output_dir = self.options.output_dir.to_string_lossy();
                println!("Generating site \"{}\" to {}", site.name, output_dir);
            },
            _ => {
                let output_dir = self.options.output_dir.to_string_lossy();
                println!("Will generate site \"{}\" to {}", site.name, output_dir);
            },
        }
    }

    pub fn did_generate_site(&self, site: &Site) {
        match self.options.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Did generate site \"{}\"", site.name);
            },
        }
    }

    pub fn will_generate_page(&self, page: &Page) {
        match self.options.verbose {
            0 => (),
            1 => {
                let path = page.path.to_string_lossy();
                println!("Generating page \"{}\" at {}", page.title, path);
            },
            _ => {
                let path = page.path.to_string_lossy();
                println!("Will generate page \"{}\" at {}", page.title, path);
            },
        }
    }

    pub fn did_generate_page(&self, page: &Page) {
        match self.options.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Did generate page \"{}\"", page.title);
            },
        }
    }
}
