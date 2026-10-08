"""Privacy policy, terms + SMS terms, and SMS consent for the contact form.
Written to Twilio A2P 10DLC review expectations: optional unchecked consent boxes,
separate service vs updates consent, HELP/STOP, frequency, rates, carrier line,
and no sharing of mobile opt-in data for marketing. DRAFT until Cedric approves."""

FIRM = "Law Office of Cedric P. Collins, LLC"
PHONE_TEL = "+17408808510"
PHONE = "(740) 880&#8202;8510"

CONSENT = f'''
          <fieldset class="consent">
            <legend>Text messages (optional)</legend>
            <label><input type="checkbox" name="sms_consent_service" value="yes" /> <span>I agree to receive text messages from {FIRM} about my inquiry, consultation scheduling, and appointment reminders at the number provided. Message frequency varies. Message and data rates may apply. Reply HELP for help or STOP to opt out.</span></label>
            <label><input type="checkbox" name="sms_consent_updates" value="yes" /> <span>I agree to receive occasional text messages from {FIRM} with firm news and family law updates. Message frequency varies. Message and data rates may apply. Reply HELP for help or STOP to opt out.</span></label>
            <p>Consent is not required to request a consultation. <a href="terms.html#sms">SMS Terms</a> &nbsp;·&nbsp; <a href="privacy.html">Privacy Policy</a></p>
          </fieldset>'''

CONTACT_BLOCK = f'<p>{FIRM}<br>38 East Columbus St., Suite 201, Pickerington, OH 43147<br>Phone: <a href="tel:{PHONE_TEL}">{PHONE}</a></p>'

PRIVACY = f"""<p>This Privacy Policy explains how {FIRM} (&ldquo;the firm,&rdquo; &ldquo;we,&rdquo; &ldquo;us&rdquo;) collects, uses, and protects information when you visit this website, contact us, or receive text messages from us.</p>
<h3>Information we collect</h3>
<ul>
<li>Information you give us through forms, chat, phone, or text, such as your name, email address, phone number, the type of legal matter, and anything you choose to share about your situation.</li>
<li>Documents you choose to upload before a consultation.</li>
<li>Basic technical information collected automatically when you visit, such as browser type, pages viewed, and general location, used to keep the site working and understand how it is used.</li>
</ul>
<h3>How we use it</h3>
<ul>
<li>To respond to your inquiry, schedule and confirm consultations, and send reminders.</li>
<li>To check for conflicts of interest before we can speak with you about your matter.</li>
<li>To send updates you have asked for, such as our monthly email or text updates.</li>
<li>To operate, secure, and improve this website.</li>
</ul>
<h3>Mobile information and text messaging</h3>
<p>We do not sell, rent, or share your mobile phone number, text messaging originator opt-in data, or consent with third parties or affiliates for their marketing or promotional purposes. Text messaging originator opt-in data and consent will not be shared with any third parties, except with service providers that help us deliver messages to you, such as our messaging platform and phone carrier, solely to provide the service.</p>
<p>You can opt out of text messages at any time by replying STOP. Reply HELP for help. See our <a href="terms.html#sms">SMS Terms</a>.</p>
<h3>How we share information</h3>
<p>We do not sell personal information. We share information only with service providers that help us run the firm, such as our website host, email and scheduling tools, practice management software, and messaging platform, and only as needed to provide their services to us. We may also disclose information when required by law or court order.</p>
<h3>Confidentiality and the attorney client relationship</h3>
<p>Contacting the firm through this website, by email, chat, phone, or text does not create an attorney client relationship. Until representation is confirmed in writing, please do not send confidential or time sensitive information.</p>
<h3>Security and retention</h3>
<p>We use reasonable safeguards to protect your information. No method of transmission over the internet is completely secure. We keep information as long as needed for the purposes above and as required by our professional obligations.</p>
<h3>Children</h3>
<p>This website is not directed to children under 13, and we do not knowingly collect their information online. Information about children shared by a parent in connection with a legal matter is handled under this policy.</p>
<h3>Your choices</h3>
<p>You can unsubscribe from emails with the link in any email, opt out of texts by replying STOP, or ask us to update or delete your contact information by reaching us below.</p>
<h3>Changes</h3>
<p>We may update this policy. The effective date at the top shows when it last changed.</p>
<h3>Contact</h3>
{CONTACT_BLOCK}"""

TERMS = f"""<h3>Website terms</h3>
<p>By using this website you agree to these terms. The content on this site is general information about Ohio family law. It is not legal advice, and it may not reflect the most current law. Every situation is different; speak with an attorney about yours.</p>
<p>Using this site, submitting a form, or contacting the firm by email, chat, phone, or text does not create an attorney client relationship. A relationship begins only when the firm agrees in writing to represent you.</p>
<p>Prior results do not guarantee a similar outcome. Links to other websites are provided for convenience; the firm is not responsible for their content.</p>
<h3 id="sms">SMS Terms</h3>
<p><b>Program.</b> {FIRM} text messaging.</p>
<p><b>What you will receive.</b> If you opt in, you may receive text messages about your inquiry, consultation scheduling, appointment reminders, and follow up on your request. If you separately opt in, you may also receive occasional firm news and family law updates.</p>
<p><b>How you opt in.</b> By checking an SMS consent box on our website forms, or by texting our firm number first and agreeing to receive replies. Consent is not required to request a consultation or to become a client.</p>
<p><b>Message frequency.</b> Message frequency varies.</p>
<p><b>Cost.</b> Message and data rates may apply.</p>
<p><b>Help and opting out.</b> Reply HELP for help, or call us at <a href="tel:{PHONE_TEL}">{PHONE}</a>. Reply STOP at any time to stop receiving messages. You will receive one final message confirming you have been unsubscribed.</p>
<p><b>Carriers.</b> Carriers are not liable for delayed or undelivered messages.</p>
<p><b>Privacy.</b> We do not share your mobile information or text messaging consent with third parties or affiliates for marketing purposes. See our <a href="privacy.html">Privacy Policy</a>.</p>
<p><b>Do not text confidential details.</b> Text messaging is not a secure channel. Please do not send confidential information by text until representation is confirmed.</p>
<h3>Contact</h3>
{CONTACT_BLOCK}"""

def patch_contact(pathlib):
    s = pathlib.Path("contact.html").read_text()
    if 'class="consent"' in s: return
    a = '          <div class="hp" aria-hidden="true">'
    assert a in s
    s = s.replace(a, CONSENT + "\n" + a, 1)
    s = s.replace('<option>Child support</option>', '<option>Child support</option>\n              <option>Changing an existing order</option>\n              <option>Grandparent or third party custody</option>\n              <option>Enforcing an order (contempt)</option>', 1)
    pathlib.Path("contact.html").write_text(s)
