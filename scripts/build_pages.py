"""Run from preview-colors/:  python3 ../scripts/build_pages.py
Builds city pages, resources, articles, and updates shared chrome for Cedric's site.
Run from the site folder (preview-colors). Idempotent on the generated pages;
existing pages are patched once (guarded by markers)."""
import json, re, pathlib

SITE = "https://www.cedriccollinslaw.com/"
PHONE_TEL = "+17408808510"
PHONE = "(740) 880&#8202;8510"
ADDR = "38 East Columbus St., Suite 201 · Pickerington, OH 43147"
WIDGET = "<!-- GHL chat + voice widget: paste the GoHighLevel embed snippet here. Keep the bottom-right corner free of other fixed elements. -->"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
 '<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />\n'
 '<link rel="stylesheet" href="styles.css" />')

CITIES = [
 ("pickerington", "Pickerington"), ("reynoldsburg", "Reynoldsburg"),
 ("gahanna", "Gahanna"), ("canal-winchester", "Canal Winchester")]

def city_file(slug): return f"{slug}-family-law-attorney.html"

NAV = [("index.html","Home"),("about.html","About"),("divorce.html","Divorce"),
       ("child-custody.html","Child Custody"),("resources.html","Resources"),("contact.html","Contact")]

def header(active):
    links = "".join(f'<a class="lk{" active" if h==active else ""}" href="{h}">{t}</a>' for h,t in NAV)
    return f'''<a href="#main" class="skip">Skip to content</a>
<header>
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="Cedric P. Collins, Attorney at Law, home"><span class="seal" aria-hidden="true">C</span><span><b>Cedric P. Collins</b><span class="role">Attorney at Law</span></span></a>
    <input type="checkbox" id="burger" class="burger" hidden />
    <nav class="menu" aria-label="Primary">
      {links}
    </nav>
    <div class="nav-cta"><a class="phone" href="tel:{PHONE_TEL}">{PHONE}</a><a class="btn btn-brass" href="contact.html"><span class="lg">Free Consultation</span><span class="sm">Free Consult</span></a><label for="burger" class="burger-lbl" aria-label="Toggle menu"><span></span><span></span><span></span></label></div>
  </div>
</header>'''

AREAS_COL = '<div class="foot-col"><h4>Areas We Serve</h4>' + "".join(
    f'<a href="{city_file(s)}">{n}</a>' for s,n in CITIES) + '</div>'

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="fb"><b>Law Office of Cedric P. Collins, LLC</b><p>A divorce and family law practice helping Central Ohio families move forward with clarity and a steady advocate in their corner.</p></div>
      <div class="foot-col"><h4>Practice</h4><a href="divorce.html">Divorce &amp; Dissolution</a><a href="child-custody.html">Child Custody</a><a href="about.html">About Cedric</a><a href="resources.html">Resources</a><a href="contact.html">Contact</a></div>
      {AREAS_COL}
      <div class="foot-col"><h4>Office</h4><a href="tel:{PHONE_TEL}">{PHONE}</a><a href="https://maps.google.com/?q=38+East+Columbus+St,+Pickerington,+OH+43147" target="_blank" rel="noopener">38 E. Columbus St., Ste 201<br>Pickerington, OH 43147</a></div>
    </div>
    <div class="foot-bottom"><span>&copy; 2026 Law Office of Cedric P. Collins, LLC</span><span>Serving Columbus &amp; Central Ohio</span></div>
    <p class="disc">The information on this website is for general purposes only and does not constitute legal advice. Viewing this site or contacting the firm does not create an attorney client relationship. Prior results do not guarantee a similar outcome.</p>
  </div>
</footer>
<script src="shared.js"></script>
{WIDGET}
</body>
</html>
'''

def consult(h2='Your first conversation is <em>free.</em>',
            p='Tell Cedric what you are facing. You will leave knowing where you stand and what your options are, with no pressure to commit.'):
    return f'''<section class="block" style="padding-top:0">
  <div class="wrap">
    <div class="consult rv"><div class="consult-in">
      <div><h2>{h2}</h2><p>{p}</p><p class="addr">{ADDR}</p></div>
      <div class="actions"><a class="btn btn-brass" href="contact.html">Book a free consult</a><a class="btn btn-ghost" style="color:#e5ded2;border-color:rgba(229,222,210,.3)" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
    </div></div>
  </div>
