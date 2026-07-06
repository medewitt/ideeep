---
title: Prospective Students
description: "Express interest in the IDEEEP concentration at Wake Forest — tell us about yourself and we will follow up as courses and opportunities open."
---

# Prospective Students

The IDEEEP concentration is in active development and is **not yet enrolling**.
The best thing you can do right now is tell us you are interested: we will keep
you posted as courses, certificates, and research opportunities open, and point
you toward the [Field Epidemiology and Tropical Medicine](field-epidemiology.md)
course and the [open learning resources](math.md) you can start with today.

Prefer email? Reach out to [Michael DeWitt](people.md) directly. Otherwise, the
short form below is the fastest way to get on our list.

<form name="interest" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/interest-thank-you.html" class="interest-form">
  <input type="hidden" name="form-name" value="interest">
  <p hidden><label>Do not fill this out if you are human: <input name="bot-field"></label></p>

  <div class="field">
    <label class="field-label" for="full_name">Full name <span class="req">*</span></label>
    <input type="text" id="full_name" name="full_name" required autocomplete="name">
  </div>

  <div class="field">
    <label class="field-label" for="email">Email address <span class="req">*</span>
      <span class="hint">We will use this to follow up about the concentration.</span>
    </label>
    <input type="email" id="email" name="email" required autocomplete="email">
  </div>

  <div class="field">
    <label class="field-label" for="phone">Phone <span class="hint">Optional.</span></label>
    <input type="tel" id="phone" name="phone" autocomplete="tel">
  </div>

  <div class="field">
    <label class="field-label" for="role">I am a&hellip; <span class="req">*</span></label>
    <select id="role" name="role" required>
      <option value="" disabled selected>Choose the option that best describes you&hellip;</option>
      <option>Prospective undergraduate</option>
      <option>Current Wake Forest undergraduate</option>
      <option>Transfer or visiting student</option>
      <option>Post-baccalaureate or graduate student</option>
      <option>Infectious Diseases fellow or clinician</option>
      <option>Public health or industry professional</option>
      <option>High school student</option>
      <option>Other</option>
    </select>
  </div>

  <div class="field">
    <label class="field-label" for="institution">Current school or organization
      <span class="hint">Leave blank if you are at Wake Forest.</span>
    </label>
    <input type="text" id="institution" name="institution" autocomplete="organization">
  </div>

  <div class="field">
    <label class="field-label" for="major">Major or field of study</label>
    <input type="text" id="major" name="major">
  </div>

  <div class="field">
    <label class="field-label" for="grad_year">Expected graduation year
      <span class="hint">For example, 2028.</span>
    </label>
    <input type="text" id="grad_year" name="grad_year">
  </div>

  <fieldset class="field">
    <legend>Research areas that interest you <span class="hint">Select all that apply.</span></legend>
    <div class="check-grid">
      <label class="check"><input type="checkbox" name="research_interests" value="Disease ecology and One Health"> Disease ecology and One Health</label>
      <label class="check"><input type="checkbox" name="research_interests" value="Zoonotic spillover and emergence"> Zoonotic spillover and emergence</label>
      <label class="check"><input type="checkbox" name="research_interests" value="Mathematical and computational modeling"> Mathematical and computational modeling</label>
      <label class="check"><input type="checkbox" name="research_interests" value="Field epidemiology and outbreak response"> Field epidemiology and outbreak response</label>
      <label class="check"><input type="checkbox" name="research_interests" value="Evolution of host-pathogen systems"> Evolution of host&ndash;pathogen systems</label>
      <label class="check"><input type="checkbox" name="research_interests" value="Diagnostics and laboratory methods"> Diagnostics and laboratory methods</label>
      <label class="check"><input type="checkbox" name="research_interests" value="Data science and scientific programming"> Data science and scientific programming</label>
    </div>
  </fieldset>

  <fieldset class="field">
    <legend>What would you like to hear about <span class="hint">Select all that apply.</span></legend>
    <div class="check-grid">
      <label class="check"><input type="checkbox" name="offerings" value="Concentration courses"> Concentration courses</label>
      <label class="check"><input type="checkbox" name="offerings" value="Field Epidemiology and Tropical Medicine"> Field Epidemiology and Tropical Medicine</label>
      <label class="check"><input type="checkbox" name="offerings" value="Graduate certificates"> Graduate certificates</label>
      <label class="check"><input type="checkbox" name="offerings" value="Short courses"> Short courses</label>
      <label class="check"><input type="checkbox" name="offerings" value="Research or independent study"> Research or independent study</label>
    </div>
  </fieldset>

  <div class="field">
    <label class="field-label" for="quant_background">Quantitative and programming background
      <span class="hint">Helps us point you to the right starting resources.</span>
    </label>
    <select id="quant_background" name="quant_background">
      <option value="" disabled selected>Choose one&hellip;</option>
      <option>None yet</option>
      <option>Some coursework</option>
      <option>Comfortable or advanced</option>
    </select>
  </div>

  <div class="field">
    <label class="field-label" for="message">Anything you would like to share
      <span class="hint">Questions, goals, or research interests.</span>
    </label>
    <textarea id="message" name="message"></textarea>
  </div>

  <div class="field">
    <label class="field-label" for="heard_from">How did you hear about the program</label>
    <select id="heard_from" name="heard_from">
      <option value="" disabled selected>Choose one&hellip;</option>
      <option>Faculty or advisor</option>
      <option>Current student</option>
      <option>Wake Forest website</option>
      <option>Social media</option>
      <option>Conference or event</option>
      <option>Other</option>
    </select>
  </div>

  <fieldset class="field">
    <legend>Before you submit</legend>
    <label class="check"><input type="checkbox" name="mailing_list" value="yes"> Add me to the interest mailing list <span class="hint">Occasional updates about courses and opportunities. Unsubscribe anytime.</span></label>
    <label class="check"><input type="checkbox" name="contact_consent" value="yes" required> I agree to be contacted about the IDEEEP concentration <span class="req">*</span></label>
  </fieldset>

  <button class="btn btn-primary" type="submit">Submit interest</button>
</form>
