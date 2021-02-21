from file_formats.links_page.parser import Parser
from file_formats.links_page.lexer import tokenize
from website.pages.links_page import build_links_page


def alastair_reynolds():
    parser = Parser(tokenize(source))
    if not parser.parse():
        raise parser.error
    build_links_page(parser.links_page)


source = """
.page links Alastair Reynolds

Reynolds is an astrophysicist turned writer with a nack for
creating trippy, mind-bending stories.


.section links Revelation Space

<em>Revelation Space</em> is the gateway drug that got me hooked
on Reynolds' strange vision of the future.  It forms
a loosely connected trilogy with <em>Redemption Ark</em> (featuring
a riveting near-light-speed chase between the stars spanning decades) and 
<em>Absolution Gap</em> (with a virus-induced religious cult, moving cathedrals
and a vanishing gas giant). 

<em>Aurora Rising</em> and <em>Elysium Fire</em> form the
<a href=http://approachingpavonis.blogspot.com/2017/07/elysium-fire-and-new-title-for-prefect.html>Prefect
Dreyfuss Emergency</a> sub-series.  They're police procedurals
set in the Glitter Band, a swarm of thousands of orbital habitats.

.link book Revelation Space
.url https://www.amazon.com/gp/product/B001QL5MAA
.date 2000
.checked

.link book Chasm City
.url https://www.amazon.com/gp/product/B000OIZUH6
.date 2001
.checked

.link book Diamond Dogs, Turquoise Days
.url https://www.amazon.com/gp/product/B001JJWICY
.date 2002
.checked

.link book Redemption Ark
.url https://www.amazon.com/gp/product/B001LFDABO
.date 2002
.checked

.link book Absolution Gap
.url https://www.amazon.com/gp/product/B001ODO61G
.date 2003
.checked

.link book Galactic North
.url https://www.amazon.com/gp/product/B0017SWQJW
.date 2006

.link book The Prefect / Aurora Rising 
.url https://www.amazon.com/gp/product/B0015DYJY4
.date 2007
.checked

.link book Elysium Fire
.url https://www.amazon.com/gp/product/B073P43TMS
.date 2018
.checked


.section links Poseidon's Children

.link book Blue Remembered Earth
.url https://www.amazon.com/gp/product/B005ZOCF5E
.date 2012
.checked

.link book On the Steel Breeze
.url https://www.amazon.com/gp/product/B00H2V6IN8
.date 2013
.checked

.link book Poseidon's Wake
.url https://www.amazon.com/gp/product/B00X5937LW
.date 2015
.checked


.section links Revenger

.link book Revenger
.url https://www.amazon.com/gp/product/B01LXW2IUQ
.date 2016
.checked

.link book Shadow Captain
.url https://www.amazon.com/gp/product/B07CWQN8FQ
.date 2019

.link book Bone Silence
.url https://www.amazon.com/gp/product/B0819W4456
.date 2020

.section links Merlin

<a href=http://approachingpavonis.blogspot.com/2016/10/new-merlin-story-iron-tactician.html>There are four Merlin stories to date, ...</a>

.link book Hideaway
.url https://www.goodreads.com/book/show/34793859-hideaway
.date 2000

.link book Minla's Flowers (included in <em>Zima Blue</em>)
.url https://www.amazon.com/gp/product/B00GVG07DC
.date 2009
.checked

.link book The Iron Tactician
.url https://www.amazon.com/Iron-Tactician-Alastair-Reynolds-ebook/dp/B01M2B9P7V
.date 2016

.link book Merlin's Gun
.url https://www.amazon.com/Mammoth-Books-presents-Merlins-Gun-ebook/dp/B00OGUTTEI
.date 2012
.checked


.section links House of Suns

.link book Thousandth Night
.url https://www.amazon.com/Thousandth-Night-Alastair-Reynolds-ebook/dp/B00C89ORWI
.date 2013

.link book House of Suns
.url https://www.amazon.com/gp/product/B002AKPECW
.date 2008
.checked


.section links Other Stories

.link book Century Rain
.url https://www.amazon.com/gp/product/B0010SB6OK
.date 2004
.checked

.link book Pushing Ice
.url https://www.amazon.com/gp/product/B00NW2Z04E
.date 2005
.checked

.link book Terminal World
.url https://www.amazon.com/gp/product/B01K3LNPCK
.date 2009

.link book Troika
.url https://www.amazon.com/gp/product/B00C89K574
.date 2010
.checked

.link book Sleepover
.url https://www.amazon.com/gp/product/B00OGUTOE8
.date 2010

.link book Slow Bullets
.url https://www.amazon.com/gp/product/B00WGX4KT6
.date 2015
.checked

.link book Permafrost
.url https://www.amazon.com/gp/product/B07HF26D1H
.date 2019


.section links Collections

Reynolds' short stories are like small bite-sized versions of his
novels.  Notably, the stories <em>Zima Blue</em> and <em>Beyond the Aquila Rift</em>
come to life in episodes of the animated series
<a href=https://www.netflix.com/title/80174608>Love, Death & Robots</a>.

.link book Zima Blue
.url https://www.amazon.com/gp/product/B00GVG07DC
.date 2006
.checked

.link book The Six Directions of Space
.url https://www.amazon.com/Six-Directions-Space-Alastair-Reynolds-ebook/dp/B00C89JZCA
.date 2008

.link book Deep Navigation
.url https://www.amazon.com/gp/product/B00XT0V0DY
.date 2010

.link book Beyond the Aquila Rift
.url https://www.amazon.com/gp/product/B01FE7KJ2C
.date 2016
"""