</section>'''

# Newsletter posts to a placeholder until the GHL form/webhook exists.
NEWS = '''<section class="block" style="padding-top:0" aria-labelledby="nl">
  <div class="wrap">
    <div class="news rv">
      <div><p class="label" style="color:var(--slate-lt)">The monthly note</p><h2 id="nl">Plain answers for <em>Ohio families,</em> once a month.</h2><p>One short email from Cedric each month: what is changing in Ohio family law, questions parents are asking, and practical steps you can take. No spam, unsubscribe any time.</p></div>
      <!-- Newsletter: swap action for the GHL form or webhook once GHL is set up -->
      <form action="https://formspree.io/f/REPLACE_WITH_NEWSLETTER_FORM_ID" method="POST">
        <input type="hidden" name="list" value="newsletter" />
        <label class="sr" for="nl-name" style="position:absolute;left:-9999px">First name</label>
        <input id="nl-name" type="text" name="first_name" placeholder="First name" autocomplete="given-name" />
        <label for="nl-email" style="position:absolute;left:-9999px">Email</label>
        <input id="nl-email" type="email" name="email" placeholder="Email address" autocomplete="email" required />
        <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true" />
        <button class="btn btn-brass" type="submit">Send me the monthly note</button>
        <small>Subscribing does not create an attorney client relationship.</small>
      </form>
    </div>
  </div>
</section>'''

def head(title, desc, path, schemas, og_img="og-image.jpg"):
    s = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False)}\n</script>' for x in schemas)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{SITE}{path}" />
<meta name="robots" content="noindex" />
<meta name="theme-color" content="#142841" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{SITE}{path}" />
<meta property="og:image" content="{SITE}{og_img}" />
<meta name="twitter:card" content="summary_large_image" />
{s}
{FONTS}
</head>
<body>'''

def crumbs(*items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":SITE+p} for i,(n,p) in enumerate(items)]}

def faq_schema(qas):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in qas]}

def faq_html(qas, hid):
    rows = "\n".join(f'      <details{" open" if i==0 else ""}><summary>{q}<span class="pm" aria-hidden="true">+</span></summary><p>{a}</p></details>' for i,(q,a) in enumerate(qas))
    return rows

# ---------------------------------------------------------------- courts
FRANKLIN = ("Franklin County Court of Common Pleas, Division of Domestic Relations and Juvenile Branch",
            "373 South High Street, Columbus, OH 43215. Divorce and dissolution are heard by the Domestic Relations division; custody and support between unmarried parents go to the Juvenile division in the same building.")
FAIRFIELD = ("Fairfield County Court of Common Pleas, Domestic Relations Division",
             "Hall of Justice, 224 East Main Street, Lancaster, OH 43130. Custody matters between unmarried parents are handled by the Fairfield County Juvenile Court, also in the Hall of Justice.")
LICKING = ("Licking County Court of Common Pleas, Domestic Relations Court",
           "75 East Main Street, Newark, OH 43055. Hears divorce and dissolution, and paternity matters with related custody questions.")

