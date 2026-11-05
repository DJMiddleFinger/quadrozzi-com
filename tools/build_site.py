#!/usr/bin/env python3
"""Build the GBX, Helping Hoof Initiative and Terminals pages (site/gbx/, site/helping-hooves/,
site/terminals/) and the search page (site/news/).

Every page shares one shell: a sidebar listing the site's pages and a breadcrumb bar. The page
tree and copy live in GBX, HHI and TERMINALS below; photo credits come from tools/credits.json.
After editing, run:
    python3 tools/build_site.py

In page bodies, {R} is the site's root folder and {A} the shared assets folder.
"""
import datetime
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
YEAR = datetime.date.today().year
e = html.escape


def plate(src, alt, caption=''):
    cap = f'<figcaption>{caption}</figcaption>' if caption else ''
    return f'<figure class="plate"><img src="{{A}}{src}" alt="{e(alt)}" loading="lazy">{cap}</figure>'


def ticks(*items):
    return '<ul class="ticks">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def book(label, **params):
    """A button to the GBX booking form with options preselected."""
    query = '&amp;'.join(f'{k}={quote(v)}' for k, v in params.items())
    return f'<p><a class="btn" href="{{R}}book/?{query}#form">{label}</a></p>'


def involve(label, kind):
    return f'<p><a class="btn" href="{{R}}get-involved/?type={quote(kind)}#form">{label}</a></p>'


GBX_FORM = '''
      <div class="split" id="form">
        <div class="aside">
          <p><a class="btn" href="{R}../contact/">Contact us</a></p>
          <div class="map">
            <iframe title="Map showing Gowanus Bay Terminal in Red Hook, Brooklyn" loading="lazy" referrerpolicy="no-referrer"
              src="https://www.openstreetmap.org/export/embed.html?bbox=-74.0145%2C40.6645%2C-73.9977%2C40.6745&amp;layer=mapnik&amp;marker=40.66944%2C-74.00611"></iframe>
            <a href="https://www.openstreetmap.org/?mlat=40.66944&amp;mlon=-74.00611#map=16/40.66944/-74.00611" target="_blank" rel="noopener">Open larger map ↗</a>
          </div>
        </div>

        <form class="form" data-inquiry novalidate>
          <fieldset>
            <legend>What are you planning? <span class="req">*</span></legend>
            <div class="chips">
              <label class="chip"><input type="radio" name="type" value="Film / TV" required><span>Film / TV</span></label>
              <label class="chip"><input type="radio" name="type" value="Commercial / Photo"><span>Commercial / Photo</span></label>
              <label class="chip"><input type="radio" name="type" value="Music video"><span>Music video</span></label>
              <label class="chip"><input type="radio" name="type" value="Event"><span>Event</span></label>
              <label class="chip"><input type="radio" name="type" value="Maritime / Leasing"><span>Maritime / Leasing</span></label>
              <label class="chip"><input type="radio" name="type" value="Other"><span>Other</span></label>
            </div>
          </fieldset>

          <div class="form-row">
            <div><label for="f-name">Name <span class="req">*</span></label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
            <div><label for="f-company">Company / production</label><input id="f-company" name="company" type="text" autocomplete="organization"></div>
          </div>
          <div class="form-row">
            <div><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
            <div><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          </div>
          <div class="form-row">
            <div><label for="f-start">Preferred start date</label><input id="f-start" name="start" type="date"></div>
            <div><label for="f-end">End date</label><input id="f-end" name="end" type="date"></div>
          </div>
          <div class="form-row">
            <div>
              <label for="f-size">Crew / guest count</label>
              <select id="f-size" name="size">
                <option value="">Select…</option>
                <option>Under 25</option>
                <option>25–75</option>
                <option>75–150</option>
                <option>150–300</option>
                <option>300+</option>
              </select>
            </div>
            <div><label for="f-hear">How did you hear about GBX?</label><input id="f-hear" name="source" type="text"></div>
          </div>

          <fieldset>
            <legend>Areas of interest</legend>
            <div class="chips">
              <label class="chip"><input type="checkbox" name="areas" value="Grain Terminal exterior"><span>Grain Terminal exterior</span></label>
              <label class="chip"><input type="checkbox" name="areas" value="Industrial details / interiors"><span>Industrial details / interiors</span></label>
              <label class="chip"><input type="checkbox" name="areas" value="Waterfront &amp; piers"><span>Waterfront &amp; piers</span></label>
              <label class="chip"><input type="checkbox" name="areas" value="Open ground / base camp"><span>Open ground / base camp</span></label>
            </div>
          </fieldset>

          <div class="field">
            <label for="f-details">Tell us about the project <span class="req">*</span></label>
            <textarea id="f-details" name="details" required placeholder="Scope, schedule, load-in/out, equipment, anything we should know."></textarea>
          </div>

          <div class="form-foot">
            <button type="submit" class="btn">Send inquiry</button>
            <p class="form-note">Sending opens your email app with the details filled in, addressed to the GBX team.</p>
          </div>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>'''

