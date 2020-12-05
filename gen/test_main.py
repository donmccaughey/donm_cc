import unittest
import main


class MainTestCase(unittest.TestCase):
    def test_all(self):
        main.root.find_files('../wwwroot')
        all = main.root.all
        expected = [
            (0, './index.html'),
            (1, './aughey/index.html'),
            (1, './banners/'),
            (2, './banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg'),
            (2, './banners/Don_and_Molly_hiking_Texas_winter_2016.jpg'),
            (1, './base.css'),
            (1, './business_novels/index.html'),
            (1, './engineering_management/index.html'),
            (1, './hash_tables/index.html'),
            (1, './icons/'),
            (2, './icons/github.png'),
            (2, './icons/copper.png'),
            (2, './icons/twitter.png'),
            (2, './icons/linkedin.png'),
            (2, './icons/truework.png'),
            (1, './macos_packages/index.html'),
            (2, './macos_packages/source-32x32.png'),
            (2, './macos_packages/package-32x32.png'),
            (2, './macos_packages/project-32x32.png'),
            (1, './make/index.html'),
            (1, './memory_match/index.html'),
            (2, './memory_match/gear.png'),
            (2, './memory_match/convert_code_points.py'),
            (2, './memory_match/memory_match.js'),
            (1, './random_words/index.html'),
            (2, './random_words/random_words.js'),
            (2, './random_words/words.table'),
            (2, './random_words/make_table.py'),
            (2, './random_words/word.list'),
            (2, './random_words/random_words.css'),
            (1, './resume/'),
            (2, './resume/Resume_of_Don_McCaughey.pdf'),
            (1, './rust_and_wasm/index.html'),
            (1, './science_fiction/index.html'),
            (2, './science_fiction/alastair_reynolds.html'),
            (2, './science_fiction/iain_m_banks.html'),
            (2, './science_fiction/james_sa_corey.html'),
            (2, './science_fiction/lois_mcmaster_bujold.html'),
        ]
        self.assertEqual(expected, [(item.rank, item.path) for item in all])


if __name__ == '__main__':
    unittest.main()