CITY = {
 "pickerington": dict(
   counties="Fairfield and Franklin Counties", courts=[FAIRFIELD, FRANKLIN], img="img/neighborhood.jpg",
   h1='A Pickerington family lawyer who is <em>right here</em> in town.',
   sub="Cedric&rsquo;s office is on East Columbus Street in Pickerington. If you live here, your attorney is a short drive away, and you can sit across the table from him instead of sending emails into the dark.",
   intro=["Most of Pickerington sits in Fairfield County, with a smaller piece in Franklin County. That detail matters more than people expect: the county you live in decides which court hears your divorce or custody case, which local rules apply, and how long things tend to take.",
          "Cedric helps Pickerington parents with divorce and dissolution, custody and parenting time, child support, and changes to orders that no longer fit. Many families here have children in school, so parenting schedules get built around the school year, activities, and the real rhythm of your week, not a template."],
   faqs=[("Which court handles a Pickerington divorce?", "It depends on which side of the county line your home is on. Most Pickerington addresses are in Fairfield County, so the case is filed with the Fairfield County Domestic Relations Division in Lancaster. Homes in the Franklin County portion file in Columbus. Your property tax bill shows your county, or Cedric can confirm it at your free consult."),
         ("Can I meet with Cedric in person in Pickerington?", "Yes. The office is at 38 East Columbus Street, Suite 201, in Pickerington. Virtual consultations are available too if that is easier for your schedule."),
         ("I just moved to Pickerington. Can I file for divorce here?", "Ohio requires that you have lived in the state for at least six months before filing for divorce, and you generally file in a county where you or your spouse has lived for at least 90 days. If you moved recently, Cedric will walk you through your timing.")]),
 "reynoldsburg": dict(
   counties="Franklin, Fairfield, and Licking Counties", courts=[FRANKLIN, FAIRFIELD, LICKING], img="img/kids-playing.jpg",
   h1='Reynoldsburg family law, across <em>all three</em> of its counties.',
   sub="Reynoldsburg is one of the few cities in Central Ohio that crosses three county lines. Cedric practices in all three, so your case starts in the right court from day one.",
   intro=["Reynoldsburg spans Franklin, Fairfield, and Licking Counties. Two neighbors on the same side of town can end up in two different courthouses, with different local rules, forms, and schedules. Filing in the wrong place costs time, and in a custody matter time is something your family does not have to spare.",
          "Cedric represents Reynoldsburg parents in divorce and dissolution, custody and shared parenting, child support, and post decree changes. He also serves as a court appointed Guardian ad Litem, so he understands how courts look at what is genuinely best for a child."],
   faqs=[("How do I know which county my Reynoldsburg home is in?", "Check your property tax bill or the county auditor website for your address. Most of Reynoldsburg is in Franklin County, with parts in Fairfield and Licking Counties. Cedric will confirm it during your free consult."),
         ("Does it matter which county my case is in?", "Yes. Each county has its own domestic relations court, local rules, forms, and scheduling. Starting in the correct court avoids delays and refiling."),
         ("Can you help if my ex lives in a different county?", "Yes. Cedric practices in Franklin, Fairfield, and Licking Counties, which covers the most common situations for Reynoldsburg families. Where a case is filed depends on residency and on where any existing orders were issued.")]),
 "gahanna": dict(
   counties="Franklin County", courts=[FRANKLIN], img="img/coparent.jpg",
   h1='A Gahanna divorce and custody lawyer who <em>keeps it human.</em>',
   sub="Gahanna families file in Franklin County, one of the busiest family court systems in Ohio. You deserve an attorney who keeps you informed and prepared at every step.",
   intro=["Gahanna is in Franklin County, so divorce, dissolution, and custody cases are heard downtown at the Franklin County Court of Common Pleas, Division of Domestic Relations and Juvenile Branch. It is a large, busy court. Being organized, on time, and prepared for each hearing makes a real difference in how your case moves.",
          "Cedric helps Gahanna parents with divorce and dissolution, custody for married and unmarried parents, parenting time, child support, and modifications. As a court appointed Guardian ad Litem in Franklin County, he has seen these cases from the side of the child, and he brings that perspective to every family he represents."],
   faqs=[("Where is a Gahanna divorce filed?", "Gahanna is in Franklin County, so divorce and dissolution cases are filed with the Franklin County Court of Common Pleas, Division of Domestic Relations, at 373 South High Street in Columbus."),
         ("We were never married. Where does our custody case go?", "In Franklin County, custody, parenting time, and support between unmarried parents are handled by the Juvenile division, in the same building as the Domestic Relations court."),
         ("How long does a Franklin County divorce take?", "An agreed dissolution can often finish within a few months. A contested divorce with custody or property disputes takes longer. Cedric will give you a realistic timeline for your situation at the free consult.")]),
 "canal-winchester": dict(
   counties="Franklin and Fairfield Counties", courts=[FRANKLIN, FAIRFIELD], img="img/hero-family.jpg",
   h1='Canal Winchester family law, from an attorney <em>next door.</em>',
   sub="Canal Winchester sits between Franklin and Fairfield Counties, minutes from Cedric&rsquo;s Pickerington office. Practical help for divorce, dissolution, and custody, close to home.",
   intro=["Canal Winchester is split between Franklin County and Fairfield County, so the court that hears your case depends on where your home sits. Franklin County cases are heard in downtown Columbus; Fairfield County cases are heard in Lancaster. Cedric practices in both.",
          "Canal Winchester has grown fast, and many families here are young: new homes, young kids, two working parents. Cedric helps with divorce and dissolution, custody and parenting time, child support, and agreements that are built to work for a busy family for years, not just for the day they are signed."],
   faqs=[("Which court hears a Canal Winchester custody case?", "It depends on the county your home is in. Franklin County cases go to the Domestic Relations and Juvenile Branch in Columbus. Fairfield County cases go to the Hall of Justice in Lancaster. Cedric will confirm your county at the free consult."),
         ("Is Cedric&rsquo;s office close to Canal Winchester?", "Yes. The office is in Pickerington, a short drive north. In person and virtual consultations are both available."),
         ("Can a dissolution work if we both agree?", "Often, yes. A dissolution is a no fault process where both spouses agree on every term before filing. Ohio holds the final hearing 30 to 90 days after filing. It is usually faster and less costly than a contested divorce.")]),
}