HHI_FORM = '''
      <div class="split" id="form">
        <div class="aside">
          <p><a class="btn" href="{R}contact/">Contact us</a></p>
          <div class="direct">
            <div><h3>The stable</h3><address>Prospect Park Stable<br>51–55 Caton Place, Brooklyn, NY 11218</address></div>
            <div><a href="https://www.google.com/maps/search/?api=1&amp;query=Prospect+Park+Stable+51+Caton+Place+Brooklyn+NY" target="_blank" rel="noopener">Get directions ↗</a></div>
          </div>
          <p class="nonprofit">Helping Hoof, Inc. is a 501(c)(3) nonprofit organization (EIN 88-3328025). Donations are tax-deductible to the extent allowed by law.</p>
        </div>

        <form class="form" data-inquiry novalidate>
          <fieldset>
            <legend>I’d like to… <span class="req">*</span></legend>
            <div class="chips">
              <label class="chip"><input type="radio" name="type" value="Volunteer" required><span>Volunteer</span></label>
              <label class="chip"><input type="radio" name="type" value="Donate"><span>Donate</span></label>
              <label class="chip"><input type="radio" name="type" value="Partner"><span>Partner</span></label>
              <label class="chip"><input type="radio" name="type" value="Enroll a rider"><span>Enroll a rider</span></label>
              <label class="chip"><input type="radio" name="type" value="Other"><span>Other</span></label>
            </div>
          </fieldset>

          <div class="form-row">
            <div><label for="h-name">Name <span class="req">*</span></label><input id="h-name" name="name" type="text" autocomplete="name" required></div>
            <div><label for="h-org">Organization (optional)</label><input id="h-org" name="organization" type="text" autocomplete="organization"></div>
          </div>
          <div class="form-row">
            <div><label for="h-email">Email <span class="req">*</span></label><input id="h-email" name="email" type="email" autocomplete="email" required></div>
            <div><label for="h-phone">Phone</label><input id="h-phone" name="phone" type="tel" autocomplete="tel"></div>
          </div>

          <div class="field">
            <label for="h-message">How would you like to help? <span class="req">*</span></label>
            <textarea id="h-message" name="message" required placeholder="A few lines about you, your organization or the rider you’d like to enroll."></textarea>
          </div>

          <div class="form-foot">
            <button type="submit" class="btn">Send message</button>
            <p class="form-note">Sending opens your email app with your message filled in.</p>
          </div>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>'''


def inquiry_config(email, subject, extra=''):
    """Where form messages go. endpoint: optional form service URL (e.g. Formspree);
    leave '' to open the visitor's email app instead."""
    return f'''
  <script>
    window.INQUIRY = {{
      email:    '{email}',
      endpoint: '',
      subject:  '{subject}'
    }};{extra}
  </script>'''


DONATE = '''
    // donate: optional online donation page (PayPal, Givebutter, Stripe…). Leave '' and "Donate" opens the form instead.
    const HOOVES = { donate: '' };
    if (HOOVES.donate) {
      document.querySelectorAll('[data-donate]').forEach(function (a) {
        a.href = HOOVES.donate;
        a.target = '_blank';
        a.rel = 'noopener';
      });
    }'''

GBX_LD = '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": ["Place", "LandmarksOrHistoricalBuildings"],
    "name": "GBX — Gowanus Bay Terminal",
    "alternateName": "Red Hook Grain Terminal",
    "geo": { "@type": "GeoCoordinates", "latitude": 40.66944, "longitude": -74.00611 },
    "parentOrganization": { "@type": "Organization", "name": "Quadrozzi" }
  }
  </script>'''

HHI_LD = '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NGO",
    "name": "Helping Hoof, Inc.",
    "alternateName": "Helping Hoof Initiative",
    "nonprofitStatus": "Nonprofit501c3",
    "taxID": "88-3328025"
  }
  </script>'''


def space(anchor, name, thumb, alt, text, area):
    return f'''
      <h2 id="{anchor}">{e(name)}</h2>
      {plate(thumb, alt)}
      <div class="prose"><p>{text}</p></div>
      {book('Ask about this space', areas=area)}'''


def terminal(anchor, label, name, text):
    return f'''
      <h2 id="{anchor}">{e(label)}</h2>
      <p class="lead">{name}</p>
      <div class="prose"><p>{text}</p></div>'''


