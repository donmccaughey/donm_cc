import unittest
import main


class MainTestCase(unittest.TestCase):
    def test_all(self):
        main.root.find_files('../wwwroot')
        all = main.root.all
        expected = [
            './index.html',
            './aughey/index.html',
            './banners/',
            './banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg',
            './banners/Don_and_Molly_hiking_Texas_winter_2016.jpg',
            './base.css',
            './business_novels/index.html',
            './engineering_management/index.html',
            './hash_tables/index.html',
            './icons/',
            './icons/github.png',
            './icons/copper.png',
            './icons/twitter.png',
            './icons/linkedin.png',
            './icons/truework.png',
            './macos_packages/index.html',
            './macos_packages/source-32x32.png',
            './macos_packages/index.html',
            './macos_packages/package-32x32.png',
            './macos_packages/project-32x32.png',
            './make/index.html',
            './memory_match/index.html',
            './memory_match/gear.png',
            './memory_match/index.html',
            './memory_match/convert_code_points.py',
            './memory_match/memory_match.js',
            './random_words/index.html',
            './random_words/index.html',
            './random_words/random_words.js',
            './random_words/words.table',
            './random_words/make_table.py',
            './random_words/word.list',
            './random_words/random_words.css',
            './resume/',
            './resume/Resume_of_Don_McCaughey.pdf',
            './rust_and_wasm/index.html',
            './science_fiction/index.html',
            './science_fiction/alastair_reynolds.html',
            './science_fiction/iain_m_banks.html',
            './science_fiction/james_sa_corey.html',
            './science_fiction/lois_mcmaster_bujold.html',
        ]
        self.assertEqual(expected, [item.path for item in all])


if __name__ == '__main__':
    unittest.main()