def build_city(slug, name):
    c = CITY[slug]; path = city_file(slug)
    schemas = [
      {"@context":"https://schema.org","@type":["Attorney","LegalService"],"name":"Law Office of Cedric P. Collins, LLC",
       "url":SITE+path,"telephone":"+1-740-880-8510",
       "address":{"@type":"PostalAddress","streetAddress":"38 East Columbus St., Suite 201","addressLocality":"Pickerington","addressRegion":"OH","postalCode":"43147","addressCountry":"US"},
       "areaServed":{"@type":"City","name":f"{name}, Ohio"},
       "knowsAbout":["Divorce","Dissolution of marriage","Child custody","Shared parenting","Child support","Post decree modification"]},
      crumbs(("Home",""),(f"{name} Family Law",path)), faq_schema(c["faqs"])]
    others = ", ".join(f'<a href="{city_file(s)}" style="color:var(--brass);font-weight:600">{n}</a>' for s,n in CITIES if s!=slug)
    courts = "".join(f'<div class="court"><b>{a}</b><span>{b}</span></div>' for a,b in c["courts"])
    intro = "".join(f"<p>{p}</p>" for p in c["intro"])
    html = head(f"{name} Divorce &amp; Custody Lawyer | Cedric P. Collins",
                f"Divorce, dissolution, and child custody help for {name}, Ohio families in {c['counties'].replace(' and ',' and ')}. Free, confidential consultation with attorney Cedric P. Collins.",
                path, schemas)
    html += "\n" + header("") + f'''

<main id="main">
<section class="page-hero">
  <div class="wrap hero-split">
    <div>
      <p class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <span>{name}</span></p>
      <h1 class="page-h">{c["h1"]}</h1>
      <p class="sub">{c["sub"]}</p>
      <div class="hero-actions"><a class="btn btn-brass" href="contact.html">Book a free consult</a><a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
    </div>
    <div class="ph-img rv"><img src="{c["img"]}" alt="A family spending time together outdoors in Central Ohio" loading="eager" /></div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="prose narrow rv">
      <h2>Family law for {name}, in {c["counties"]}</h2>
      {intro}
      <ul>
        <li><span><a href="divorce.html">Divorce and dissolution</a>, including property, debt, and spousal support</span></li>
        <li><span><a href="child-custody.html">Custody, shared parenting, and parenting time</a>, for married and unmarried parents</span></li>
        <li>Child support, and changes to orders after the divorce is final</li>
        <li>Third party and grandparent custody questions</li>
      </ul>
    </div>
  </div>
</section>

<section class="block" style="padding-top:0" aria-labelledby="ct">
  <div class="wrap">
    <div class="sec-head rv"><span class="sec-num" aria-hidden="true">&mdash;</span><h2 id="ct">Where a {name} case <em>is heard.</em></h2></div>
    <p class="county-note rv">Your county decides your court. Not sure which county your home is in? Your property tax bill will tell you, or Cedric can confirm it at your free consult.</p>
    <div class="courts rv">{courts}</div>
  </div>
</section>

<section class="block" style="padding-top:0" aria-labelledby="fq">
  <div class="wrap">
    <div class="sec-head rv"><span class="sec-num" aria-hidden="true">FAQ</span><h2 id="fq">{name} families <em>often ask.</em></h2></div>
    <div class="faq rv">
{faq_html(c["faqs"], "fq")}
    </div>
    <p class="county-note">Also serving families in {others}, and across Central Ohio.</p>
  </div>
</section>

{consult(f'{name} families, your first conversation is <em>free.</em>')}
</main>

''' + FOOTER
    pathlib.Path(path).write_text(html)