GBX = dict(
    folder='gbx', name='GBX Gowanus Bay Terminal', short='GBX', tagline='Gowanus Bay Terminal, Red Hook',
    above=[('Quadrozzi', '../')], owner='Quadrozzi', contact='../contact/',
    pages=[
        dict(path='', nav='Overview', h1='Gowanus Bay Terminal', head=GBX_LD,
             title='GBX Gowanus Bay Terminal | Film, events and waterfront in Red Hook',
             desc='GBX Gowanus Bay Terminal: the 1922 Red Hook Grain Terminal and working waterfront in Brooklyn. Book the property for film and TV, photo shoots, events and maritime use.',
             body='''
      <p class="lead">A 1922 grain terminal on the Red Hook waterfront, and today a working maritime site, film location and event venue.</p>
      ''' + plate('gbx/hero.jpg', 'The Red Hook Grain Terminal against a blue sky') + '''
      <dl class="facts">
        <div><dt>1922</dt><dd>Opened September 1</dd></div>
        <div><dt>12</dt><dd>Stories of reinforced concrete</dd></div>
        <div><dt>429 ft</dt><dd>Length of the grain elevator</dd></div>
        <div><dt>46</dt><dd>Acres acquired by the family in 1997</dd></div>
      </dl>
      <h2>Working waterfront</h2>
      <div class="prose">
        <p>Gowanus Bay Terminal, GBX, sits in Red Hook between the mouth of the Gowanus Canal and Erie Basin.</p>
        <p>At its center stands the Red Hook Grain Terminal, the neighborhood’s tallest structure and one of Brooklyn’s most recognizable silhouettes, visible from the Gowanus Expressway and the elevated F and G trains.</p>
        <p>Today GBX is a multi-user maritime and industrial facility. Its piers and yards serve working tenants, while the terminal’s monumental concrete draws filmmakers, photographers, artists and event producers.</p>
        <p>See the <a href="{R}../terminals/">other Quadrozzi terminals</a>.</p>
      </div>
      <p><a class="btn" href="{R}book/">Book the site</a></p>
      ''' + plate('gbx.jpg', 'The rooftop towers of the Red Hook Grain Terminal against a blue sky', 'The Red Hook Grain Terminal, 2025.')),

        dict(path='spaces', nav='Spaces', h1='Spaces',
             desc='The spaces available at GBX Gowanus Bay Terminal: the Grain Terminal, industrial details, open ground, and the waterfront and piers.',
             body='''
      <p class="lead">Raw scale that can’t be built on a stage. Every request is reviewed against terminal operations and safety requirements.</p>''' +
             space('grain-terminal', 'Grain Terminal', 'gbx/towers.jpg', 'Weathered concrete towers of the grain terminal',
                   'Twelve stories of weathered concrete behind a 429-foot façade, built for exteriors, wide shots and large-scale projection.',
                   'Grain Terminal exterior') +
             space('industrial-details', 'Industrial Details', 'gbx/interior-arch.jpg', 'Arched steel-framed windows high on the terminal',
                   'Steel, glass and concrete with nearly a century of texture. Interior access is by site review only.',
                   'Industrial details / interiors') +
             space('open-ground', 'Open Ground', 'gbx/park-view.jpg', 'The full length of the grain terminal seen from across an open field',
                   'Wide, level yard space for staging, base camp, parking and large builds, subject to availability.',
                   'Open ground / base camp') +
             space('waterfront', 'Waterfront & Piers', 'gbx/loujaine.jpg', 'A large ship moored at the terminal pier',
                   'Bay frontage and working piers, with vessels, tugs and the open harbor as a backdrop.',
                   'Waterfront & piers')),

        dict(path='film', nav='Film & Photo', h1='Film & Photo',
             desc='Film, TV, commercial and photo shoots at GBX Gowanus Bay Terminal in Red Hook, Brooklyn.',
             body=plate('heritage-1.jpg', 'Low-angle view of the grain terminal’s concrete tower with graffiti') + '''
      <div class="prose">
        <p>The terminal’s scale and texture have made it a sought-after New York location. It has appeared in music videos for Lorde’s <em>Team</em> and David Bowie’s <em>Valentine’s Day</em>.</p>
        <p>Tell us what the production needs (base camp, parking, power, water access or specific angles) and we’ll confirm what’s available for your dates.</p>
      </div>
      ''' + ticks('Feature film &amp; television', 'Commercials &amp; branded content', 'Music videos',
                  'Editorial &amp; fashion photography', 'Documentary &amp; stills', 'Location scouts')
             + book('Start a film inquiry', type='Film / TV')),

        dict(path='events', nav='Events', h1='Events',
             desc='Private, corporate and cultural events at GBX Gowanus Bay Terminal in Red Hook, Brooklyn.',
             body=plate('hero.jpg', 'The grain terminal seen across the water of Gowanus Bay') + '''
      <div class="prose">
        <p>GBX offers a setting no ballroom can match. In 2002, Zacho Dance Theater staged an aerial performance here: dancers scaled the building while 100-foot video images of Red Hook were projected across its walls.</p>
        <p>From private events to cultural programs, we’ll work with you on a plan that fits the site.</p>
      </div>
      ''' + ticks('Private &amp; corporate events', 'Brand activations &amp; launches',
                  'Performances &amp; installations', 'Community &amp; cultural programs') + '''
      <p class="fineprint">All events are subject to site review, and to the permits and insurance that apply.</p>
      ''' + book('Plan an event', type='Event')),

        dict(path='history', nav='History', h1='History',
             desc='A century of the Red Hook Grain Terminal, from the 1922 Barge Canal era to GBX today.',
             body='''
      <p class="lead">Built by New York State for the Barge Canal era, the terminal has watched a hundred years of the harbor change around it.</p>
      <ol class="timeline">
        <li><span class="yr">1922</span><div><h3>Built by New York State</h3><p>Designed by the Office of the State Engineer to serve the State Barge Canal, the reinforced-concrete grain elevator took 16 months to build, cost $2.5 million and opened on September 1, 1922.</p></div></li>
        <li><span class="yr">1944</span><div><h3>The Port Authority era</h3><p>Control of the terminal passes to the Port Authority of New York and New Jersey.</p></div></li>
        <li><span class="yr">1965</span><div><h3>Grain operations end</h3><p>As grain shipping shifts to other ports, the elevator is deactivated.</p></div></li>
        <li><span class="yr">1997</span><div><h3>The Quadrozzi family</h3><p>John Quadrozzi Sr., president of Quadrozzi Concrete, purchases the terminal and the surrounding 46 acres.</p></div></li>
        <li><span class="yr">2004</span><div><h3>Gowanus Bay Terminal</h3><p>John Quadrozzi Jr. takes the helm and leads the property as Gowanus Bay Terminal, GBX.</p></div></li>
        <li><span class="yr">Today</span><div><h3>A working landmark</h3><p>Maritime and industrial tenants, film and photo productions, and events share one of Brooklyn’s most storied waterfront sites.</p></div></li>
      </ol>
      <div class="gallery">
        <figure><img src="{A}heritage-2.jpg" alt="Archival photo of the grain elevator seen from the northeast" loading="lazy"><figcaption>The grain elevator from the northeast. Historic American Engineering Record.</figcaption></figure>
        <figure><img src="{A}gbx/1922-galleries.jpg" alt="Steel conveyor galleries under construction, 1922" loading="lazy"><figcaption>Conveyor galleries, July 17, 1922.</figcaption></figure>
        <figure><img src="{A}gbx/pier-view.jpg" alt="Archival view southwest from the top of the grain elevator over the terminal pier" loading="lazy"><figcaption>Looking southwest from the elevator. Thomas R. Flagg, HAER.</figcaption></figure>
      </div>'''),

        dict(path='book', nav='Book', h1='Book the site', foot=inquiry_config('info@Quadrozzi.com', 'GBX inquiry'),
             desc='Book GBX Gowanus Bay Terminal for film and photo shoots, events, and maritime or industrial use.',
             body='''
      <p class="lead">Film and photo shoots, events, and maritime or industrial use. Tell us about your project and we’ll reply with availability and next steps.</p>
      <ol class="steps">
        <li><h3>Inquire</h3><p>Send your dates, crew or guest count, and the areas you’re interested in.</p></li>
        <li><h3>Scout</h3><p>We’ll arrange a site visit so your team can walk the property.</p></li>
        <li><h3>Confirm</h3><p>Agree terms and schedule, and provide insurance certificates and any permits that apply.</p></li>
        <li><h3>Arrive</h3><p>We coordinate access on the day around terminal operations.</p></li>
      </ol>''' + GBX_FORM),
    ],
)

