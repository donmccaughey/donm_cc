use std::error::Error;
use std::fs::create_dir_all;
use std::fs::File;
use std::io::BufWriter;
use std::io::Write;
use std::path::Component::RootDir;
use std::path::PathBuf;

use crate::banner::Banner;
use crate::error::Error::OutputDirIsRoot;
use crate::error::Error::PageExists;
use crate::item::Item;
use crate::options::Options;
use crate::report::Report;


#[derive(Debug, Deserialize)]
pub struct Page {
    pub path: PathBuf,
    pub title: String,

    pub banner: Option<Banner>,

    #[serde(default)]
    pub collection: Vec<Item>,

    #[serde(default)]
    pub children: Vec<Page>,
}

impl Page {
    pub fn generate(&self, options: &Options, report: &Report)
        -> Result<(), Box<dyn Error>>
    {
        report.will_generate_page(self);

        let relative_path = match self.path.strip_prefix(RootDir) {
            Ok(stripped_path) => stripped_path,
            Err(_) => &self.path,
        };

        let mut output_path = options.output_dir.clone();
        output_path.push(relative_path);

        if output_path.exists() && !options.overwrite {
            return Err(Box::new(PageExists(self.title.clone(), output_path.clone())));
        }

        let output_dir = output_path.parent().ok_or(OutputDirIsRoot(self.title.clone()))?;
        create_dir_all(output_dir)?;

        let file = File::create(output_path)?;
        let mut buf_writer = BufWriter::new(file);
        self.write(&mut buf_writer)?;

        report.did_generate_page(self);

        for child in self.children.iter() {
            child.generate(options, report)?;
        }

        Ok(())
    }

    fn write(&self, buf_writer: &mut BufWriter<File>) -> Result<(), Box<dyn Error>> {
        write!(buf_writer, "<!doctype html>\n")?;
        write!(buf_writer, "<html lang=en>\n")?;
        self.write_head(buf_writer)?;
        self.write_body(buf_writer)?;
        write!(buf_writer, "</html>\n")?;
        Ok(())
    }

    fn write_head(&self, buf_writer: &mut BufWriter<File>) -> Result<(), Box<dyn Error>> {
        write!(buf_writer, "<head>\n")?;
        write!(buf_writer, "    <meta charset=utf-8>\n")?;
        write!(buf_writer, "    <meta name=viewport content='initial-scale=0.9, width=device-width'>\n")?;
        write!(buf_writer, "    <title>{}</title>\n", self.title)?;
        write!(buf_writer, "    <link rel=stylesheet href=/base.css>\n")?;
        write!(buf_writer, "</head>\n")?;
        Ok(())
    }

    fn write_body(&self, buf_writer: &mut BufWriter<File>) -> Result<(), Box<dyn Error>> {
        write!(buf_writer, "<body>\n")?;
        self.write_menu(buf_writer)?;
        if let Some(ref banner) = self.banner {
            banner.write(buf_writer)?;
        }
        if !self.collection.is_empty() {
            write!(buf_writer, "    <div class=collection>\n")?;
            for item in self.collection.iter() {
                item.write(buf_writer)?;
            }
            write!(buf_writer, "    </div>\n")?;
        }

        write!(buf_writer, "</body>\n")?;
        Ok(())
    }

    fn write_menu(&self, buf_writer: &mut BufWriter<File>) -> Result<(), Box<dyn Error>> {
        write!(buf_writer, "    <nav class=menu>\n")?;
        write!(buf_writer, "        <a href=/>Don McCaughey</a>\n")?;
        write!(buf_writer, "    </nav>\n")?;
        Ok(())
    }
}