# ---------------------------------------------------------------- articles
ARTICLES = [
 dict(path="ohio-dissolution-vs-divorce.html", tag="Divorce", img="img/kitchen-table.jpg",
  title="Dissolution or divorce in Ohio: which path fits your family?",
  seo="Dissolution vs. Divorce in Ohio: Which Is Right for You?",
  desc="Ohio offers two ways to end a marriage. Here is how dissolution and divorce differ, how long each takes, and how to tell which one fits your situation.",
  teaser="Ohio gives you two ways to end a marriage. The right one depends on how much you and your spouse already agree on.",
  body='''<p>When people say they are &ldquo;getting a divorce&rdquo; in Ohio, they may actually be heading toward one of two different legal processes: a <b>dissolution</b> or a <b>divorce</b>. Both end the marriage. They just get there differently.</p>
<h3>Dissolution: when you already agree</h3>
<p>A dissolution is a no fault process. Both spouses work out every term first, including property, debts, spousal support, and if you have children, a parenting plan and child support. You then file together, asking the court to approve the agreement.</p>
<p>Ohio law sets the final hearing for 30 to 90 days after the petition is filed. Both spouses attend and tell the court they are satisfied with the agreement. For many families this is the faster, quieter, and less costly route.</p>
<h3>Divorce: when there are things to resolve</h3>
<p>A divorce starts when one spouse files a complaint with the court. Ohio law lists the grounds that can be used, including incompatibility (unless the other spouse denies it) and living separate and apart for a year. If you cannot agree on everything, the court will help resolve what is left, through negotiation, mediation, or ultimately a decision by the judge.</p>
<p>A divorce can still settle. Ohio even allows a divorce case to be converted into a dissolution if the two of you reach a full agreement along the way.</p>
<h3>How to tell which one fits</h3>
<ul>
<li>If you agree on every major issue, dissolution is usually worth considering.</li>
<li>If you agree on most things but not all, an uncontested divorce or negotiated settlement may fit.</li>
<li>If there are safety concerns, hidden assets, or deep disagreement about the children, a divorce gives you the court&rsquo;s protection and process.</li>
</ul>
<div class="takeaway"><b>The short version</b><p>Agreement decides the path. The more you agree on before filing, the simpler and faster the process tends to be. Either way, have an attorney review the terms, because what you sign is what you live with.</p></div>'''),
 dict(path="ohio-custody-unmarried-parents.html", tag="Custody", img="img/dad-child.jpg",
  title="Custody for unmarried parents in Ohio: where to start",
  seo="Child Custody for Unmarried Parents in Ohio: Where to Start",
  desc="In Ohio, unmarried parents do not automatically share custody. Here is what the law says, how paternity works, and how either parent can ask the court for parenting time.",
  teaser="Without a court order, Ohio law gives custody to one parent by default. Here is how both parents can get a clear, fair arrangement.",
  body='''<p>Many unmarried parents raise their children together for years without ever going to court. That works until it does not: a move, a new relationship, or a disagreement about school. At that point, it matters a great deal what Ohio law says when there is no court order.</p>
<h3>The default rule</h3>
<p>Under Ohio law, when a child is born to unmarried parents, the mother is the sole residential parent and legal custodian until a court issues an order that says otherwise. That is true even if both parents are named on the birth certificate and even if the child spends equal time in both homes.</p>
<h3>Step one: establish parentage</h3>
<p>Before a court can allocate parental rights, legal parentage needs to be established. Often this happens at the hospital, when both parents sign an Acknowledgment of Paternity. If that did not happen, parentage can be established through the county child support enforcement agency or through the court, usually with genetic testing.</p>
<h3>Step two: ask the court for an order</h3>
<p>Once parentage is established, either parent can file with the court to set custody, parenting time, and child support. Depending on the county, these cases are heard by the juvenile court or the domestic relations court. The court can name one parent the residential parent with a parenting time schedule for the other, or approve a shared parenting plan.</p>
<h3>What the court looks at</h3>
<p>Every decision is made on the child&rsquo;s best interest. Ohio law lists the factors, including each parent&rsquo;s wishes, the child&rsquo;s relationships and adjustment to home and school, each parent&rsquo;s willingness to support the child&rsquo;s relationship with the other parent, and the child&rsquo;s own wishes when the court considers it appropriate.</p>
<div class="takeaway"><b>The short version</b><p>An informal arrangement protects no one. Whether you are the parent with custody by default or the parent asking for time, a clear court order gives your child stability and gives both of you rights you can rely on.</p></div>'''),
 dict(path="before-you-file-ohio-divorce.html", tag="Getting started", img="img/mom-child.jpg",
  title="Before you file: Ohio residency rules and what to bring to your first consult",
  seo="Filing for Divorce in Ohio: Residency Rules and What to Bring",
  desc="How long you need to live in Ohio before filing for divorce, which county to file in, and a simple checklist for your first consultation.",
  teaser="Two residency rules decide when and where you can file. Plus a simple list of what to bring so your first consult counts.",
  body='''<p>If you are thinking about divorce or a custody case, a little preparation makes your first conversation with an attorney far more useful. Here is what to know before you file.</p>
<h3>Ohio&rsquo;s residency rules</h3>
<ul>
<li><b>Six months in Ohio.</b> To file for divorce, you must have lived in Ohio for at least six months immediately before filing. For a dissolution, at least one spouse must meet that requirement.</li>
<li><b>About 90 days in the county.</b> Ohio&rsquo;s court rules generally have you file in a county where you or your spouse has lived for at least 90 days.</li>
</ul>
<p>If you recently moved, these rules can affect when and where you file. That is worth sorting out before anything else.</p>
<h3>What to bring to your first consult</h3>
<p>You do not need everything on this list. Bring what you have; it helps your attorney give you real answers instead of general ones.</p>
<ul>
<li>Your date of marriage and, if it applies, your date of separation</li>
<li>The full name of the other party, so the firm can run a conflict check</li>
<li>Your children&rsquo;s names and dates of birth</li>
<li>Any existing court orders about custody, support, or protection</li>
<li>Any papers you have been served, such as a complaint or notice of hearing</li>
<li>A rough list of major assets and debts: home, vehicles, retirement accounts, loans</li>
<li>Recent income information, such as pay stubs or a tax return</li>
</ul>
<div class="takeaway"><b>The short version</b><p>Check the six month and 90 day rules, gather what you can from the list, and write down your top three questions. You will walk out of your first consult knowing where you stand.</p></div>'''),
]