HHI = dict(
    folder='helping-hooves', name='Helping Hoof Initiative', short='Helping Hoof Initiative',
    tagline='A program of Helping Hoof, Inc., a 501(c)(3) nonprofit',
    above=[], owner='Helping Hoof, Inc.', contacts=[('', 'info@hhi.horse')], contact='contact/',
    contact_note='Want to volunteer, donate, partner or enroll a rider? <a href="{R}get-involved/">Use the Get involved form</a>. Riding lessons are at Prospect Park Stable, 51–55 Caton Place, Brooklyn, NY 11218.',
    pages=[
        dict(path='', nav='Overview', h1='Helping Hoof Initiative', head=HHI_LD,
             title='Helping Hoof Initiative | Horses and community in Brooklyn',
             desc='Helping Hoof Initiative is a community program for horses and people in Brooklyn: second-career horses, therapeutic riding, youth programs and a greener, horse-friendly Brooklyn. Run by Helping Hoof, Inc., a 501(c)(3) nonprofit.',
             body='''
      <p class="lead">Second careers for horses, and a way into riding for Brooklynites of every background and ability.</p>
      ''' + plate('hooves/hero.jpg', 'Riders on horseback on a tree-lined path in Prospect Park') + '''
      <dl class="facts">
        <div><dt>1917</dt><dd>Prospect Park Stable founded</dd></div>
        <div><dt>2018</dt><dd>Stable restored and renamed</dd></div>
        <div><dt>3.5 mi</dt><dd>Bridle path through Prospect Park</dd></div>
        <div><dt>501(c)(3)</dt><dd>Helping Hoof, Inc. nonprofit</dd></div>
      </dl>
      <h2>Our mission</h2>
      <div class="prose"><p>Helping Hoof Initiative is a community program for horses and people. It is carried out by Helping Hoof, Inc., a 501(c)(3) nonprofit, alongside Be•Brooklyn Equine at Prospect Park Stable. The mission has four parts.</p></div>
      <div class="cards">
        <article class="card"><img src="{A}hooves/second-career.jpg" alt="A child’s hand offering hay to horses through a gate" loading="lazy"><div><h3>Second-career horses</h3><p>Giving horses whose first careers didn’t work out a new start in “healthy, nurturing, loving environments.”</p></div></article>
        <article class="card"><img src="{A}hooves/hands-on.jpg" alt="Close-up of a calm horse in a teal halter" loading="lazy"><div><h3>Therapy &amp; learning</h3><p>Promoting equine-assisted therapy and assisted learning.</p></div></article>
        <article class="card"><img src="{A}hooves.jpg" alt="A young rider in a helmet greeting a horse" loading="lazy"><div><h3>Riding for everyone</h3><p>Making riding accessible to people “with physical, emotional, social, or economic challenges.”</p></div></article>
        <article class="card"><img src="{A}hooves/park-1911.jpg" alt="Archival photo of a tree-lined drive in Prospect Park, 1911" loading="lazy"><div><h3>Safe streets &amp; trails</h3><p>Promoting public infrastructure that lets urban horses live and thrive, safely for horses and people alike.</p></div></article>
      </div>
      <p class="source-note">Mission as published by Helping Hoof (<a href="https://www.6sqft.com/where-to-go-horseback-riding-in-nyc/" target="_blank" rel="noopener">6sqft, 2023</a>).</p>
      <p><a class="btn" href="{R}get-involved/">Get involved</a></p>'''),

        dict(path='programs', nav='Programs', h1='Programs',
             desc='Second-career horses, therapeutic riding, youth programs and community work from Helping Hoof Initiative.',
             body='''
      <p class="lead">From the riding ring to Red Hook’s community gardens, the work reaches well beyond the barn.</p>
      <h2>Second-career horses</h2>
      <div class="prose"><p>Many of the stable’s horses didn’t work out in their first jobs and were resold or rehomed before arriving in Brooklyn. With retraining, focused healthcare and plenty of time with other horses and the people who care for them, each one finds a role that suits its mind and body.</p></div>
      <blockquote>Some become loyal student horses, some trusty trail horses, and most enjoy both jobs.<cite>Program Director, Be•Brooklyn Equine</cite></blockquote>
      <h2>Therapeutic riding</h2>
      ''' + plate('hooves/therapy-riding.jpg', 'A horse and handlers during a therapeutic riding session on Prospect Park’s Bowling Green') + '''
      <div class="prose"><p>In 2019, Prospect Park Stable began providing horses to GallopNYC, the New York therapeutic riding nonprofit, for sessions on Prospect Park’s Bowling Green. The horses had a month of specialized training to prepare for the program, which serves children and adults with disabilities, including autism.</p></div>
      ''' + involve('Partner with us', 'Partner') + '''
      <h2>Youth programs</h2>
      ''' + plate('hooves/youth.jpg', 'A young rider on a pony led by stable staff') + '''
      <div class="prose">
        <p>In the summer immersion program, riders ages 6 to 15 spend the whole day at the stable. They get their horse ready, ride in the park, and then learn a different part of horse history, behavior and healthcare each week.</p>
        <p>After-school and weekend programs teach both riding and complete horse care, from grooming to groundwork.</p>
      </div>
      <p><a class="btn" href="https://DJMiddleFinger.github.io/be-brooklyn-equine/" target="_blank" rel="noopener">Enroll with Brooklyn Equine ↗</a></p>
      <h2>In the community</h2>
      <div class="cards">
        <article class="card"><img src="{A}hooves/garden.jpg" alt="A brick path through a Brooklyn community garden with red tulips" loading="lazy"><div><h3>From stable to garden</h3><p>Since 2019 the stable’s manure has been composted in Red Hook, under the mentorship of the nonprofit Red Hook Farms, and given to Red Hook community gardens. Bedding comes from wood shavings donated by local Brooklyn woodworkers.</p></div></article>
        <article class="card"><img src="{A}hooves/horse-tamers.jpg" alt="The Horse Tamers sculptures at Park Circle, Prospect Park" loading="lazy"><div><h3>The horse parade returns</h3><p>In June 2019 the Prospect Park Equine Rally rode from the Horse Tamers statues along the Bridle Path to the riding circle known as “the Q.” It was Brooklyn’s first equestrian parade since the 1930s, with free pony rides for kids.</p></div></article>
        <article class="card card--plain"><div><h3>Neighbors in need</h3><p>In May 2020, during the pandemic, stable horses pulled carts delivering food and supplies in Red Hook, with stops at Red Hook Farm, Red Hook Houses and the Joseph Miccio Community Center.</p></div></article>
      </div>'''),

        dict(path='heritage', nav='Heritage', h1='Heritage',
             desc='Prospect Park was designed with a bridle path, and Brooklyn once held horse parades hundreds strong.',
             body='''
      <p class="lead">Prospect Park was designed with a bridle path, and Brooklyn once held horse parades hundreds strong. Helping Hoof Initiative carries that tradition forward.</p>
      <ol class="timeline">
        <li><span class="yr">1917</span><div><h3>Prospect Park Stable</h3><p>Prospect Park Stable is founded. It’s the name the stable would get back a century later.</p></div></li>
        <li><span class="yr">1935</span><div><h3>A parade hundreds strong</h3><p>A parade sponsored by the Brooklyn Daily Eagle and the ASPCA draws 252 horses, some 500 dogs, and a goat pulling a cart.</p></div></li>
        <li><span class="yr">2018</span><div><h3>A name restored</h3><p>The former Kensington Stables changes hands and gets back its 1917 name, Prospect Park Stable.</p></div></li>
        <li><span class="yr">2019</span><div><h3>Back in the park</h3><p>The Equine Rally revives Brooklyn’s horse parade, compost from the stable reaches Red Hook’s gardens, and the GallopNYC therapeutic riding partnership begins.</p></div></li>
        <li><span class="yr">2020</span><div><h3>Neighbors &amp; new riders</h3><p>Horse-drawn deliveries reach Red Hook neighbors during the pandemic, and young riders fill the summer immersion program.</p></div></li>
        <li><span class="yr">Today</span><div><h3>Helping Hoof Initiative</h3><p>Helping Hoof, Inc., a registered 501(c)(3) nonprofit, carries the mission forward alongside Be•Brooklyn Equine.</p></div></li>
      </ol>
      <div class="gallery">
        <figure><img src="{A}hooves/wallabout.jpg" alt="Archival photo of trucks and horse-drawn carts crowding Brooklyn’s Wallabout Market" loading="lazy"><figcaption>Trucks and horse-drawn carts at Brooklyn’s Wallabout Market, 1940. Library of Congress.</figcaption></figure>
        <figure><img src="{A}hooves/stable.jpg" alt="Riders on horseback outside the stable on Caton Place" loading="lazy"><figcaption>The stable on Caton Place, then called Kensington Stables, in 2011.</figcaption></figure>
      </div>'''),

        dict(path='get-involved', nav='Get Involved', h1='Get involved',
             foot=inquiry_config('info@hhi.horse', 'Helping Hoof Initiative', DONATE),
             desc='Volunteer, donate, partner with or enroll a rider in Helping Hoof Initiative.',
             body='''
      <p class="lead">Volunteer, donate, partner, or enroll a rider. Choose how you’d like to help and tell us a little about yourself.</p>
      <nav class="levers" aria-label="Ways to help">
        <a class="lever" href="./?type=Volunteer#form"><span><b>Volunteer</b><small>Lend a hand at the stable or at community events.</small></span></a>
        <a class="lever" href="./?type=Donate#form" data-donate><span><b>Donate</b><small>Support second-career horses and access to riding.</small></span></a>
        <a class="lever" href="./?type=Partner#form"><span><b>Partner</b><small>Schools, therapy programs and community gardens.</small></span></a>
        <a class="lever" href="https://DJMiddleFinger.github.io/be-brooklyn-equine/" target="_blank" rel="noopener"><span><b>Ride &amp; learn ↗</b><small>Lessons, trail rides and youth programs with Be•Brooklyn Equine.</small></span></a>
      </nav>''' + HHI_FORM),
    ],
)

