use crate::abs_path::AbsPath;
use crate::content_folder::ContentFolder;
use crate::page::Page;
use crate::site_def::SiteDef;
use crate::site_file::SiteFile;


#[derive(Debug)]
pub struct Report {
    pub verbose: u8,
}

impl Report {
    pub fn new(verbose: u8) -> Report {
        Report {
            verbose,
        }
    }

    pub fn will_read_site(&self, site_root: &AbsPath) {
        match self.verbose {
            0 => (),
            1 => {
                println!("Reading site from '{}'", site_root);
            },
            _ => {
                println!("Will read site from '{}'", site_root);
            },
        }
    }

    pub fn did_read_site(&self, site_def: &SiteDef) {
        match self.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Did read site \"{}\"", site_def.name);
            },
        }
    }

    pub fn will_read_site_file(&self, site_file_path: &AbsPath) {
        match self.verbose {
            0 => (),
            1 => {
                println!("Reading site file from '{}'", site_file_path);
            },
            _ => {
                println!("Will read site file from '{}'", site_file_path);
            },
        }
    }

    pub fn did_read_site_file(&self, site_file: &SiteFile) {
        match self.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Did read site file for site \"{}\"", site_file.name);
            },
        }
    }

    pub fn will_scan_content_folder(&self, folder_path: &AbsPath) {
        match self.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Will scan folder at \"{}\"", folder_path);
            },
        }
    }

    pub fn did_scan_content_folder(&self, content_folder: &ContentFolder) {
        match self.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Did scan folder \"{}\"", content_folder.abs_path);
            },
        }
    }

    pub fn will_generate_site(&self, site_def: &SiteDef) {
        /*
        match self.verbose {
            0 => (),
            1 => {
                let output_dir = self.options.output_dir.to_string_lossy();
                println!("Generating site \"{}\" to {}", site.site_file.name, output_dir);
            },
            _ => {
                let output_dir = self.options.output_dir.to_string_lossy();
                println!("Will generate site \"{}\" to {}", site.site_file.name, output_dir);
            },
        }
         */
    }

    pub fn did_generate_site(&self, site_def: &SiteDef) {
        match self.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Did generate site \"{}\"", site_def.name);
            },
        }
    }

    pub fn will_generate_page(&self, page: &Page) {
        match self.verbose {
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
        match self.verbose {
            0 => (),
            1 => (),
            _ => {
                println!("Did generate page \"{}\"", page.title);
            },
        }
    }
}