def build_article(a):
    schemas = [{"@context":"https://schema.org","@type":"Article","headline":a["title"],"description":a["desc"],
                "datePublished":"2026-10-08","author":{"@type":"Organization","name":"Law Office of Cedric P. Collins, LLC"},
                "publisher":{"@type":"Organization","name":"Law Office of Cedric P. Collins, LLC"},
                "image":SITE+a["img"],"mainEntityOfPage":SITE+a["path"]},
               crumbs(("Home",""),("Resources","resources.html"),(a["title"],a["path"]))]
    html = head(f'{a["seo"]} | Cedric P. Collins', a["desc"], a["path"], schemas)
    html += "\n<!-- DRAFT: Cedric must review this article for legal accuracy before the site launches. -->\n" + header("resources.html") + f'''

<main id="main">
<article style="padding:54px 0 92px;position:relative;z-index:2">
  <div class="wrap">
    <div class="narrow" style="margin:0 auto">
      <p class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="resources.html">Resources</a> &nbsp;/&nbsp; <span>{a["tag"]}</span></p>
      <h1 class="page-h" style="max-width:none">{a["title"]}</h1>
      <p class="byline">Law Office of Cedric P. Collins &nbsp;·&nbsp; October 2026 &nbsp;·&nbsp; General information, not legal advice</p>
    </div>
    <div class="article-hero rv"><img src="{a["img"]}" alt="" /></div>
    <div class="prose narrow" style="margin:0 auto">
{a["body"]}
    </div>
  </div>
</article>

{NEWS}

{consult('Questions about <em>your</em> situation?', 'Every family is different. A free, confidential consult with Cedric turns general information into a plan for yours.')}
</main>

''' + FOOTER
    pathlib.Path(a["path"]).write_text(html)