# anchor, label, name, text
TERMINAL_ROWS = [
    ('gbx', 'GBX', 'Gowanus Bay Terminal',
     'In Red Hook, between the mouth of the Gowanus Canal and Erie Basin. <a href="{R}../gbx/">Visit the GBX site</a>.'),
    ('bbx', 'BBX', 'Barbadoes Basin Terminal',
     'On Jamaica Bay at Rockaway Beach. Once home to the famed Brooklyn Day Camp.'),
    ('vbx', 'VBX', 'Vernam Basin Terminal',
     'On Jamaica Bay, across from the Barbadoes Basin Reserve, with open bay, bridge and Manhattan views.'),
    ('gcx', 'GCX', 'Gowanus Canal Terminal',
     'On the Gowanus Canal, beneath the elevated Smith–9th Streets subway station. It appears in a scene from <em>Goodfellas</em>.'),
    ('ncx', 'NCX', 'Newtown Creek Terminal',
     'In Long Island City, along the LIRR tracks, with a large bulk silo for cement and fly ash.'),
    ('cicx', 'CICX', 'Coney Island Creek Terminal',
     'The first property you see entering Coney Island, marked by its tall coal silos.'),
    ('metropolitan-ave', 'Metropolitan Ave', 'Ridgewood, Queens',
     '3.69 acres along Newtown Creek, ready for almost anything.'),
]

