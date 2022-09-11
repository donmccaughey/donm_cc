# TODO

- remove color from all links
- where is Node.tokens() used?
- strip and crush images
- strip and compress resume pdf
- relocate [markdown pdf] aside on resume page
- rename `test_link_x()` methods to `test_book_link_x()` and ensure coverage for general link cases
- remove `modifier` attribute from `BookLink` class
- should `url_directive()` and `asin_directive()` return `NotMatched`?  See `test_link_missing_url_data()` and `test_book_link_with_asin()`
- should `book_locator()` return `NotMatched`?
- ensure that wrapping works correctly when encountering `<br>` tags:
                    <strong>Square</strong>, 2012 - <em>iPad integration with
                    point−of−sale (POS) hardware</em><br>
                     Built an iOS library
                    linking the Square POS app with the Square Stand.  Worked
                    with the app team and embedded software team to create APIs
- handle block elements inside compact elements and make <address> compact
- fix sitemap to account for relative paths in internal links
- convert absolute paths to relative paths in internal links
- accumulate links from static HTML files -- maybe subclass `File` to `HTMLFile`?
- add link checking for internal links
- add link checking for `sitemap.txt`
- add `.tagline` page file directive to specify home page link subtext
- trace and remove unused css from pages
- investigate stripping unneeded metadata from images
- investigate improving accessibility
  - look into adding roles https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles
- clean up `random_words.js`
- investigate removing jQuery-isms from `memory_match.js`
- support [OpenLibrary links](https://openlibrary.org/dev/docs/api/books) on book links
- support ISBN metadata on book links
- expose ASIN, ISBN, etc in book link HTML as data attributes
- generate alternate representations of links pages (CSV, JSON)
- set up CI in GitHub Actions
- generate gemini site