def post_cards():
    return "".join(f'''<a class="post rv" href="{a["path"]}"><div class="pi"><img src="{a["img"]}" alt="" loading="lazy" /></div><div class="pb"><span class="tag">{a["tag"]}</span><h3>{a["title"]}</h3><p>{a["teaser"]}</p></div></a>''' for a in ARTICLES)

def build_resources():
    schemas = [{"@context":"https://schema.org","@type":"CollectionPage","name":"Resources for Ohio families","url":SITE+"resources.html"},
               crumbs(("Home",""),("Resources","resources.html"))]
    html = head("Ohio Divorce &amp; Custody Resources | Cedric P. Collins",
                "Plain language guides on Ohio divorce, dissolution, and child custody, plus a monthly note from attorney Cedric P. Collins.",
                "resources.html", schemas)
    html += "\n" + header("resources.html") + f'''

<main id="main">
<section class="page-hero">
  <div class="wrap">
    <p class="crumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <span>Resources</span></p>
    <h1 class="page-h">Plain answers for the <em>questions</em> keeping you up at night.</h1>
    <p class="sub">Short, practical guides on Ohio divorce and custody, written for parents, not lawyers. Read at your own pace, then talk with Cedric when you are ready.</p>
  </div>
</section>

<section class="block" style="padding-top:44px">
  <div class="wrap">
    <div class="posts">{post_cards()}</div>
  </div>
</section>

{NEWS}

{consult()}
</main>

''' + FOOTER
    pathlib.Path("resources.html").write_text(html)

# ---------------------------------------------------------------- patch existing pages
def patch_existing():
    for f in ["index.html","about.html","divorce.html","child-custody.html","contact.html"]:
        s = pathlib.Path(f).read_text()
        if "<!-- patched-oct26 -->" in s: continue
        active = f
        s = re.sub(r'<a href="#main" class="skip">.*?</header>', header(active), s, count=1, flags=re.S)
        s = re.sub(r'<footer>.*$', FOOTER, s, count=1, flags=re.S)
        s = s.replace('<meta name="robots" content="index, follow, max-image-preview:large" />\n', '')
        s = s.replace("<body>", "<body>\n<!-- patched-oct26 -->", 1)
        pathlib.Path(f).write_text(s)

def hero_photo(f, img, alt):
    s = pathlib.Path(f).read_text()
    if 'class="wrap hero-split"' in s: return
    m = re.search(r'<section class="page-hero">\s*<div class="wrap">(.*?)\n  </div>\n</section>', s, flags=re.S)
    assert m, f
    new = f'<section class="page-hero">\n  <div class="wrap hero-split">\n    <div>{m.group(1)}\n    </div>\n    <div class="ph-img rv"><img src="{img}" alt="{alt}" loading="eager" /></div>\n  </div>\n</section>'
    s = s[:m.start()] + new + s[m.end():]
    pathlib.Path(f).write_text(s)

