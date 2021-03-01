from file_formats.links_page.parser import parse
from website.pages.links_page import build_links_page


def iain_m_banks():
    build_links_page(parse(source))


source = """
.page links Iain M Banks

Banks passed away in 2013, and I've been carefully parceling out his
remaining novels since.  

.section links The Culture Novels

Banks creates a vision of a galaxy-spanning
post-scarcity future that is unique, hopeful and somehow very comforting
in its humanity.  I was hooked in the early chapters of
<em>Consider Phlebas</em>, though lots of folks in 
<a href=https://www.reddit.com/r/printSF/>r/printSF</a> seem lukewarm
on this one.  <em>The Player of Games</em> and <em>Use of
Weapons</em> are probably better and more accessible starting places.
For me, <em>Look to Windward</em> best captures the heart and soul of
the Culture.            

.link book Consider Phlebas
.url https://www.amazon.com/gp/product/B0013TX6FI
.date 1987
.checked

.link book The Player of Games
.url https://www.amazon.com/gp/product/B002WM3HC2
.date 1988
.checked

.link book Use of Weapons
.url https://www.amazon.com/gp/product/B0015DWLTE
.date 1990
.checked

.link book The State of the Art (collection) 
.url https://www.goodreads.com/book/show/129131.The_State_of_the_Art
.date 1991
.checked

.link book Excession
.url https://www.amazon.com/Excession-Iain-M-Banks/dp/0553575376
.date 1996
.checked

.link book Inversions
.url https://www.amazon.com/Inversions-Iain-M-Banks/dp/074341196X
.date 1998
.checked

.link book Look to Windward
.url https://www.amazon.com/gp/product/B001D20270
.date 2000
.checked

.link book Matter
.url https://www.amazon.com/gp/product/B000VMHI98
.date 2008
.checked

.link book Surface Detail
.url https://www.amazon.com/gp/product/B0046A9NLC
.date 2010
.checked

.link book The Hydrogen Sonata
.url https://www.amazon.com/gp/product/B0081BU42O
.date 2012
.checked

.section links Other Novels

.link book Against a Dark Background
.url https://www.amazon.com/gp/product/B002CT0TXK
.date 1993

.link book Feersum Endjinn
.url https://www.amazon.com/Feersum-Endjinn-Novel-Iain-Banks/dp/0553374591
.date 1994

.link book The Algebraist
.url https://www.amazon.com/Algebraist-Iain-M-Banks/dp/1597800449
.date 2004

.link book Transition
.url https://www.amazon.com/gp/product/B002O0Q6YS
.date 2009
"""
