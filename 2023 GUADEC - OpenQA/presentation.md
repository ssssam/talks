<!--
The best testing tools we've ever had
GUADEC 2023 - ...
... minutes
-->

# The best testing tools we've ever had

<div class="r-stretch"></div>

<div class="flex-row-stretch" markdown="1">
  <p class="left" style="flex: 1;" markdown="1">
  **Sam Thursfield**<br>
  **GUADEC 2023**
  </p>

  ![Codethink logo](./images/codethink-logo.svg){:.right style="flex: 1;"}
</div>

---

<!-- 1. Where we are -->

Open this URL in your laptop...

https://openqa.gnome.org/

<!-- FIXME: QR code?! -->

???

You can sign in with GNOME LDAP if you have it.

View "All tests" and select one test

Do this in browser ! Show:

  -- install: 
  --   it's creating an empty qemu VM
  --   installing GNOME OS with the latest ISO
  --   ...
  -- apps:
  --   it uses the preinstalled disk image
  -->

---

# Integration testing of GNOME OS

  * openqa.gnome.org is about ~1 year old and in "open beta" status
  * Tests run against GNOME OS: latest commit of every GNOME module + [Freedesktop SDK](https://gitlab.com/freedesktop-sdk/freedesktop-sdk/-/tree/master/elements) base OS
  * Each testsuite runs in new, temporary virtual machine

???

Notes:

  * distro independent - distros are doing their own integration testing (many also using openQA), but testing already-released versions of GNOME
  * good coverage of stuff which is difficult with project-specific tests: hardware support, initial setup, session management, font rendering ...
  * not a replacement for unit tests (errors are quite broad)
  * get bug reports as soon as you break something

---

Open a testsuite and look at some tests.

???

Show some screenshots, explain "Needles".

---

# openQA testing philosophy

  * Tests are Perl programs with full access to the VM
  * Test runner is separate from the web UI (you can run the testsuite on your laptop)
  * Strong support for screenshot testing (via "Needles")

???

You are not limited to screenshot testing.

Tests are Perl programs & can run arbitrary code. openQA is not only for screenshot tests.

But it has special helpers for screenshot testing. We'll go more into how that works.

---

Check the "Logs & Assets" tab

???

If you're a developer you're thinking, what do I do if this fails?

Obvious option: run the same OS image in gnome-boxes and reproduce the issue there

Quickest option: Look at the journal.

Show the serial0.txt log

Show link to Gitlab

---

# How it works

  * Gitlab pipeline for gnome-build-meta.git has a "test-s3-image" job
  * The runner registers as a temporary openQA worker
  * The test job is submitted to the web UI

???

This is a "non-standard" approach, which saves us from maintaining a fleet of physical runners.

---

# Here's what we can do today

  * Curate and browse screenshots of the next GNOME release
  * Run ~nightly tests as we develop new features

???

More ?

We can do integration testing of your latest GNOME modules from Git.

Let's write some tests!

But first... some notes on how we got here.

---

My story

 * Codethink (2011-)
 * Tracker (2011-)

???

I don't always do "about me", but it is relevant here to see why I've been pushing this recently...

Using GNOME since 2003 ([2.8](https://help.gnome.org/misc/release-notes/2.8/))

Codethink - somehow still work here - consultancy, mostly financial & automotive work now

Early projects: MeeGo - Tracker - critical bugs e.g. 100% CPU when you connect a USB stick.


No paid work on Tracker since 2012, but remained as a volunteer maintainer. Ported to Meson, set up initial Gitlab CI, in-tree "functional tests" testsuite.

---

# How do you write integration tests for a search engine?

Golden rule: if it's not tested, it doesn't work.

Actual bug reports:

  * Performance issues on corporate deployment with NFS home directory
  * GStreamer enters 100% CPU usage when typefinding files in a video game mod due to trying to decode them as MP3
  * ...

Input: an entire hard disk of random data.

Actual tests: https://gitlab.gnome.org/GNOME/tracker-miners/-/blob/master/tests/functional-tests/test_fts_basic.py

???

I'll leave you with this problem...

---

My story

 * Codethink (2011-)
 * Tracker (2011-)
 * GUADEC (2011-)

???

Desktop summit (2011), GUADEC in A Coruña (2012)

---

# GUADEC 2012

  * Colin Walters introduces OSTree and GNOME Continuous
  * First "GNOME OS" BOF
  * "Testable" initiative

???

We've been working towards "integration testing of GNOME as it happens" for over a decade.

---

Screenshot of GNOME Continuous

???

Reference also: GNOME OS, BuildStream, Freedesktop SDK

Meanwhile SUSE were working on openQA.

---

# openQA testing at Codethink

Began using it for automotive clients.

Also set up testing for open source projects:

  * Linux kernel (Sudip M.)
  * GNOME OS (James Thomas, Javier Jardón, me)

---


## How to get involved {:.r-fit-text}

<div class="left" markdown="1">

I will provide training on infra maintenance and writing tests - just ask!

  * Chat: Matrix [#gnome-os:gnome.org](https://app.element.io/#/room/#gnome-os:gnome.org)
  {:.fs-3}
  * Forum: [https://discourse.gnome.org/](https://discourse.gnome.org/)
  {:.fs-3}
  * Email: *sam@afuera.me.uk*
  {:.fs-3}

Also: [documentation](https://gitlab.gnome.org/GNOME/gnome-build-meta/-/wikis/openqa/OpenQA-for-GNOME-developers), [issue tracker](https://gitlab.gnome.org/GNOME/gnome-build-meta/-/wikis/openqa/OpenQA-for-GNOME-developers)
{:.fs-3}

<div class="flex-row-stretch" markdown="1">
  <p class="left" style="flex: 1;" markdown="1">
  **Sam Thursfield**<br>
  **FOSDEM 2023**
  </p>

  ![Codethink logo](./images/codethink-logo.svg){:.right style="flex: 1;"}
</div>
</div>