FAMILIES = '''<section class="block" aria-labelledby="fam">
  <div class="wrap">
    <div class="sec-head rv"><span class="sec-num" aria-hidden="true">&mdash;</span><h2 id="fam">Every kind of family deserves a <em>steady advocate.</em></h2></div>
    <div class="families rv">
      <figure class="fam"><img src="img/dad-child.jpg" alt="A father sharing a warm moment with his young child" loading="lazy" /><figcaption><b>Dads</b><span>Custody, parenting time, and a real voice in your child&rsquo;s life.</span></figcaption></figure>
      <figure class="fam"><img src="img/mom-child.jpg" alt="A mother holding her child close" loading="lazy" /><figcaption><b>Moms</b><span>Stability for your children and a fair outcome for you.</span></figcaption></figure>
      <figure class="fam"><img src="img/grandparent.jpg" alt="A grandparent spending time with a grandchild" loading="lazy" /><figcaption><b>Grandparents</b><span>Third party custody and staying in a child&rsquo;s life.</span></figcaption></figure>
    </div>
  </div>
</section>
'''

BAND = '''<section class="photo-band" aria-label="Our approach">
  <img src="img/kids-playing.jpg" alt="Children playing outdoors in an Ohio park" loading="lazy" />
  <div class="wrap"><blockquote class="rv">Your children will remember how this season felt. Our job is to make it steadier.</blockquote><cite>Law Office of Cedric P. Collins</cite></div>
</section>
'''

def areas_section():
    cards = "".join(f'<a class="city rv" href="{city_file(s)}"><div class="ci"><img src="{CITY[s]["img"]}" alt="" loading="lazy" /></div><div class="cb"><h3>{n}</h3><p>{CITY[s]["counties"]}</p><div class="more">Family law in {n} &rarr;</div></div></a>' for s,n in CITIES)
    return f'''<section class="block" style="padding-top:0" aria-labelledby="areas">
  <div class="wrap">
    <div class="sec-head rv"><span class="sec-num" aria-hidden="true">&mdash;</span><h2 id="areas">Close to home, across <em>Central Ohio.</em></h2></div>
    <div class="cities">{cards}</div>
    <p class="county-note rv">Cedric practices in Franklin, Fairfield, and Licking Counties, from his office in Pickerington.</p>
  </div>
</section>
'''

def patch_home():
    s = pathlib.Path("index.html").read_text()
    if 'id="fam"' in s: return
    # families right after the credential band + marquee; photo band after "How Cedric can help"
    s = s.replace('<section class="block" aria-labelledby="s1">', FAMILIES + '\n<section class="block" style="padding-top:0" aria-labelledby="s1">', 1)
    s = s.replace('<section class="block" style="padding-top:0" aria-label="About attorney Cedric Collins">', BAND + '\n<section class="block" aria-label="About attorney Cedric Collins">', 1)
    s = s.replace('<section class="block" style="padding-top:0" aria-labelledby="s5">', areas_section() + '\n' + NEWS + '\n\n<section class="block" style="padding-top:0" aria-labelledby="s5">', 1)
    pathlib.Path("index.html").write_text(s)

def sitemap():
    pages = ["","about.html","divorce.html","child-custody.html","contact.html","resources.html"] + \
            [city_file(s) for s,_ in CITIES] + [a["path"] for a in ARTICLES]
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc><lastmod>2026-10-08</lastmod></url>" for p in pages)
    pathlib.Path("sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')

if __name__ == "__main__":
    patch_existing()
    patch_home()
    hero_photo("divorce.html", "img/kitchen-table.jpg", "A parent at the kitchen table working through paperwork calmly")
    hero_photo("child-custody.html", "img/coparent.jpg", "A parent walking with their child")
    hero_photo("about.html", "img/columbus.jpg", "The Columbus, Ohio skyline") if False else None
    for s,n in CITIES: build_city(s,n)
    for a in ARTICLES: build_article(a)
    build_resources()
    sitemap()
    print("built")
