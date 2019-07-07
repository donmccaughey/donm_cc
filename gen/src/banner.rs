use std::path::PathBuf;
use std::io::BufWriter;
use std::io::Write;
use std::fs::File;
use std::error::Error;

use crate::error::Error::PathContainsInvalidUnicode;


#[derive(Debug, Deserialize)]
pub struct Banner {
    pub image: PathBuf,
    pub description: String,
    pub caption: String,
}

impl Banner {
    pub fn write(&self, buf_writer: &mut BufWriter<File>) -> Result<(), Box<dyn Error>> {
        let image = self.image.to_str().ok_or(PathContainsInvalidUnicode(self.image.clone()))?;
        write!(buf_writer, "    <div class=banner>\n")?;
        write!(buf_writer, "        <img src='{}' alt='{}'>\n", image, self.description)?;
        write!(buf_writer, "        <span class=caption>{}</span>\n", self.caption)?;
        write!(buf_writer, "    </div>\n")?;
        Ok(())
    }
}