TERMINALS = dict(
    folder='terminals', name='Quadrozzi Terminals', short='Terminals', tagline='Waterfront terminals in Brooklyn and Queens',
    above=[('Quadrozzi', '../')], owner='Quadrozzi', contact='../contact/',
    side_links=[(label, f'#{anchor}') for anchor, label, _, _ in TERMINAL_ROWS],
    pages=[
        dict(path='', nav='Overview', h1='Terminals', title='Terminals | Quadrozzi',
             desc='The Quadrozzi waterfront terminals in Brooklyn and Queens.',
             body='''
      <p class="lead">In 2013, Quadrozzi Enterprises represented seven multi-user waterfront terminals in Brooklyn and Queens: more than 30 acres of industrial land, with “an emphasis on sustainability &amp; community.”</p>''' + ''.join(terminal(*row) for row in TERMINAL_ROWS) + '''
      <h2>Land &amp; sea</h2>
      <div class="prose"><p>With decades of sea-freight experience, Quadrozzi representatives moved bulk cargo from Europe, South America and Mexico up the Eastern Seaboard into New York. On land, trucking skills passed down through generations moved concrete, sand and stone, rubble, rock salt, bulk powders and specialty equipment throughout the city.</p></div>
      <h2>After Sandy</h2>
      <div class="prose"><p>After Hurricane Sandy in 2012, the company called for rebuilding smarter in flood zones: keep living space and mechanicals above the flood plain, build with concrete for strength and fire resistance, and replace wooden boardwalks with concrete ones that double as sea walls.</p></div>
      <h2>Our approach</h2>
      <blockquote>We do not promote our name using persuasive language or trickery, but rather use our natural creative talents and diverse experience in finding the simplest solutions to each objective.<cite>Quadrozzi Enterprises, 2013</cite></blockquote>'''),
    ],
)



