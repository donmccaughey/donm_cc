import unittest
import main


class MainTestCase(unittest.TestCase):
    def test_all(self):
        main.root.find_files('../site-src')
        all = main.root.all
        expected = [
            ('./', '/'),
            ('./aughey/', '/aughey/'),
            ('./aughey/handstand.jpg', '/aughey/handstand.jpg'),
            ('./aughey/index.html', '/aughey/index.html'),
            ('./banners/', '/banners/'),
            ('./banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg', '/banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg'),
            ('./banners/Don_and_Molly_hiking_Texas_winter_2016.jpg', '/banners/Don_and_Molly_hiking_Texas_winter_2016.jpg'),
            ('./base.css', '/base.css'),
            ('./bash/', '/bash/'),
            ('./bash/index.html', '/bash/index.html'),
            ('./business_novels/', '/business_novels/'),
            ('./business_novels/index.html', '/business_novels/index.html'),
            ('./engineering_management/', '/engineering_management/'),
            ('./engineering_management/index.html', '/engineering_management/index.html'),
            ('./hashtables/', '/hashtables/'),
            ('./hashtables/index.html', '/hashtables/index.html'),
            ('./icons/', '/icons/'),
            ('./icons/copper.png', '/icons/copper.png'),
            ('./icons/github.png', '/icons/github.png'),
            ('./icons/linkedin.png', '/icons/linkedin.png'),
            ('./icons/truework.png', '/icons/truework.png'),
            ('./icons/twitter.png', '/icons/twitter.png'),
            ('./index.html', '/index.html'),
            ('./macos_packages/', '/macos_packages/'),
            ('./macos_packages/index.html', '/macos_packages/index.html'),
            ('./macos_packages/package-32x32.png', '/macos_packages/package-32x32.png'),
            ('./macos_packages/project-32x32.png', '/macos_packages/project-32x32.png'),
            ('./macos_packages/source-32x32.png', '/macos_packages/source-32x32.png'),
            ('./make/', '/make/'),
            ('./make/index.html', '/make/index.html'),
            ('./memory_match/', '/memory_match/'),
            ('./memory_match/convert_code_points.py', '/memory_match/convert_code_points.py'),
            ('./memory_match/gear.png', '/memory_match/gear.png'),
            ('./memory_match/index.html', '/memory_match/index.html'),
            ('./memory_match/memory_match.js', '/memory_match/memory_match.js'),
            ('./random_words/', '/random_words/'),
            ('./random_words/index.html', '/random_words/index.html'),
            ('./random_words/make_table.py', '/random_words/make_table.py'),
            ('./random_words/random_words.css', '/random_words/random_words.css'),
            ('./random_words/random_words.js', '/random_words/random_words.js'),
            ('./random_words/word.list', '/random_words/word.list'),
            ('./random_words/words.table', '/random_words/words.table'),
            ('./resume/', '/resume/'),
            ('./resume/Resume_of_Don_McCaughey.pdf', '/resume/Resume_of_Don_McCaughey.pdf'),
            ('./rust_and_wasm/', '/rust_and_wasm/'),
            ('./rust_and_wasm/index.html', '/rust_and_wasm/index.html'),
            ('./science_fiction/', '/science_fiction/'),
            ('./science_fiction/alastair_reynolds.html', '/science_fiction/alastair_reynolds.html'),
            ('./science_fiction/iain_m_banks.html', '/science_fiction/iain_m_banks.html'),
            ('./science_fiction/index.html', '/science_fiction/index.html'),
            ('./science_fiction/james_sa_corey.html', '/science_fiction/james_sa_corey.html'),
            ('./science_fiction/lois_mcmaster_bujold.html', '/science_fiction/lois_mcmaster_bujold.html'),
        ]
        actual = [(item.path, item.url) for item in all]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
