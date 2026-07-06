# Interest form — Netlify setup and auto-reply copy

The prospective-student interest form lives at `content/prospective-students.md`
and posts to Netlify Forms (no backend). This note covers the two things that
are configured outside the codebase: the success redirect and the auto-reply.

## Success redirect (already wired in code)

The form redirects to a custom landing page on successful submission via its
`action` attribute:

```html
<form name="interest" method="POST" data-netlify="true"
      netlify-honeypot="bot-field" action="/interest-thank-you.html">
```

After a submission, Netlify sends the visitor to `/interest-thank-you.html`
(`content/interest-thank-you.md`). No dashboard setting is required for this —
it works as soon as the site is deployed. To change the destination, edit the
`action` on the form and the target page.

## First-deploy checklist (Netlify dashboard)

1. Deploy the branch. Netlify auto-detects the `interest` form from the built
   HTML (it must be present in the static output, which it is).
2. **Forms → interest** should appear after the first submission (send a test).
3. **Site settings → Forms → Form notifications**
   - Add an **email notification to yourself** so you are alerted on each
     submission (e.g. to `me.dewitt.jr@gmail.com`).
   - Add the **auto-reply / confirmation email** below.
4. Optional: enable reCAPTCHA (Forms → Spam filtering) in addition to the
   built-in `bot-field` honeypot if you see spam.

## Auto-reply (confirmation email to the submitter)

In **Form notifications → Add notification → Email confirmation**, set the
email field to the form's `email` field and paste the copy below.

**Subject:**

```
Thanks for your interest in the IDEEEP concentration at Wake Forest
```

**Reply-to:** `medewitt@wakehealth.edu`
**From name:** `Wake Forest IDEEEP`

**Body:**

```
Hi there,

Thank you for your interest in the Infectious Disease Ecology, Evolution &
Epidemiology (IDEEEP) concentration at Wake Forest. We have your information and
will reach out as courses, certificates, and research opportunities open.

The concentration is still in development and is not yet enrolling — but there
is plenty you can do now:

- Field Epidemiology and Tropical Medicine (BIO 301/302) is offered and open,
  with the next section in Summer 2027, including fieldwork in Tumbes and Lima,
  Peru: https://id3es.com/field-epidemiology.html

- Start building skills with our open learning resources in quantitative
  methods, scientific programming, and epidemiology:
  https://id3es.com/math.html

- Learn more about the program and its research:
  https://id3es.com/programs.html

If you have a specific question, just reply to this email and it will reach
Michael DeWitt directly.

We are glad you found us, and we will be in touch.

— The Wake Forest IDEEEP team
https://id3es.com
```

> Note: Netlify's built-in email confirmation is plain text. If you want an
> HTML-formatted auto-reply, route form submissions to an email service (e.g.
> via a Netlify function or a Zapier/Make webhook on the form-submission event)
> and send the confirmation from there.