def build(site, credits):
    pages = list(site['pages'])
    if 'contacts' in site:
        pages.append(contact_page(site))
    has_credits = site is not TERMINALS  # the terminals page has no photos
    if has_credits:
        pages.append(credits_page(site, credits))

    for page in pages:
        path = page['path']
        R = '../' if path else ''
        A = R + '../assets/'

        def href(target):
            return R + target + '/' if target else (R or './')

        side = []
        for p in pages:
            if p['path'] in ('contact', 'credits'):
                continue
            attr = ' aria-current="page"' if p['path'] == path else ''
            side.append(f'        <li><a href="{href(p["path"])}"{attr}>{e(p["nav"])}</a></li>')
        side += [f'        <li><a href="{link}">{e(label)}</a></li>' for label, link in site.get('side_links', [])]

        trail = [(label, R + link) for label, link in site['above']] + [(site['short'], href(''))]
        if path:
            trail.append((page['nav'], href(path)))
        crumbs = ''.join(f'<li><a href="{link}">{e(label)}</a></li>' for label, link in trail[:-1])
        crumbs += f'<li><span aria-current="page">{e(trail[-1][0])}</span></li>'

        photo_credits = f'\n      <a href="{href("credits")}">Photo credits</a>' if has_credits else ''
        body = page['body'].replace('{R}', R).replace('{A}', A)

        title = page.get('title') or f'{page["h1"]} | {site["name"]}'
        out = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)}</title>
  <meta name="description" content="{e(page['desc'])}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(page['desc'])}">
  <meta name="theme-color" content="#161616">
  <link rel="preconnect" href="https://api.fontshare.com">
  <link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,401,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{A}css/site.css">{page.get('head', '')}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="sidebar" aria-label="Open menu"><i></i><i></i><i></i><i></i></button>
  <aside class="sidebar" id="sidebar" aria-label="{e(site['name'])}">
    <a class="side-brand" href="{href('')}">{e(site['short'])}<small>{e(site['tagline'])}</small></a>
    <nav aria-label="Pages">
      <ul class="side-nav">
{chr(10).join(side)}
      </ul>
    </nav>
  </aside>
  <div class="content" id="content">
    <header class="bar">
      <nav class="crumbs" aria-label="Breadcrumb"><ol>{crumbs}</ol></nav>
    </header>
    <main class="page" id="main">
      <h1>{e(page['h1'])}</h1>{body}
    </main>
    <footer class="page-foot">
      <a class="btn" href="{R}{site['contact']}">Contact us</a>{photo_credits}
      <span>© {YEAR} {e(site['owner'])}</span>
    </footer>
  </div>{page.get('foot', '')}
  <script src="{A}js/site.js"></script>
