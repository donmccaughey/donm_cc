import unittest
import main


class MainTestCase(unittest.TestCase):
    def test_all(self):
        main.root.find_files('../wwwroot')
        all = main.root.all
        expected = [
            (0, './index.html', '/'),
            (1, './aughey/index.html', '/aughey/'),
            (2, './aughey/handstand.jpg', '/aughey/handstand.jpg'),
            (1, './banners/', '/banners/'),
            (2, './banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg', '/banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg'),
            (2, './banners/Don_and_Molly_hiking_Texas_winter_2016.jpg', '/banners/Don_and_Molly_hiking_Texas_winter_2016.jpg'),
            (1, './base.css', '/base.css'),
            (1, './bash/index.html', '/bash/'),
            (1, './business_novels/index.html', '/business_novels/'),
            (1, './engineering_management/index.html', '/engineering_management/'),
            (1, './hashtables/index.html', '/hashtables/'),
            (1, './icons/', '/icons/'),
            (2, './icons/copper.png', '/icons/copper.png'),
            (2, './icons/github.png', '/icons/github.png'),
            (2, './icons/linkedin.png', '/icons/linkedin.png'),
            (2, './icons/truework.png', '/icons/truework.png'),
            (2, './icons/twitter.png', '/icons/twitter.png'),
            (1, './macos_packages/index.html', '/macos_packages/'),
            (2, './macos_packages/package-32x32.png', '/macos_packages/package-32x32.png'),
            (2, './macos_packages/project-32x32.png', '/macos_packages/project-32x32.png'),
            (2, './macos_packages/source-32x32.png', '/macos_packages/source-32x32.png'),
            (1, './make/index.html', '/make/'),
            (1, './memory_match/index.html', '/memory_match/'),
            (2, './memory_match/convert_code_points.py', '/memory_match/convert_code_points.py'),
            (2, './memory_match/gear.png', '/memory_match/gear.png'),
            (2, './memory_match/memory_match.js', '/memory_match/memory_match.js'),
            (1, './random_words/index.html', '/random_words/'),
            (2, './random_words/make_table.py', '/random_words/make_table.py'),
            (2, './random_words/random_words.css', '/random_words/random_words.css'),
            (2, './random_words/random_words.js', '/random_words/random_words.js'),
            (2, './random_words/word.list', '/random_words/word.list'),
            (2, './random_words/words.table', '/random_words/words.table'),
            (1, './resume/', '/resume/'),
            (2, './resume/Resume_of_Don_McCaughey.pdf', '/resume/Resume_of_Don_McCaughey.pdf'),
            (1, './rust_and_wasm/index.html', '/rust_and_wasm/'),
            (1, './science_fiction/index.html', '/science_fiction/'),
            (2, './science_fiction/alastair_reynolds.html', '/science_fiction/alastair_reynolds.html'),
            (2, './science_fiction/iain_m_banks.html', '/science_fiction/iain_m_banks.html'),
            (2, './science_fiction/james_sa_corey.html', '/science_fiction/james_sa_corey.html'),
            (2, './science_fiction/lois_mcmaster_bujold.html', '/science_fiction/lois_mcmaster_bujold.html'),
        ]
        actual = [(item.rank, item.path, item.url) for item in all]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
