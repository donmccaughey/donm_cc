use std::path::PathBuf;
use url::Url;
use url_serde;
use std::io::BufWriter;
use std::io::Write;
use std::fs::File;
use std::error::Error;
use crate::error::Error::PathContainsInvalidUnicode;


#[derive(Debug, Deserialize)]
#[serde(untagged)]
pub enum Link {
    Global {
        #[serde(with = "url_serde")]
        url: Url
    },
    Local {
        path: PathBuf
    },
}

impl Link {
    pub fn class(&self) -> String {
        match *self {
            Link::Global { url: _ } => "item",
            Link::Local { path: _ } => "item local",
        }.to_string()
    }

    pub fn href(&self) -> Result<String, Box<dyn Error>> {
        match *self {
            Link::Global { ref url } => Ok(url.to_string()),
            Link::Local { ref path } => {
                path.to_str()
                    .map(String::from)
                    .ok_or(Box::new(PathContainsInvalidUnicode(path.clone())))
            },
        }
    }
}


#[derive(Debug, Deserialize)]
pub struct Favicon {
    path: PathBuf,
    description: String,
}


#[derive(Debug, Deserialize)]
pub struct Item {
    #[serde(flatten)]
    link: Link,

    favicon: Option<Favicon>,
    title: String,
    subtitle: String,
}

impl Item {
    pub fn write(&self, buf_writer: &mut BufWriter<File>) -> Result<(), Box<dyn Error>> {
        let href = self.link.href()?;
        write!(buf_writer, "        <a class='{}' href='{}'>\n", self.link.class(), href)?;
        if let Some(ref favicon) = self.favicon {
            let src = favicon.path.to_str().ok_or(PathContainsInvalidUnicode(favicon.path.clone()))?;
            write!(buf_writer, "            <img class=favicon src='{}' alt='{}'>\n", src, favicon.description)?;
        }
        write!(buf_writer, "            <strong>{}</strong>\n", self.title)?;
        write!(buf_writer, "            <br><em>{}</em>\n", self.title)?;
        write!(buf_writer, "        </a>\n")?;
        Ok(())
    }
}