</body>
</html>
'''
        target = ROOT / 'site' / site['folder'] / path / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out, encoding='utf-8')
    print(f'Wrote {len(pages)} pages to site/{site["folder"]}/')


def display_title(title):
    stem, dot, ext = title.rpartition('.')
    return stem if dot and ext.lower() in ('jpg', 'jpeg', 'png', 'tif', 'tiff') else title


def contact_page(site):
    # The only place a site lists its email addresses; every Contact us button leads here.
    # contacts: (heading, email) pairs. The unheaded one is the site's main address, shown large;
    # headed ones are smaller and sit lower, under .more.
    main = ''.join(f'<p class="main-email"><a href="mailto:{m}">{m}</a></p>' for h, m in site['contacts'] if not h)
    more = ''.join(f'<div><h2>{e(h)}</h2><a href="mailto:{m}">{m}</a></div>' for h, m in site['contacts'] if h)
    more = f'\n      <div class="more">{more}</div>' if more else ''
    return dict(path='contact', nav='Contact', h1='Contact us',
                desc=f'How to reach {site["name"]}.',
                body=f'''
      {main}
      <div class="prose"><p>{site["contact_note"]}</p></div>{more}''')


def credits_page(site, credits):
    # Photos with "hooves" in their path belong to Helping Hoof Initiative site.
    mine = [c for c in credits if ('hooves' in c['file']) == (site is HHI)]
    rows = []
    for c in mine:
        lic = (f'<a href="{e(c["license_url"])}" target="_blank" rel="noopener">{e(c["license"])}</a>'
               if c.get('license_url') else e(c['license']))
        byline = lic if c['license'].startswith('Courtesy') else f'By {e(c["artist"])}, {lic}'
        rows.append(f'''
        <li class="credit">
          <img src="{{A}}{e(c["file"].removeprefix("assets/"))}" alt="" loading="lazy">
          <div>
            <p class="used">{e(c["used"])}</p>
            <h3><a href="{e(c["source"])}" target="_blank" rel="noopener">{e(display_title(c["title"]))}</a></h3>
            <p>{byline}</p>
          </div>
        </li>''')
    return dict(path='credits', nav='Photo credits', h1='Photo credits',
                desc='Photo credits and licenses for images used on this site.',
                body=f'''
      <p class="lead">Most photographs on this site come from Wikimedia Commons and are used under the licenses listed below. Public-domain images are courtesy of the Library of Congress and other collections. Select a title to see the original file and its full license.</p>
      <ul class="credit-list">{"".join(rows)}
      </ul>''')


COMPANIES = ['BBX™', 'GBX™', 'VBX™', 'PPS▪Prospect Park Stable™', 'Quadro▪cem™', 'Quadrozzi™Concrete', 'Quadro▪salt™',
             'Quadrozzi™Studios', 'Quadro▪trax™', 'Quadrozzi™disegno', 'Be™•Brooklyn equine™', 'hhi™•helpinghoof initiative']
CATEGORIES = ['Industrial', 'Commercial', 'Residential', 'Cement & cementitious materials', 'Concrete', 'Rock salt', 'Studios',
              'Transportation', 'Design', 'Horse care & riding', 'Equine', 'Environmental', 'Arts • Theater • Film']
TYPES = ['News', 'Sponsorship', 'Special']


def options(values):
    return ''.join(f'<option>{e(v)}</option>' for v in values)


def build_news():
    # The searchable page; its entries are in site/assets/data/news.json and the search is assets/js/lists.js.
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>In the News | Quadrozzi</title>
  <meta name="description" content="News, sponsorships and more from Quadrozzi, searchable by type, date, organization, category and company.">
  <meta name="theme-color" content="#ffe641">
  <link rel="preconnect" href="https://api.fontshare.com">
  <link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,401,500,700,900&display=swap" rel="stylesheet">
  <style>
    :root {{ --yellow: #ffe641; --smoke: #161616; --hazard: repeating-linear-gradient(-45deg, #f6d31c 0 14px, #161616 14px 28px); }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      min-height: 100svh; padding: 4rem 16px;
      background: var(--yellow); color: var(--smoke); font-family: 'Satoshi', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    }}
    body::before, body::after {{ content: ''; position: fixed; z-index: 1; left: 0; right: 0; height: 14px; background: var(--hazard); }}
    body::before {{ top: 0; }}
    body::after {{ bottom: 0; }}
    main {{ width: min(60rem, 100%); margin: 0 auto; }}
    h1 {{ font-weight: 900; text-transform: uppercase; letter-spacing: -.02em; font-size: clamp(2.6rem, 10vw, 6.5rem); line-height: .95; margin-bottom: 2rem; overflow-wrap: anywhere; }}
    a {{ color: inherit; }}
    a:focus-visible, input:focus-visible, select:focus-visible, button:focus-visible {{ outline: 3px solid var(--smoke); outline-offset: 2px; }}

    form {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr)); gap: 1rem; align-items: end; }}
    label {{ display: grid; gap: .3rem; font-size: .85rem; font-weight: 700; }}
    input, select, button {{ width: 100%; min-height: 2.75rem; padding: .5rem .6rem; font: inherit; font-weight: 500; font-size: 1rem; color: inherit; background: #fff; border: 2px solid var(--smoke); border-radius: 0; }}
    button {{ background: none; font-weight: 700; cursor: pointer; }}
    button:hover {{ background: var(--smoke); color: var(--yellow); }}

    #status:not(:empty) {{ margin-top: 2.5rem; font-size: 1.25rem; font-weight: 700; }}
    #results {{ list-style: none; margin-top: 2.5rem; border-top: 2px solid var(--smoke); }}
    #results:empty {{ display: none; }}
    #results li {{ padding: 1rem 0; border-bottom: 1px solid var(--smoke); }}
    #results b {{ display: block; font-weight: 900; font-size: 1.25rem; line-height: 1.25; overflow-wrap: anywhere; }}
    #results small {{ display: block; margin-top: .3rem; font-size: .95rem; }}

    .back {{ display: inline-block; margin-top: 3rem; padding: .9rem 1.6rem; background: var(--smoke); color: var(--yellow); text-decoration: none; font-weight: 700; }}
    .back:hover {{ background: #000; }}
  </style>
</head>
<body>
  <main>
    <h1>In the News</h1>
    <form id="filters" data-src="../assets/data/news.json" aria-label="Search news, sponsorships and more">
      <label>Type <select name="type"><option value="">All</option>{options(TYPES)}</select></label>
      <label>From <input type="date" name="from"></label>
      <label>To <input type="date" name="to"></label>
      <label>Organization <select name="name"><option value="">All</option></select></label>
      <label>Category <select name="category"><option value="">All</option>{options(CATEGORIES)}</select></label>
      <label>Company <select name="company"><option value="">All</option>{options(COMPANIES)}</select></label>
      <button type="reset">Clear</button>
    </form>
    <p id="status" role="status"></p>
    <ul id="results"></ul>
    <a class="back" href="../">Back to Quadrozzi</a>
  </main>
  <script src="../assets/js/lists.js"></script>
</body>
</html>
'''
    target = ROOT / 'site' / 'news' / 'index.html'
    target.parent.mkdir(exist_ok=True)
    target.write_text(out, encoding='utf-8')
    print('Wrote the news page')


if __name__ == '__main__':
    all_credits = json.loads((ROOT / 'tools' / 'credits.json').read_text(encoding='utf-8'))
    for s in (GBX, HHI, TERMINALS):
        build(s, all_credits)
    build_news()
